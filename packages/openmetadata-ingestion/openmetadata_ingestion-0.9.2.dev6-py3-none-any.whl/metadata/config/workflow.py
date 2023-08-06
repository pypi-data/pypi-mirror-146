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
Workflow related configurations and utilities
"""
import importlib
import logging
from typing import Type, TypeVar

from metadata.ingestion.api.common import DynamicTypedConfig, WorkflowContext
from metadata.ingestion.api.processor import Processor
from metadata.ingestion.api.sink import Sink
from metadata.ingestion.api.source import Source
from metadata.ingestion.ometa.openmetadata_rest import MetadataServerConfig

logger = logging.getLogger("Config")

T = TypeVar("T")


def fetch_type_class(_type: str, is_file: bool):
    """
    Helper function to build the path for
    dynamic imports
    """
    if is_file:
        return _type.replace("-", "_")
    else:
        return "".join([i.title() for i in _type.replace("-", "_").split("_")])


def get_class(key: str) -> Type[T]:
    """
    Given an import key, import the class and return it
    """
    if key.find(".") >= 0:
        # If the key contains a dot, we treat it as an import path and attempt
        # to load it dynamically.
        module_name, class_name = key.rsplit(".", 1)
        my_class = getattr(importlib.import_module(module_name), class_name)
        return my_class


def get_ingestion_source(
    source_type: str,
    context: WorkflowContext,
    source_config: DynamicTypedConfig,
    metadata_config: MetadataServerConfig,
) -> Source:
    """
    Import the required source class and configure it.

    :param source_type: Type specified in the config, e.g., redshift
    :param context: Workflow related information
    :param source_config: Specific source configurations, such as the host
    :param metadata_config: Metadata server configurations
    """

    source_class = get_class(
        "metadata.ingestion.source.{}.{}Source".format(
            fetch_type_class(source_type, is_file=True),
            fetch_type_class(source_type, is_file=False),
        )
    )
    source: Source = source_class.create(
        source_config.dict().get("config", {}), metadata_config, context
    )
    logger.debug(f"Source type:{source_type},{source_class} configured")

    source.prepare()
    logger.debug(f"Source type:{source_type},{source_class} prepared")

    return source


def get_sink(
    sink_type: str,
    context: WorkflowContext,
    sink_config: DynamicTypedConfig,
    metadata_config: MetadataServerConfig,
    _from: str = "ingestion",
) -> Sink:
    """
    Helps us to fetch and importing the sink class.

    By default, we will pick it up from `ingestion`.

    :param sink_type: Type specified in the config, e.g., metadata-rest
    :param context: Workflow related information
    :param sink_config: Specific sink configurations, such as the host
    :param metadata_config: Metadata server configurations
    :param _from: From where do we load the sink class. Ingestion by default.
    """
    sink_class = get_class(
        "metadata.{}.sink.{}.{}Sink".format(
            _from,
            fetch_type_class(sink_type, is_file=True),
            fetch_type_class(sink_type, is_file=False),
        )
    )

    sink: Sink = sink_class.create(
        sink_config.dict().get("config", {}), metadata_config, context
    )

    logger.debug(f"Sink type: {sink_type}, {sink_class} configured")

    return sink


def get_processor(
    processor_type: str,
    context: WorkflowContext,
    processor_config: DynamicTypedConfig,
    metadata_config: MetadataServerConfig,
    _from: str = "ingestion",
    **kwargs,
) -> Processor:
    """
    Helps us to fetch and import the Processor class.

    By default, we will pick it up from `ingestion`

    We allow to pass any other specific object we may require.
    E.g., for the ORM Profiler we need a Session to reach
    the source tables.

    :param processor_type: Type specified in the config, e.g., metadata-rest
    :param context: Workflow related information
    :param processor_config: Specific Processor configurations, such as the profiler and tests
    :param metadata_config: Metadata server configurations
    :param _from: From where do we load the sink class. Ingestion by default.
    """
    processor_class = get_class(
        "metadata.{}.processor.{}.{}Processor".format(
            _from,
            fetch_type_class(processor_type, is_file=True),
            fetch_type_class(processor_type, is_file=False),
        )
    )

    processor: Processor = processor_class.create(
        processor_config.dict().get("config", {}), metadata_config, context, **kwargs
    )

    logger.debug(f"Sink type: {processor_type}, {processor_class} configured")

    return processor
