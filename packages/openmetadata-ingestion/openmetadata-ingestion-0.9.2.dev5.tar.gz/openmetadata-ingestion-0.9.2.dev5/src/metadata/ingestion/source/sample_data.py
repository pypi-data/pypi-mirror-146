#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import csv
import json
import logging
import os
import random
import uuid
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Union

from pydantic import ValidationError

from metadata.config.common import ConfigModel
from metadata.generated.schema.api.data.createMlModel import CreateMlModelRequest
from metadata.generated.schema.api.data.createTopic import CreateTopicRequest
from metadata.generated.schema.api.lineage.addLineage import AddLineageRequest
from metadata.generated.schema.api.teams.createRole import CreateRoleRequest
from metadata.generated.schema.api.teams.createTeam import CreateTeamRequest
from metadata.generated.schema.api.teams.createUser import CreateUserRequest
from metadata.generated.schema.api.tests.createColumnTest import CreateColumnTestRequest
from metadata.generated.schema.api.tests.createTableTest import CreateTableTestRequest
from metadata.generated.schema.entity.data.database import Database
from metadata.generated.schema.entity.data.location import Location, LocationType
from metadata.generated.schema.entity.data.pipeline import Pipeline
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.entity.services.databaseService import (
    DatabaseServiceType,
)
from metadata.generated.schema.entity.teams.user import User
from metadata.generated.schema.tests.basic import TestCaseResult
from metadata.generated.schema.tests.columnTest import ColumnTestCase
from metadata.generated.schema.tests.tableTest import TableTestCase
from metadata.generated.schema.type.entityLineage import EntitiesEdge
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.ingestion.api.common import Entity
from metadata.ingestion.api.source import Source, SourceStatus
from metadata.ingestion.models.ometa_table_db import OMetaDatabaseAndTable
from metadata.ingestion.models.table_metadata import Chart, Dashboard
from metadata.ingestion.models.table_tests import OMetaTableTest
from metadata.ingestion.models.user import OMetaUserProfile
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.ingestion.ometa.openmetadata_rest import MetadataServerConfig
from metadata.utils.helpers import (
    get_dashboard_service_or_create,
    get_database_service_or_create,
    get_database_service_or_create_v2,
    get_messaging_service_or_create,
    get_pipeline_service_or_create,
    get_storage_service_or_create,
)

logger: logging.Logger = logging.getLogger(__name__)

COLUMN_NAME = "Column"
KEY_TYPE = "Key type"
DATA_TYPE = "Data type"
COL_DESCRIPTION = "Description"
TableKey = namedtuple("TableKey", ["schema", "table_name"])


class InvalidSampleDataException(Exception):
    """
    Sample data is not valid to be ingested
    """


def get_lineage_entity_ref(edge, metadata_config) -> EntityReference:
    metadata = OpenMetadata(metadata_config)
    fqn = edge["fqn"]
    if edge["type"] == "table":
        table = metadata.get_by_name(entity=Table, fqdn=fqn)
        return EntityReference(id=table.id, type="table")
    elif edge["type"] == "pipeline":
        pipeline = metadata.get_by_name(entity=Pipeline, fqdn=fqn)
        return EntityReference(id=pipeline.id, type="pipeline")
    elif edge["type"] == "dashboard":
        dashboard = metadata.get_by_name(entity=Dashboard, fqdn=fqn)
        return EntityReference(id=dashboard.id, type="dashboard")


def get_table_key(row: Dict[str, Any]) -> Union[TableKey, None]:
    """
    Table key consists of schema and table name
    :param row:
    :return:
    """
    return TableKey(schema=row["schema"], table_name=row["table_name"])


class SampleDataSourceConfig(ConfigModel):
    sample_data_folder: str
    service_name: str = "bigquery_gcp"
    database: str = "warehouse"
    service_type: str = DatabaseServiceType.BigQuery.value
    scheme: str = "bigquery+pymysql"
    host_port: str = "9999"

    def get_sample_data_folder(self):
        return self.sample_data_folder

    def get_service_type(self):
        return self.service_type


@dataclass
class SampleDataSourceStatus(SourceStatus):
    success: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def scanned(self, entity_type: str, entity_name: str) -> None:
        self.success.append(entity_name)
        logger.info("{} Scanned: {}".format(entity_type, entity_name))

    def filtered(self, entity_type: str, entity_name: str, err: str) -> None:
        self.warnings.append(entity_name)
        logger.warning("Dropped {} {} due to {}".format(entity_type, entity_name, err))


