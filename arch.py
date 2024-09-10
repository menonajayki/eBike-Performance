import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes with labels
nodes = {
    "User's Web Browser": "User's Web Browser",
    'Flask App (app.py)': 'Flask App (app.py)',
    'get_performance_data()': 'get_performance_data()',
    'predict_maintenance()': 'predict_maintenance()',
    'Neo4j Database': 'Neo4j Database'
}

G.add_nodes_from(nodes.keys())

# Add edges with labels
edges = [
    ("User's Web Browser", 'Flask App (app.py)', 'Requests Data'),
    ('Flask App (app.py)', 'get_performance_data()', 'Data Retrieval'),
    ('Flask App (app.py)', 'predict_maintenance()', 'Predict Maintenance'),
    ('get_performance_data()', 'Neo4j Database', 'Query Data'),
    ('predict_maintenance()', 'Neo4j Database', 'Use Data')
]

G.add_edges_from((u, v) for u, v, _ in edges)

# Create labels for edges
edge_labels = {(u, v): label for u, v, label in edges}

# Draw the graph
pos = nx.spring_layout(G, seed=42)  # Fixed seed for reproducible layout

plt.figure(figsize=(14, 10))
nx.draw(
    G, pos,
    with_labels=True,
    node_size=3500,
    node_color='lightblue',
    font_size=12,
    font_weight='bold',
    edge_color='gray',
    linewidths=1,
    arrows=True,
    arrowsize=20
)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_color='red',
    font_size=10
)

plt.title('eBike System Architecture', fontsize=16, fontweight='bold')
plt.axis('off')  # Turn off the axis
plt.tight_layout()  # Adjust layout to fit into the figure area
plt.show()
