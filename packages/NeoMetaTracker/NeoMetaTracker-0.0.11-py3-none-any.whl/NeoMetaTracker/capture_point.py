from __future__ import annotations
from typing import Dict, TYPE_CHECKING
from NeoMetaTracker.graph_scheme import GraphSchema
import time

if TYPE_CHECKING:
    from NeoMetaTracker.neo_meta_logger import NeoMetaTracker


class CapturePoint:
    """The state of a Neo4j database in terms of relationship and node count at a certain time"""

    def __init__(
        self,
        parent_logger: NeoMetaTracker,
        name: str,
        labels_count: Dict[str, int],
        relations_count: Dict[str, int],
        neo4j_schema_vis_data: Dict,
    ):
        self.parent_logger = parent_logger
        self.name = name
        self.timestamp: float = time.time()
        self.labels_count = labels_count
        self.relations_count = relations_count
        self.schema: GraphSchema = GraphSchema.from_neo4j_schema_vis_data(
            neo4j_schema_vis_data,
            parent_capture_point=self,
            extra_props={"capture_name": name} if name else {},
        )

    def __hash__(self):
        return hash(self.timestamp)

    def __eq__(self, other: "CapturePoint") -> bool:
        return type(other) is type(self) and self.timestamp == other.timestamp
