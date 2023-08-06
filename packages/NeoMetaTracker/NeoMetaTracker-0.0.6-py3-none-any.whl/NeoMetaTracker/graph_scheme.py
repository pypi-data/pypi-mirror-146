from __future__ import annotations
from typing import Union, List, Dict, Generic, TYPE_CHECKING

from bleach import clean

if TYPE_CHECKING:
    from NeoMetaTracker.capture_point import CapturePoint
from pathlib import Path
import py2neo

from NeoMetaTracker.visualizer._base_visualizer import BaseVisualizer


class GraphSchema(py2neo.Subgraph):
    parent_capture_point: CapturePoint

    def visualize(
        self,
        visualizer_class: BaseVisualizer,
        to_file: Union[Path, str] = None,
    ):
        visualizer: BaseVisualizer = visualizer_class(self)
        if to_file:
            visualizer.generate_file(to_file)
        else:
            return visualizer.generate_object()

    @classmethod
    def from_neo4j_schema_vis_data(
        cls,
        neo4j_schema_vis_data: Dict[str, List[Union[py2neo.Node, py2neo.Relationship]]],
        parent_capture_point: CapturePoint,
        extra_props: Dict = None,
    ) -> "GraphSchema":
        # ToDo: Break this function down. Too complex/spaghetti!

        # the nodes are bound atm. meaning they belong to a certain DB. we need to unbound them.
        # we clean the nodes and relationship from Neo4j's `call db.schema.visualization` from IDs (the IDs are random anyway on every call and consequently worthless outside of the own transaction)
        # We connect the nodes and relationships into a py2neo.Subgraph
        # store that in an instance of GraphSchema
        schema_graph: GraphSchema = cls()
        if not parent_capture_point.parent_logger.all_schema_nodes:
            parent_capture_point.parent_logger.all_schema_nodes = {}
        if not parent_capture_point.parent_logger.all_schema_rels:
            parent_capture_point.parent_logger.all_schema_rels = {}
        if not extra_props:
            extra_props = {}
        extra_props = extra_props | {"__neo_meta_logger_node": True}
        # copy all nodes to track if they are involed in a relation
        nodes_without_relation = list(neo4j_schema_vis_data["nodes"])
        for rel in neo4j_schema_vis_data["relationships"]:

            rel_nodes = [None, None]
            for node in neo4j_schema_vis_data["nodes"]:
                if rel_nodes[0] and rel_nodes[1]:
                    break
                if node.identity in [rel.start_node.identity, rel.end_node.identity]:
                    if node in nodes_without_relation:
                        nodes_without_relation.remove(node)
                    clean_rel_node = cls._get_or_create_unbound_schema_node(
                        node=node,
                        parent_capture_point=parent_capture_point,
                        extra_props=extra_props,
                    )
                    if clean_rel_node is None:
                        # the node was filterd out
                        continue
                    if rel.start_node.identity == rel.end_node.identity:
                        rel_nodes[0] = rel_nodes[1] = clean_rel_node
                    elif node.identity == rel.start_node.identity:
                        rel_nodes[0] = clean_rel_node
                    elif node.identity == rel.end_node.identity:
                        rel_nodes[1] = clean_rel_node
            rel_ident = f"{list(rel_nodes[0].labels)[0]}_{type(rel).__name__}_{list(rel_nodes[1].labels)[0]}"
            if rel_ident in parent_capture_point.parent_logger.all_schema_rels:
                clean_rel = parent_capture_point.parent_logger.all_schema_rels[
                    rel_ident
                ]
            else:
                parent_capture_point.parent_logger.all_schema_rels[
                    rel_ident
                ] = clean_rel = py2neo.Relationship(
                    rel_nodes[0],
                    type(rel).__name__,
                    rel_nodes[1],
                    **extra_props,
                )
            schema_graph = schema_graph | clean_rel

        # atm we ignored any nodes without any relation.
        # lets make up that leeway
        single_nodes_cleaned = []
        for node in nodes_without_relation:
            clean_node = cls._get_or_create_unbound_schema_node(
                node=node,
                parent_capture_point=parent_capture_point,
                extra_props=extra_props,
            )
            if clean_node is None:
                continue
            single_nodes_cleaned.append(
                cls._get_or_create_unbound_schema_node(
                    node=node,
                    parent_capture_point=parent_capture_point,
                    extra_props=extra_props,
                )
            )
        # hardcoded class name in subgraph. we need to workaround this. can be removed with https://github.com/py2neo-org/py2neo/issues/940 merged
        # original line: return schema_graph | cls(single_nodes_cleaned)

        # workaround:
        sb: py2neo.Subgraph = schema_graph | cls(single_nodes_cleaned)
        gs = GraphSchema(nodes=sb.nodes, relationships=sb.relationships)
        gs.parent_capture_point = parent_capture_point
        return gs

    @classmethod
    def _get_or_create_unbound_schema_node(
        cls,
        node: py2neo.Node,
        parent_capture_point: "CapturePoint",
        extra_props: Dict = None,
    ) -> py2neo.Node:
        if tuple(
            node.labels
        ) not in parent_capture_point.parent_logger.all_schema_nodes or (
            parent_capture_point.parent_logger.all_schema_nodes[tuple(node.labels)][
                "__node_count"
            ]
            != parent_capture_point.labels[tuple(node.labels)[0]]
        ):
            clean_node = py2neo.Node(
                *list(node.labels),
                **(
                    extra_props
                    | {
                        "__label_name": ":".join(list(node.labels)),
                        "__node_count": parent_capture_point.labels[
                            tuple(node.labels)[0]
                        ],
                    }
                ),
            )
            clean_node.__primarykey__ = "__label_name"
            clean_node.__primarylabel__ = list(node.labels)[0]
            if parent_capture_point.parent_logger.node_filter_func(clean_node):
                parent_capture_point.parent_logger.all_schema_nodes[
                    tuple(node.labels)
                ] = clean_node
            else:
                return None

        else:
            clean_node = parent_capture_point.parent_logger.all_schema_nodes[
                tuple(node.labels)
            ]
        return clean_node
