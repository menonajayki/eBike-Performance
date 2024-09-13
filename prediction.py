from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "arena2036"))


def get_rubber_shim_data():
    with driver.session() as session:
        query = """
        MATCH (r:RubberShim)
        RETURN r.Diameter AS diameter, r.ProductionMonth AS month, r.HandlebarWidth AS handlebar_width, r.ScrewParams AS screw_params
        """
        result = session.run(query)
        return [record for record in result]


def get_customer_feedback_data():
    with driver.session() as session:
        query = """
        MATCH (r:RubberShim)<-[:FEEDBACK_ON]-(f:Feedback)
        RETURN r.ScrewParams AS screw_params, f.Feedback AS feedback, f.Breakage AS breakage
        """
        result = session.run(query)
        return [record for record in result]


def predict_breakage(diameter, screw_params, handlebar_width):
    with driver.session() as session:
        breakage_risk = False
        if diameter < 42.0 or handlebar_width < 780:
            breakage_risk = True

    return breakage_risk
