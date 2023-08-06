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
Snowflake usage module
"""

from typing import Any, Dict, Iterable, Iterator, Union

from metadata.generated.schema.entity.services.databaseService import (
    DatabaseServiceType,
)
from metadata.ingestion.api.source import Source, SourceStatus

# This import verifies that the dependencies are available.
from metadata.ingestion.models.table_queries import TableQuery
from metadata.ingestion.ometa.openmetadata_rest import MetadataServerConfig
from metadata.ingestion.source.snowflake import SnowflakeConfig
from metadata.ingestion.source.sql_alchemy_helper import (
    SQLAlchemyHelper,
    SQLSourceStatus,
)
from metadata.utils.helpers import get_start_and_end, ingest_lineage
from metadata.utils.sql_queries import SNOWFLAKE_SQL_STATEMENT


class SnowflakeUsageSource(Source[TableQuery]):
    """
    Snowflake Usage source

    Args:
        config:
        metadata_config:
        ctx:

    Attributes:
        config:
        analysis_date:
        sql_stmt:
        alchemy_helper:
        _extract_iter:
        _database:
        report:
        SQL_STATEMENT (str):
        WHERE_CLAUSE_SUFFIX_KEY (str):
        CLUSTER_SOURCE (str):
        USE_CATALOG_AS_CLUSTER_NAME (str):
        DATABASE_KEY (str):
        SERVICE_TYPE (str):
        DEFAULT_CLUSTER_SOURCE (str):
    """

    # SELECT statement from mysql information_schema
    # to extract table and column metadata
    SQL_STATEMENT = SNOWFLAKE_SQL_STATEMENT

    # CONFIG KEYS
    WHERE_CLAUSE_SUFFIX_KEY = "where_clause"
    CLUSTER_SOURCE = "cluster_source"
    CLUSTER_KEY = "cluster_key"
    USE_CATALOG_AS_CLUSTER_NAME = "use_catalog_as_cluster_name"
    DATABASE_KEY = "database_key"
    SERVICE_TYPE = DatabaseServiceType.Snowflake.value
    DEFAULT_CLUSTER_SOURCE = "CURRENT_DATABASE()"

    def __init__(self, config, metadata_config, ctx):
        super().__init__(ctx)
        self.config = config
        start, end = get_start_and_end(config.duration)
        self.analysis_date = start
        self.metadata_config = metadata_config
        self.sql_stmt = SnowflakeUsageSource.SQL_STATEMENT.format(
            start_date=start, end_date=end
        )
        self.alchemy_helper = SQLAlchemyHelper(
            config, metadata_config, ctx, "Snowflake", self.sql_stmt
        )
        self._extract_iter: Union[None, Iterator] = None
        self._database = "Snowflake"
        self.report = SQLSourceStatus()

    @classmethod
    def create(cls, config_dict, metadata_config_dict, ctx):
        config = SnowflakeConfig.parse_obj(config_dict)
        metadata_config = MetadataServerConfig.parse_obj(metadata_config_dict)
        return cls(config, metadata_config, ctx)

    def prepare(self):
        pass

    def _get_raw_extract_iter(self) -> Iterable[Dict[str, Any]]:
        """
        Provides iterator of result row from SQLAlchemy helper
        :return:
        """
        rows = self.alchemy_helper.execute_query()
        for row in rows:
            yield row

    def next_record(self) -> Iterable[TableQuery]:
        """
        Using itertools.groupby and raw level iterator,
        it groups to table and yields TableMetadata
        :return:
        """
        for row in self._get_raw_extract_iter():
            table_query = TableQuery(
                query=row["query_type"],
                user_name=row["user_name"],
                starttime=str(row["start_time"]),
                endtime=str(row["end_time"]),
                analysis_date=self.analysis_date,
                aborted="1969" in str(row["end_time"]),
                database=row["database_name"],
                sql=row["query_text"],
                service_name=self.config.service_name,
            )
            if row["schema_name"] is not None:
                self.report.scanned(f"{row['database_name']}.{row['schema_name']}")
            else:
                self.report.scanned(f"{row['database_name']}")
            yield table_query
            query_info = {
                "sql": table_query.sql,
                "from_type": "table",
                "to_type": "table",
                "service_name": self.config.service_name,
            }
            ingest_lineage(query_info, self.metadata_config)

    def get_report(self):
        """
        get report

        Returns:
        """
        return self.report

    def close(self):
        self.alchemy_helper.close()

    def get_status(self) -> SourceStatus:
        return self.report
