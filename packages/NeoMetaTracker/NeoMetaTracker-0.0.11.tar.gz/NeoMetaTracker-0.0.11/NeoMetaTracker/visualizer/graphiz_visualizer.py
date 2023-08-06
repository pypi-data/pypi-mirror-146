from __future__ import annotations
from typing import List, TYPE_CHECKING

import py2neo
from NeoMetaTracker.visualizer._base_visualizer import BaseVisualizer

if TYPE_CHECKING:
    from NeoMetaTracker.graph_scheme import GraphSchema

# sudo apt-get install graphviz graphviz-dev
# pip install pygraphviz
import pygraphviz as pgv


class GraphvizVisualizer(BaseVisualizer):
    def generate_file(self, path):
        self._py2neo_subgraph_to_graphviz(
            neometatracker_graphschemas=self.neo_meta_logger_graph_schemas
        ).write(path)

    def generate_object(self) -> bytes:
        return (
            self._py2neo_subgraph_to_graphviz(
                neometatracker_graphschemas=self.neo_meta_logger_graph_schemas
            )
            .string()
            .encode("utf-8")
        )

    def _py2neo_subgraph_to_graphviz(
        self,
        neometatracker_graphschemas: List[GraphSchema],
    ) -> pgv.AGraph:
        # https://pygraphviz.github.io/documentation/stable/tutorial.html#graphs
        graph: pgv.AGraph = pgv.AGraph(strict=False, directed=True, landscape=False)
        node_track_list: List[py2neo.Node] = []
        for nmt_graphschema in neometatracker_graphschemas:
            if len(neometatracker_graphschemas) == 1:
                graphviz_subg = graph
            else:
                sb_name = (
                    nmt_graphschema.parent_capture_point.name
                    if nmt_graphschema.parent_capture_point.name
                    else ""
                )
                graphviz_subg = graph.add_subgraph(
                    name=sb_name,
                    label=sb_name,
                    cluster=True,
                    style="filled",
                    color="#E0E0E0",
                )
            for node in nmt_graphschema.nodes:
                if node not in node_track_list:
                    node_track_list.append(node)
                    graphviz_subg.add_node(node["__label_name"], **dict(node))

            for rel in nmt_graphschema.relationships:
                graph.add_edge(
                    rel.start_node["__label_name"],
                    rel.end_node["__label_name"],
                    fontsize=8,
                    minlen=2,
                    # key=type(rel).__name__,
                    label=type(rel).__name__ + "   ",
                )
        return graph
