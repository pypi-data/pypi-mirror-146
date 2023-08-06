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
"""
Tableau source module
"""

import logging
import uuid
from typing import Iterable, List, Optional

import dateutil.parser as dateparser
from pydantic import SecretStr
from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils.querying import (
    get_views_dataframe,
    get_workbook_connections_dataframe,
    get_workbooks_dataframe,
)

from metadata.generated.schema.api.lineage.addLineage import AddLineageRequest
from metadata.generated.schema.entity.data.dashboard import (
    Dashboard as Dashboard_Entity,
)
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.entity.services.dashboardService import (
    DashboardServiceType,
)
from metadata.generated.schema.type.entityLineage import EntitiesEdge
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.ingestion.api.common import (
    ConfigModel,
    Entity,
    IncludeFilterPattern,
    WorkflowContext,
)
from metadata.ingestion.api.source import Source, SourceStatus
from metadata.ingestion.models.table_metadata import Chart, Dashboard, DashboardOwner
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.ingestion.ometa.openmetadata_rest import MetadataServerConfig
from metadata.utils.helpers import get_dashboard_service_or_create

logger = logging.getLogger(__name__)


class TableauSourceConfig(ConfigModel):
    """Tableau pydantic source model"""

    username: Optional[str] = None
    password: Optional[SecretStr] = None
    server: str
    api_version: str
    env: Optional[str] = "tableau_prod"
    site_name: str
    site_url: str
    db_service_name: Optional[str] = None
    service_name: str
    service_type: str = DashboardServiceType.Tableau.value
    personal_access_token_name: Optional[str] = None
    personal_access_token_secret: Optional[str] = None
    dashboard_pattern: IncludeFilterPattern = IncludeFilterPattern.allow_all()
    chart_pattern: IncludeFilterPattern = IncludeFilterPattern.allow_all()


