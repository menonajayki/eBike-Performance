from neo4j import GraphDatabase
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Neo4j connection setup
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "arena2036"))


def get_performance_data():
    query = "MATCH (m:Metric) RETURN m.metric AS metric, m.value AS value, m.threshold AS threshold"
    with driver.session() as session:
        result = session.run(query)
        data = []
        for record in result:
            data.append([record['metric'], record['value'], record['threshold']])
        return data


def predict_maintenance(value, threshold):
    # Get data for training
    data = get_performance_data()
    df = pd.DataFrame(data, columns=["metric", "value", "threshold"])
    df['needs_maintenance'] = df['value'] < df['threshold']

    # Prepare data for AI model
    X = df[['value', 'threshold']]
    y = df['needs_maintenance']

    # Train a decision tree classifier
    model = DecisionTreeClassifier()
    model.fit(X, y)

    # Predict maintenance need
    return model.predict([[value, threshold]])[0]
