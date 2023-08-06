import sys
import os
from typing import Dict, List
import json
import py2neo
from DZDutils.neo4j import wait_for_db_boot

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))

from NeoMetaTracker import NeoMetaTracker
from NeoMetaTracker.visualizer import GraphvizVisualizer

NEO4J: Dict = json.loads(os.getenv("NEO4J", "{}"))
wait_for_db_boot(NEO4J)

current_dir = os.path.dirname(__file__)
graph = py2neo.Graph(**NEO4J)

graph.run("CREATE OR REPLACE DATABASE schematest")
graph.run("CREATE OR REPLACE DATABASE test")
test_graph = py2neo.Graph(**(NEO4J | {"name": "test"}))
# test_graph = py2neo.Graph(**(NEO4J))
mlog = NeoMetaTracker(test_graph)


def node_filter(node: py2neo.Node):
    if list(node.labels)[0].startswith("_"):
        return None
    return node


mlog.node_filter_func = node_filter

mlog.capture(name="Init")
test_graph.run("CREATE (:Alien {name: 'E.T.'})")
mlog.capture("AlienCluster")
test_graph.run("CREATE (:Human{name:'Amina Okujewa'})")
test_graph.run("CREATE (as:Human{name:'Aaron Swartz'})")
mlog.capture(name="HumansCluster")
test_graph.run("CREATE (:Cat{name:'Grumpy Cat'})")
test_graph.run("CREATE (:Pig{name:'Miss Piggy'})")
mlog.capture("AnimalCluster")
test_graph.run("CREATE (:World {name: 'Earth'})")
test_graph.run("CREATE (:World {name: 'Internet'})")
test_graph.run("CREATE (:World{name:'House'})")
mlog.capture("WorldCluster")
test_graph.run(
    "MATCH (wE:World{name:'Earth'}),(ao:Human{name:'Amina Okujewa'}) CREATE (ao)-[:LIVES_ON]->(wE)"
)
test_graph.run(
    "MATCH (wE:World{name:'Earth'}),(c:Cat{name:'Grumpy Cat'}) CREATE (c)-[:LIVES_ON]->(wE)"
)
test_graph.run(
    "MATCH (wI:World{name:'Internet'}),(wE:World{name:'Earth'}),(as:Human{name:'Aaron Swartz'}) CREATE (as)-[:LIVES_ON]->(wI), (as)-[:LIVES_ON]->(wE)"
)
test_graph.run(
    "MATCH (wI:World{name:'Internet'}),(wE:World{name:'Earth'}) CREATE (wI)-[:EXISTS_ON]->(wE)"
)
test_graph.run(
    "MATCH (wH:World{name:'House'}),(wE:World{name:'Earth'}) CREATE (wH)-[:EXISTS_ON]->(wE)"
)
test_graph.run(
    "MATCH (wH:World{name:'House'}),(wE:World{name:'Earth'}),(mp:Pig{name:'Miss Piggy'}) CREATE (mp)-[:LIVES_ON]->(wH),(mp)-[:LIVES_ON]->(wE)"
)
mlog.capture(name="RelationCluster")
test_graph.run("CREATE (:_SystemNode{name:'test'})")
mlog.capture()
print("###get_numeric_last_changes###\n", mlog.get_numeric_last_changes())
print("###get_schemagraph_last_changes###\n", mlog.get_schemagraph_last_changes())
print(
    "###schema.visualize(GraphvizVisualizer)###\n",
    mlog.capture_points[-1].schema.visualize(GraphvizVisualizer),
)
print(
    mlog.get_schemagraph_last_changes().visualize(
        GraphvizVisualizer, to_file=os.path.join(current_dir, "last_change.dot")
    )
)
print(mlog.visualize(GraphvizVisualizer, to_file=os.path.join(current_dir, "all.dot")))
schema_graph = py2neo.Graph(**(NEO4J | {"name": "schematest"}))
schema_graph.merge(mlog.get_schemagraph_last_changes())
