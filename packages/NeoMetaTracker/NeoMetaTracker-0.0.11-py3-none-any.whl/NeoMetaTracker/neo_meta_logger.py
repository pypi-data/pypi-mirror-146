from typing import Union, Dict, List, Generic
import time
import py2neo
from pathlib import Path
from NeoMetaTracker.capture_point import CapturePoint
from NeoMetaTracker.graph_scheme import GraphSchema
from NeoMetaTracker.visualizer._base_visualizer import BaseVisualizer


class NeoMetaTracker:
    def __init__(self, connection: Union[py2neo.Graph, Dict]):
        self.capture_points: List[CapturePoint] = []
        self.all_schema_nodes: Dict[tuple, py2neo.Node] = None
        self.all_schema_rels: Dict[str, py2neo.Relationship] = None
        self.ignore_labels: List[str] = []
        self.ignore_reliations_types: List[str] = []
        # by zero changes we mean, changes where the node count did not change. e.g. if we create an index for label "myLabel" we also detect a schema change for Label "myLabel"
        # this can be undesirable in some situations. to ignore such changes set `ignore_zero_changes` to True
        self.ignore_zero_changes: bool = False
        if isinstance(connection, dict):
            self.graph: py2neo.Graph = py2neo.Graph(**connection)
        elif isinstance(connection, py2neo.Graph):
            self.graph = connection
        else:
            raise TypeError(
                f"Expected 'py2neo.Graph' or 'dict'. Got '{type(connection)}'"
            )

    def capture(self, name: str = None):
        labels_count = self._get_labels_count()
        relations_count = self._get_relations_count()

        self.capture_points.append(
            CapturePoint(
                name=name,
                parent_logger=self,
                labels_count=labels_count,
                relations_count=relations_count,
                neo4j_schema_vis_data=self._get_neo4j_schema(),
            )
        )

    def node_filter_func(self, node: py2neo.Node):
        """This function can be overiden to filter specifics nodes out of the schema tracker

        example; Remove all schema-nodes with label starting with "_":
            mlog = NeoMetaTracker(test_graph)

            def node_filter(node: py2neo.Node):
                node_label = list(node.labels)[0]
                if node_label.startswith("_") or node_label in self.ignore_labels:
                    return None
                return node

            mlog.node_filter_func = node_filter

        """
        if list(node.labels)[0] in self.ignore_labels:
            return None
        return node

    def rel_filter_func(self, rel: py2neo.Relationship):
        """This function can be overiden to filter specifics nodes out of the schema tracker

        example; Remove all schema-nodes with label starting with "_":
            mlog = NeoMetaTracker(test_graph)

            def my_filter_func(self, rel: py2neo.Relationship):
                if type(rel).__name__.startwith("_") or type(rel).__name__ in self.ignore_reliations_types:
                    return None
            return rel

            mlog.rel_filter_func = my_filter_func

        """
        if type(rel).__name__ in self.ignore_reliations_types:
            return None
        return rel

    def visualize(
        self, visualizer_class: BaseVisualizer, to_file: Union[str, Path] = None
    ):
        schemas_changes = []
        for index, to_cp in enumerate(self.capture_points):
            if index < 1:
                continue
            from_cp = self.capture_points[index - 1]
            changes = self.get_schemagraph_changes(
                from_capture=from_cp, to_capture=to_cp
            )
            changes.parent_capture_point = to_cp
            schemas_changes.append(changes)
        visualizer: BaseVisualizer = visualizer_class(schemas_changes)
        if to_file:
            visualizer.generate_file(to_file)
        else:
            return visualizer.generate_object()

    def _get_neo4j_schema(self):
        # call db.schema.visualization
        return self.graph.run(
            "call db.schema.visualization yield nodes, relationships"
        ).data()[0]

    def _get_labels_count(self) -> Dict[str, int]:
        all_labels: List[str] = self.graph.run(
            "CALL db.labels() yield label return collect(label) as res"
        ).data()[0]["res"]
        labels_count: Dict[str, int] = {}
        for label in all_labels:
            if label in self.ignore_labels:
                continue
            query_label_count = f"""
                    MATCH (n:{label})
                    RETURN count(n) AS res
                    """
            res = self.graph.run(query_label_count).data()[0]["res"]
            if (self.ignore_zero_changes and res != 0) or not self.ignore_zero_changes:
                labels_count[label] = res
        return labels_count

    def _get_relations_count(self) -> Dict[str, int]:
        all_rels: List[str] = self.graph.run(
            "CALL db.relationshipTypes() yield relationshipType return collect(relationshipType) as res"
        ).data()[0]["res"]
        rels_count: Dict[str, int] = {}
        for rel in all_rels:
            if rel in self.ignore_reliations_types:
                continue
            query_rel_count = f"""
                    MATCH ()-[:{rel}]->() 
                    return count(*) AS res
                    """
            res = self.graph.run(query_rel_count).data()[0]["res"]
            if (self.ignore_zero_changes and res != 0) or not self.ignore_zero_changes:
                rels_count[rel] = res
        return rels_count

    def get_capture_point_by(
        self,
        capture_point_index: int = None,
        capture_point_time: float = None,
        capture_point_name: str = None,
    ):
        if capture_point_time:
            return next(
                cp for cp in self.capture_points if capture_point_time == cp.timestamp
            )
        elif capture_point_index:
            return self.capture_points[capture_point_index]
        elif capture_point_name:
            return next(
                cp for cp in self.capture_points if capture_point_name == cp.name
            )

    def get_schemagraph_last_changes(self) -> GraphSchema:
        return self.get_schemagraph_changes_since(
            self.get_capture_point_by(capture_point_index=-2)
        )

    def get_schemagraph_changes_since(
        self,
        capture_point: CapturePoint = None,
    ) -> GraphSchema:
        current_capture_point: CapturePoint = (
            self.capture_points[-1] if self.capture_points else None
        )
        return self.get_schemagraph_changes(
            from_capture=capture_point, to_capture=current_capture_point
        )

    def get_schemagraph_changes(
        self, from_capture: CapturePoint, to_capture: CapturePoint
    ) -> GraphSchema:
        # hardcoded class name in subgraph. we need to workaround this. can be removed with https://github.com/py2neo-org/py2neo/issues/940 merged
        # original line: return from_capture.schema - to_capture.schema
        # workaround:
        sb: py2neo.Subgraph = to_capture.schema - from_capture.schema
        return GraphSchema(nodes=sb.nodes, relationships=sb.relationships)

    def get_numeric_last_changes(self) -> Dict[str, Dict[str, int]]:
        """Get changes, in terms of quantity, of labels and relations since the last capture compared to the current capture

        Returns:
            Dict[str,Dict[str,int]]: A base dictonary "{'labels':{...},'relation':{...}}" containing two dictoniries listing changes (in terms of quantity) for labels and relations.
        """
        return self.get_numeric_changes_since(
            self.get_capture_point_by(capture_point_index=-2)
        )

    def get_numeric_changes_since(
        self,
        capture_point: CapturePoint = None,
    ) -> Dict[str, Dict[str, int]]:
        """Get changes, in terms of quantity, of labels and relations since the last capture compared to the current capture

        Returns:
            Dict[str,Dict[str,int]]: A base dictonary "{'labels':{...},'relation':{...}}" containing two dictoniries listing changes (in terms of quantity) for labels and relations.
        """
        current_capture_point: CapturePoint = (
            self.capture_points[-1] if self.capture_points else None
        )
        return self.get_numeric_changes(
            from_capture=capture_point, to_capture=current_capture_point
        )

    def get_numeric_changes(
        self,
        from_capture: CapturePoint,
        to_capture: CapturePoint,
        ignore_zeros: bool = None,
    ):
        if ignore_zeros is None:
            ignore_zeros = self.ignore_zero_changes
        if len(self.capture_points) <= 1:
            raise ValueError(
                f"You need at least 2 capture points to compare any changes. Got only {len(self.capture_points)} points"
            )
        # Compare labels
        result: Dict = {"labels": {}, "relations": {}}
        if to_capture.labels_count or from_capture.labels_count:
            diff_labels = set(to_capture.labels_count.items()) ^ set(
                from_capture.labels_count.items()
            )
            for diff_label in set([lbl[0] for lbl in diff_labels]):
                res = (
                    to_capture.labels_count[diff_label]
                    if diff_label in to_capture.labels_count
                    else 0
                ) - (
                    from_capture.labels_count[diff_label]
                    if diff_label in from_capture.labels_count
                    else 0
                )
                if (res != 0 and ignore_zeros) or not ignore_zeros:
                    result["labels"][diff_label] = res
        # Compare relations
        if not to_capture.relations_count and not from_capture.relations_count:
            return result
        diff_relations = set(to_capture.relations_count.items()) ^ set(
            from_capture.relations_count.items()
        )
        for diff_rel in set([lbl[0] for lbl in diff_relations]):
            res = (
                to_capture.relations_count[diff_rel]
                if diff_rel in to_capture.relations_count
                else 0
            ) - (
                from_capture.relations_count[diff_rel]
                if diff_rel in from_capture.relations_count
                else 0
            )
            if (res != 0 and ignore_zeros) or not ignore_zeros:
                result["relations"][diff_rel] = res
        return result
