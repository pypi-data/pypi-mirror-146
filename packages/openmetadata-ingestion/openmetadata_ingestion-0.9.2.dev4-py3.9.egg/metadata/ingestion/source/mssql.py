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
"""MSSQL source module"""
from typing import Optional

from metadata.generated.schema.entity.services.databaseService import (
    DatabaseServiceType,
)
from metadata.ingestion.ometa.openmetadata_rest import MetadataServerConfig
from metadata.ingestion.source.sql_source import SQLSource
from metadata.ingestion.source.sql_source_common import SQLConnectionConfig


class MssqlConfig(SQLConnectionConfig):
    """MSSQL config -- extends SQLConnectionConfig class"""

    host_port = "localhost:1433"
    scheme = "mssql+pytds"
    service_type = DatabaseServiceType.MSSQL.value
    use_pymssql: bool = False
    use_pyodbc: bool = False
    uri_string: str = ""
    duration: Optional[int]

    def get_connection_url(self):
        if self.use_pyodbc:
            self.scheme = "mssql+pyodbc"
            return f"{self.scheme}://{self.uri_string}"
        if self.use_pymssql:
            self.scheme = "mssql+pymssql"
        return super().get_connection_url()


class MssqlSource(SQLSource):
    """MSSQL Source class

    Args:
        config:
        metadata_config:
        ctx
    """

    @classmethod
    def create(cls, config_dict, metadata_config_dict, ctx):
        """Create class instance"""
        config = MssqlConfig.parse_obj(config_dict)
        metadata_config = MetadataServerConfig.parse_obj(metadata_config_dict)
        return cls(config, metadata_config, ctx)