class TableSchema:
    def __init__(self, filename):
        # error if the file is not csv file
        if not filename.endswith(".csv"):
            raise Exception("Input file should be a csv file")

        # file name is assumed to be the table name
        basename = os.path.basename(filename)
        self.table_name = os.path.splitext(basename)[0]

        with open(filename, "r") as fin:
            self.columns = [dict(i) for i in csv.DictReader(fin)]

    def primary_keys(self):
        return [c[COLUMN_NAME] for c in self.columns if c[KEY_TYPE] == "PK"]

    def foreign_keys(self):
        return [c[COLUMN_NAME] for c in self.columns if c[KEY_TYPE] == "FK"]

    def get_name(self):
        return self.table_name

    def get_schema(self):
        return self.columns

    def get_column_names(self):
        return [c[COLUMN_NAME] for c in self.columns]


class SampleTableMetadataGenerator:
    def __init__(self, table_to_df_dict, table_to_schema_map):
        self.table_to_df_dict = table_to_df_dict
        self.table_to_schema_map = table_to_schema_map
        self.sample_user = None
        self.sample_table = None
        self.sample_table_owner = None
        self.sample_table_last_updated = None

    def get_empty_dict_with_cols(self, columns):
        data = {}
        for c in columns:
            data[c] = []
        return data


