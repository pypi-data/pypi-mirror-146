from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from NeoMetaTracker.graph_scheme import GraphSchema


class BaseVisualizer:
    def __init__(self, neo_meta_logger_graph_schemas: List[GraphSchema]):
        if not isinstance(neo_meta_logger_graph_schemas, list):
            self.neo_meta_logger_graph_schemas = [neo_meta_logger_graph_schemas]
        else:
            self.neo_meta_logger_graph_schemas = neo_meta_logger_graph_schemas

    def generate_file(self, path):
        raise NotImplementedError

    def generate_object(self) -> bytes:
        raise NotImplementedError
