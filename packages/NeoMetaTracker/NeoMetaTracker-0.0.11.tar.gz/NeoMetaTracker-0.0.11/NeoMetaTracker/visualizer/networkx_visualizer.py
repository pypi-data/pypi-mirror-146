from py2neo import Subgraph
import networkx
from NeoMetaTracker.visualizer._base_visualizer import BaseVisualizer
import matplotlib.pyplot as plt


# WIP: not usable atm


class NetworkxVisualizer:
    def create_schema_png(self):
        nx_graph = self._py2neo_subgraph_to_networkxgraph(
            py2neo_subgraph=self.neo_meta_logger.capture_points[0].schema
        )

    def _py2neo_subgraph_to_networkxgraph(
        self,
        py2neo_subgraph: Subgraph,
    ) -> networkx.MultiDiGraph:
        nx_graph: networkx.MultiDiGraph = networkx.MultiDiGraph()
        for node in py2neo_subgraph.nodes:
            nx_graph.add_node(
                node["__label_name"],
                labels=list[node.labels],
                properties=dict(node),
            )
        for rel in py2neo_subgraph.relationships:
            nx_graph.add_edge(
                rel.start_node["__label_name"],
                rel.end_node["__label_name"],
                key=rel.type,
                type=rel.type,
                properties=dict(rel),
            )
        return nx_graph