class SampleDataSource(Source[Entity]):
    """
    Loads JSON data and prepares the required
    python objects to be sent to the Sink.
    """

    def __init__(
        self, config: SampleDataSourceConfig, metadata_config: MetadataServerConfig, ctx
    ):
        super().__init__(ctx)
        self.status = SampleDataSourceStatus()
        self.config = config
        self.metadata_config = metadata_config
        self.metadata = OpenMetadata(metadata_config)
        self.storage_service_json = json.load(
            open(self.config.sample_data_folder + "/locations/service.json", "r")
        )
        self.locations = json.load(
            open(self.config.sample_data_folder + "/locations/locations.json", "r")
        )
        self.storage_service = get_storage_service_or_create(
            service_json=self.storage_service_json,
            metadata_config=metadata_config,
        )
        self.glue_storage_service_json = json.load(
            open(self.config.sample_data_folder + "/glue/storage_service.json", "r")
        )
        self.glue_database_service_json = json.load(
            open(self.config.sample_data_folder + "/glue/database_service.json", "r")
        )
        self.glue_database = json.load(
            open(self.config.sample_data_folder + "/glue/database.json", "r")
        )
        self.glue_tables = json.load(
            open(self.config.sample_data_folder + "/glue/tables.json", "r")
        )
        self.glue_database_service = get_database_service_or_create_v2(
            service_json=self.glue_database_service_json,
            metadata_config=metadata_config,
        )
        self.glue_storage_service = get_storage_service_or_create(
            self.glue_storage_service_json,
            metadata_config,
        )
        self.database_service_json = json.load(
            open(self.config.sample_data_folder + "/datasets/service.json", "r")
        )
        self.database = json.load(
            open(self.config.sample_data_folder + "/datasets/database.json", "r")
        )
        self.tables = json.load(
            open(self.config.sample_data_folder + "/datasets/tables.json", "r")
        )
        self.database_service = get_database_service_or_create(
            config=config, metadata_config=self.metadata_config
        )
        self.kafka_service_json = json.load(
            open(self.config.sample_data_folder + "/topics/service.json", "r")
        )
        self.topics = json.load(
            open(self.config.sample_data_folder + "/topics/topics.json", "r")
        )
        self.kafka_service = get_messaging_service_or_create(
            service_name=self.kafka_service_json.get("name"),
            message_service_type=self.kafka_service_json.get("serviceType"),
            schema_registry_url=self.kafka_service_json.get("schemaRegistry"),
            brokers=self.kafka_service_json.get("brokers"),
            metadata_config=self.metadata_config,
        )
        self.dashboard_service_json = json.load(
            open(self.config.sample_data_folder + "/dashboards/service.json", "r")
        )
        self.charts = json.load(
            open(self.config.sample_data_folder + "/dashboards/charts.json", "r")
        )
        self.dashboards = json.load(
            open(self.config.sample_data_folder + "/dashboards/dashboards.json", "r")
        )
        self.dashboard_service = get_dashboard_service_or_create(
            service_name=self.dashboard_service_json.get("name"),
            dashboard_service_type=self.dashboard_service_json.get("serviceType"),
            username=self.dashboard_service_json.get("username"),
            password=self.dashboard_service_json.get("password"),
            dashboard_url=self.dashboard_service_json.get("dashboardUrl"),
            metadata_config=metadata_config,
        )
        self.pipeline_service_json = json.load(
            open(self.config.sample_data_folder + "/pipelines/service.json", "r")
        )
        self.pipelines = json.load(
            open(self.config.sample_data_folder + "/pipelines/pipelines.json", "r")
        )
        self.pipeline_service = get_pipeline_service_or_create(
            service_json=self.pipeline_service_json,
            metadata_config=metadata_config,
        )
        self.lineage = json.load(
            open(self.config.sample_data_folder + "/lineage/lineage.json", "r")
        )
        self.users = json.load(
            open(self.config.sample_data_folder + "/users/users.json", "r")
        )
        self.models = json.load(
            open(self.config.sample_data_folder + "/models/models.json", "r")
        )
        self.user_entity = {}
        self.table_tests = json.load(
            open(self.config.sample_data_folder + "/datasets/tableTests.json", "r")
        )

    @classmethod
    def create(cls, config_dict, metadata_config_dict, ctx):
        config = SampleDataSourceConfig.parse_obj(config_dict)
        metadata_config = MetadataServerConfig.parse_obj(metadata_config_dict)
        return cls(config, metadata_config, ctx)

    def prepare(self):
        pass

    def next_record(self) -> Iterable[Entity]:
        yield from self.ingest_users()
        yield from self.ingest_locations()
        yield from self.ingest_glue()
        yield from self.ingest_tables()
        yield from self.ingest_table_tests()
        yield from self.ingest_topics()
        yield from self.ingest_charts()
        yield from self.ingest_dashboards()
        yield from self.ingest_pipelines()
        yield from self.ingest_lineage()
        yield from self.ingest_mlmodels()

    def ingest_locations(self) -> Iterable[Location]:
        for location in self.locations["locations"]:
            location_ev = Location(
                id=uuid.uuid4(),
                name=location["name"],
                displayName=location["displayName"],
                description=location["description"],
                locationType=location["locationType"],
                service=EntityReference(
                    id=self.storage_service.id, type="storageService"
                ),
            )
            yield location_ev

    def ingest_glue(self) -> Iterable[OMetaDatabaseAndTable]:
        db = Database(
            id=uuid.uuid4(),
            name=self.glue_database["name"],
            description=self.glue_database["description"],
            service=EntityReference(
                id=self.glue_database_service.id,
                type=self.glue_database_service.serviceType.value,
            ),
        )
        for table in self.glue_tables["tables"]:
            table["id"] = uuid.uuid4()
            parameters = table.get("Parameters")
            table = {key: val for key, val in table.items() if key != "Parameters"}
            table_metadata = Table(**table)
            location_type = LocationType.Table
            if parameters:
                location_type = (
                    location_type
                    if parameters.get("table_type") != "ICEBERG"
                    else LocationType.Iceberg
                )
            location_metadata = Location(
                id=uuid.uuid4(),
                name="s3://glue_bucket/dwh/schema/" + table["name"],
                description=table["description"],
                locationType=location_type,
                service=EntityReference(
                    id=self.glue_storage_service.id, type="storageService"
                ),
            )
            db_table_location = OMetaDatabaseAndTable(
                database=db, table=table_metadata, location=location_metadata
            )
            self.status.scanned("table", table_metadata.name.__root__)
            yield db_table_location

    def ingest_tables(self) -> Iterable[OMetaDatabaseAndTable]:
        db = Database(
            id=uuid.uuid4(),
            name=self.database["name"],
            description=self.database["description"],
            service=EntityReference(
                id=self.database_service.id, type=self.config.service_type
            ),
        )
        resp = self.metadata.list_entities(entity=User, limit=5)
        self.user_entity = resp.entities
        for table in self.tables["tables"]:
            for sql_object in table["tableQueries"]:
                user_entity = self.user_entity[random.choice(range(5))]
                user_dict = {
                    "id": user_entity.id,
                    "name": user_entity.name.__root__,
                    "displayName": user_entity.displayName,
                    "href": user_entity.href,
                    "description": user_entity.description,
                }
                sql_object["user"] = EntityReference(**user_dict, type="user")
            table_metadata = Table(**table)
            table_and_db = OMetaDatabaseAndTable(table=table_metadata, database=db)
            self.status.scanned("table", table_metadata.name.__root__)
            yield table_and_db

    def ingest_topics(self) -> Iterable[CreateTopicRequest]:
        for topic in self.topics["topics"]:
            topic["service"] = EntityReference(
                id=self.kafka_service.id, type="messagingService"
            )
            create_topic = CreateTopicRequest(**topic)
            self.status.scanned("topic", create_topic.name.__root__)
            yield create_topic

    def ingest_charts(self) -> Iterable[Chart]:
        for chart in self.charts["charts"]:
            try:
                chart_ev = Chart(
                    name=chart["name"],
                    displayName=chart["displayName"],
                    description=chart["description"],
                    chart_type=chart["chartType"],
                    url=chart["chartUrl"],
                    service=EntityReference(
                        id=self.dashboard_service.id, type="dashboardService"
                    ),
                )
                self.status.scanned("chart", chart_ev.name)
                yield chart_ev
            except ValidationError as err:
                logger.error(err)

    def ingest_dashboards(self) -> Iterable[Dashboard]:
        for dashboard in self.dashboards["dashboards"]:
            dashboard_ev = Dashboard(
                name=dashboard["name"],
                displayName=dashboard["displayName"],
                description=dashboard["description"],
                url=dashboard["dashboardUrl"],
                charts=dashboard["charts"],
                service=EntityReference(
                    id=self.dashboard_service.id, type="dashboardService"
                ),
            )
            self.status.scanned("dashboard", dashboard_ev.name)
            yield dashboard_ev

    def ingest_pipelines(self) -> Iterable[Dashboard]:
        for pipeline in self.pipelines["pipelines"]:
            pipeline_ev = Pipeline(
                id=uuid.uuid4(),
                name=pipeline["name"],
                displayName=pipeline["displayName"],
                description=pipeline["description"],
                pipelineUrl=pipeline["pipelineUrl"],
                tasks=pipeline["tasks"],
                service=EntityReference(
                    id=self.pipeline_service.id, type="pipelineService"
                ),
            )
            yield pipeline_ev

    def ingest_lineage(self) -> Iterable[AddLineageRequest]:
        for edge in self.lineage:
            from_entity_ref = get_lineage_entity_ref(edge["from"], self.metadata_config)
            to_entity_ref = get_lineage_entity_ref(edge["to"], self.metadata_config)
            lineage = AddLineageRequest(
                edge=EntitiesEdge(fromEntity=from_entity_ref, toEntity=to_entity_ref)
            )
            yield lineage

    def ingest_mlmodels(self) -> Iterable[CreateMlModelRequest]:
        """
        Convert sample model data into a Model Entity
        to feed the metastore
        """
        from metadata.generated.schema.entity.data.dashboard import Dashboard

        for model in self.models:
            # Fetch linked dashboard ID from name
            fqdn = model["dashboard"]
            dashboard = self.metadata.get_by_name(entity=Dashboard, fqdn=fqdn)

            if not dashboard:
                raise InvalidSampleDataException(
                    f"Cannot find {fqdn} in Sample Dashboards"
                )

            dashboard_id = str(dashboard.id.__root__)

            model_ev = CreateMlModelRequest(
                name=model["name"],
                displayName=model["displayName"],
                description=model["description"],
                algorithm=model["algorithm"],
                dashboard=EntityReference(id=dashboard_id, type="dashboard"),
            )
            yield model_ev

    def ingest_users(self) -> Iterable[OMetaUserProfile]:
        try:
            for user in self.users["users"]:
                teams = [
                    CreateTeamRequest(
                        name=user["teams"],
                        displayName=user["teams"],
                        description=f"This is {user['teams']} description.",
                    )
                ]
                roles = (
                    [
                        CreateRoleRequest(
                            name=role,
                            description=f"This is {role} description.",
                        )
                        for role in user["roles"]
                    ]
                    if "roles" in user
                    else []
                )
                user_metadata = CreateUserRequest(
                    name=user["name"],
                    displayName=user["displayName"],
                    email=user["email"],
                )

                yield OMetaUserProfile(user=user_metadata, teams=teams, roles=roles)
        except Exception as err:
            logger.error(err)

    def ingest_table_tests(self) -> Iterable[OMetaTableTest]:
        """
        Iterate over all tables and fetch
        the sample test data. For each table test and column
        test, prepare all TestCaseResults
        """
        try:
            for test_def in self.table_tests:
                table_name = test_def["table"]

                for table_test in test_def["tableTests"]:
                    create_table_test = CreateTableTestRequest(
                        description=table_test.get("description"),
                        testCase=TableTestCase.parse_obj(table_test["testCase"]),
                        executionFrequency=table_test["executionFrequency"],
                        result=TestCaseResult.parse_obj(table_test["result"]),
                    )
                    yield OMetaTableTest(
                        table_name=table_name, table_test=create_table_test
                    )

                for col_test in test_def["columnTests"]:
                    create_column_test = CreateColumnTestRequest(
                        description=col_test.get("description"),
                        columnName=col_test["columnName"],
                        testCase=ColumnTestCase.parse_obj(col_test["testCase"]),
                        executionFrequency=col_test["executionFrequency"],
                        result=TestCaseResult.parse_obj(col_test["result"]),
                    )
                    yield OMetaTableTest(
                        table_name=table_name, column_test=create_column_test
                    )
        except Exception as err:  # pylint: disable=broad-except
            logger.error(err)

    def close(self):
        pass

    def get_status(self):
        return self.status
