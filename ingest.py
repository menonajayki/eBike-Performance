from neo4j import GraphDatabase
import pandas as pd

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "arena2036"))

def ingest_rubber_shim_data(tx, shim_id, diameter, month, screw_params, handlebar_width):
    query = """
    CREATE (r:RubberShim {
        ShimID: $shim_id, 
        Diameter: $diameter, 
        ProductionMonth: $month, 
        ScrewParams: $screw_params, 
        HandlebarWidth: $handlebar_width
    })
    """
    tx.run(query, shim_id=shim_id, diameter=diameter, month=month, screw_params=screw_params, handlebar_width=handlebar_width)

def ingest_feedback_data(tx, shim_id, feedback, breakage):
    query = """
    MATCH (r:RubberShim {ShimID: $shim_id})
    CREATE (f:Feedback {
        Feedback: $feedback, 
        Breakage: $breakage
    })-[:FEEDBACK_ON]->(r)
    """
    tx.run(query, shim_id=shim_id, feedback=feedback, breakage=breakage)

def ingest_data_to_neo4j():
    # CSV files
    rubber_shim_data = pd.read_csv('rubber_shim_data.csv')
    feedback_data = pd.read_csv('customer_feedback_data.csv')

    # rubber shim data
    with driver.session() as session:
        for index, row in rubber_shim_data.iterrows():
            session.write_transaction(ingest_rubber_shim_data, row['ShimID'], row['Diameter (mm)'], row['Production Month'], row['Screw Parameters'], row['Handlebar Width (mm)'])

    # feedback data
    with driver.session() as session:
        for index, row in feedback_data.iterrows():
            session.write_transaction(ingest_feedback_data, row['ShimID'], row['Customer Feedback'], row['Breakage (Yes/No)'])

# ingestion
ingest_data_to_neo4j()

print("Data ingestion to Neo4j completed.")