class TableauSource(Source[Entity]):
    """Tableau source entity class

    Args:
        config:
        metadata_config:
        ctx:

    Attributes:
        config:
        metadata_config:
        status:
        service:
        dashboard:
        all_dashboard_details:
    """

    config: TableauSourceConfig
    metadata_config: MetadataServerConfig
    status: SourceStatus

    def __init__(
        self,
        config: TableauSourceConfig,
        metadata_config: MetadataServerConfig,
        ctx: WorkflowContext,
    ):
        super().__init__(ctx)
        self.config = config
        self.metadata_config = metadata_config
        self.client = self.tableau_client()
        self.service = get_dashboard_service_or_create(
            service_name=config.service_name,
            dashboard_service_type=DashboardServiceType.Tableau.name,
            username=config.username,
            password=config.password.get_secret_value() if config.password else None,
            dashboard_url=config.server,
            metadata_config=metadata_config,
        )
        self.status = SourceStatus()
        self.metadata_client = OpenMetadata(self.metadata_config)
        self.dashboards = get_workbooks_dataframe(self.client).to_dict()
        self.all_dashboard_details = get_views_dataframe(self.client).to_dict()

    def tableau_client(self):
        """Tableau client method

        Returns:
        """
        tableau_server_config = {
            f"{self.config.env}": {
                "server": self.config.server,
                "api_version": self.config.api_version,
                "site_name": self.config.site_name,
                "site_url": self.config.site_url,
            }
        }
        if self.config.username and self.config.password:
            tableau_server_config[self.config.env]["username"] = self.config.username
            tableau_server_config[self.config.env][
                "password"
            ] = self.config.password.get_secret_value()
        elif (
            self.config.personal_access_token_name
            and self.config.personal_access_token_secret
        ):
            tableau_server_config[self.config.env][
                "personal_access_token_name"
            ] = self.config.personal_access_token_name
            tableau_server_config[self.config.env][
                "personal_access_token_secret"
            ] = self.config.personal_access_token_secret
        try:
            conn = TableauServerConnection(
                config_json=tableau_server_config, env=self.config.env
            )
            conn.sign_in().json()
        except Exception as err:  # pylint: disable=broad-except
            logger.error("%s: %s", repr(err), err)
        return conn

    @classmethod
    def create(
        cls, config_dict: dict, metadata_config_dict: dict, ctx: WorkflowContext
    ):
        config = TableauSourceConfig.parse_obj(config_dict)
        metadata_config = MetadataServerConfig.parse_obj(metadata_config_dict)
        return cls(config, metadata_config, ctx)

    def prepare(self):
        pass

    def next_record(self) -> Iterable[Entity]:
        yield from self._get_tableau_charts()
        yield from self._get_tableau_dashboard()

    @staticmethod
    def get_owner(owner) -> List[DashboardOwner]:
        """Get dashboard owner

        Args:
            owner:
        Returns:
            List[DashboardOwner]
        """
        parts = owner["fullName"].split(" ")
        first_name = " ".join(parts[: len(owner) // 2])
        last_name = " ".join(parts[len(owner) // 2 :])
        return [
            DashboardOwner(
                first_name=first_name,
                last_name=last_name,
                username=owner["name"],
            )
        ]

    def get_lineage(self, datasource_list, dashboard_name) -> AddLineageRequest:
        for datasource in datasource_list:
            try:
                table_fqdn = datasource.split("(")[1].split(")")[0]
                dashboard_fqdn = f"{self.config.service_name}.{dashboard_name}"
                table_fqdn = f"{self.config.db_service_name}.{table_fqdn}"
                table_entity = self.metadata_client.get_by_name(
                    entity=Table, fqdn=table_fqdn
                )
                dashboard_entity = self.metadata_client.get_by_name(
                    entity=Dashboard_Entity, fqdn=dashboard_fqdn
                )
                if table_entity and dashboard_entity:
                    lineage = AddLineageRequest(
                        edge=EntitiesEdge(
                            fromEntity=EntityReference(
                                id=table_entity.id.__root__, type="table"
                            ),
                            toEntity=EntityReference(
                                id=dashboard_entity.id.__root__, type="dashboard"
                            ),
                        )
                    )
                    yield lineage
            except (Exception, IndexError) as err:
                logger.error(err)

    def _get_tableau_dashboard(self) -> Dashboard:
        for index in range(len(self.dashboards["id"])):
            dashboard_id = self.dashboards["id"][index]
            dashboard_name = self.dashboards["name"][index]
            dashboard_tag = self.dashboards["tags"][index]
            dashboard_url = self.dashboards["webpageUrl"][index]
            datasource_list = (
                get_workbook_connections_dataframe(self.client, dashboard_id)
                .get("datasource_name")
                .tolist()
            )
            tag_labels = []
            if hasattr(dashboard_tag, "tag"):
                for tag in dashboard_tag["tag"]:
                    tag_labels.append(tag["label"])
            dashboard_chart = []
            for chart_index in self.all_dashboard_details["workbook"]:
                dashboard_owner = self.all_dashboard_details["owner"][chart_index]
                chart = self.all_dashboard_details["workbook"][chart_index]
                if chart["id"] == dashboard_id:
                    dashboard_chart.append(
                        self.all_dashboard_details["name"][chart_index]
                    )
            yield Dashboard(
                id=uuid.uuid4(),
                name=dashboard_id,
                displayName=dashboard_name,
                description="",
                owner=self.get_owner(dashboard_owner),
                charts=dashboard_chart,
                tags=list(tag_labels),
                url=dashboard_url,
                service=EntityReference(id=self.service.id, type="dashboardService"),
                last_modified=dateparser.parse(chart["updatedAt"]).timestamp() * 1000,
            )
            if self.config.db_service_name:
                yield from self.get_lineage(datasource_list, dashboard_id)

    def _get_tableau_charts(self):
        for index in range(len(self.all_dashboard_details["id"])):
            chart_name = self.all_dashboard_details["name"][index]
            chart_id = self.all_dashboard_details["id"][index]
            chart_tags = self.all_dashboard_details["tags"][index]
            chart_type = self.all_dashboard_details["sheetType"][index]
            chart_url = (
                f"{self.config.server}/#/site/{self.config.site_name}"
                f"{self.all_dashboard_details['contentUrl'][index]}"
            )
            chart_owner = self.all_dashboard_details["owner"][index]
            chart_datasource_fqn = chart_url.replace("/", ".")
            chart_last_modified = self.all_dashboard_details["updatedAt"][index]
            tag_labels = []
            if hasattr(chart_tags, "tag"):
                for tag in chart_tags["tag"]:
                    tag_labels.append(tag["label"])
            yield Chart(
                name=chart_id,
                displayName=chart_name,
                description="",
                chart_type=chart_type,
                url=chart_url,
                owners=self.get_owner(chart_owner),
                datasource_fqn=chart_datasource_fqn,
                last_modified=dateparser.parse(chart_last_modified).timestamp() * 1000,
                service=EntityReference(id=self.service.id, type="dashboardService"),
            )

    def get_status(self) -> SourceStatus:
        return self.status

    def close(self):
        pass
