from neo4j import GraphDatabase
import pandas as pd
import csv

# Neo4j connection setup
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "arena2036"))

# Functions to create eBike nodes, components, and metrics
def create_ebike(tx, ebike_id):
    query = "CREATE (e:EBike {id: $ebike_id}) RETURN e"
    tx.run(query, ebike_id=ebike_id)

def create_component(tx, ebike_id, component_id, component_type, manufacturer, last_maintenance):
    query = (
        "MATCH (e:EBike {id: $ebike_id}) "
        "CREATE (c:Component {id: $component_id, type: $component_type, manufacturer: $manufacturer, lastMaintenance: $last_maintenance}) "
        "MERGE (e)-[:HAS_COMPONENT]->(c) RETURN e, c"
    )
    tx.run(query, ebike_id=ebike_id, component_id=component_id, component_type=component_type, manufacturer=manufacturer, last_maintenance=last_maintenance)

def create_metric(tx, component_id, metric, value, threshold, timestamp):
    query = (
        "MATCH (c:Component {id: $component_id}) "
        "CREATE (m:Metric {metric: $metric, value: $value, threshold: $threshold, timestamp: $timestamp}) "
        "MERGE (c)-[:HAS_METRIC]->(m) RETURN c, m"
    )
    tx.run(query, component_id=component_id, metric=metric, value=value, threshold=threshold, timestamp=timestamp)

# Load sample eBike and component data from CSV
def load_ebike_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        with driver.session() as session:
            for row in reader:
                session.write_transaction(create_ebike, row['eBikeID'])
                session.write_transaction(
                    create_component, row['eBikeID'], row['ComponentID'], row['ComponentType'],
                    row['Manufacturer'], row['LastMaintenanceDate']
                )

def load_performance_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        with driver.session() as session:
            for row in reader:
                session.write_transaction(
                    create_metric, row['ComponentID'], row['Metric'], row['Value'], row['Threshold'], row['Timestamp']
                )

# Load data from CSV
load_ebike_data("ebike_components.csv")
load_performance_data("performance_metrics.csv")
