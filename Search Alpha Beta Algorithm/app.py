# ---------------------------------------------
# Import required libraries
# ---------------------------------------------
import streamlit as st              # For web application UI
import numpy as np                  # For numerical operations
import pandas as pd                 # For tabular data handling
import networkx as nx               # For game tree visualization
import matplotlib.pyplot as plt     # For plotting graphs

# ---------------------------------------------
# Configure Streamlit page settings
# ---------------------------------------------
st.set_page_config(
    page_title="Alpha-Beta Cutoffs",
    page_icon="♟️",
    layout="wide"
)

# ---------------------------------------------
# Application title and description
# ---------------------------------------------
st.title("♟️ Alpha–Beta Search with Cutoffs")
st.write("This program demonstrates Alpha–Beta Pruning with explicit cutoffs.")

# ---------------------------------------------
# Global variables to track nodes and cutoffs
# ---------------------------------------------
visited_nodes = []   # Stores visited nodes during search
cutoffs = []         # Stores alpha and beta cutoffs

# ---------------------------------------------
# Alpha–Beta Pruning algorithm function
# ---------------------------------------------
def alpha_beta(depth, index, is_max, values, alpha, beta):
    # Record the visited node
    visited_nodes.append(index)

    # If leaf node is reached, return its value
    if depth == 0:
        return values[index]

    # Maximizing player logic
    if is_max:
        best = -np.inf
        for i in range(2):  # Binary tree
            value = alpha_beta(
                depth - 1,
                index * 2 + i,
                False,
                values,
                alpha,
                beta
            )
            best = max(best, value)
            alpha = max(alpha, best)

            # Beta cutoff condition
            if beta <= alpha:
                cutoffs.append({"Node": index, "Cutoff": "Beta Cutoff"})
                break
        return best

    # Minimizing player logic
    else:
        best = np.inf
        for i in range(2):
            value = alpha_beta(
                depth - 1,
                index * 2 + i,
                True,
                values,
                alpha,
                beta
            )
            best = min(best, value)
            beta = min(beta, best)

            # Alpha cutoff condition
            if beta <= alpha:
                cutoffs.append({"Node": index, "Cutoff": "Alpha Cutoff"})
                break
        return best

# ---------------------------------------------
# Sidebar controls for user input
# ---------------------------------------------
st.sidebar.header("⚙️ Controls")
depth = st.sidebar.slider("Tree Depth", 2, 4, 3)

# ---------------------------------------------
# Generate random leaf node values
# ---------------------------------------------
leaf_count = 2 ** depth
np.random.seed(1)
values = np.random.randint(-10, 15, leaf_count)

# ---------------------------------------------
# Display leaf node values
# ---------------------------------------------
st.subheader("🍃 Leaf Node Values")
st.write(values)

# ---------------------------------------------
# Run Alpha–Beta algorithm
# ---------------------------------------------
visited_nodes.clear()
cutoffs.clear()

result = alpha_beta(
    depth=depth,
    index=0,
    is_max=True,
    values=values,
    alpha=-np.inf,
    beta=np.inf
)

# ---------------------------------------------
# Display optimal value
# ---------------------------------------------
st.success(f"🎯 Optimal Value: **{result}**")

# ---------------------------------------------
# Display statistics
# ---------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Leaf Nodes", leaf_count)
col2.metric("Visited Nodes", len(set(visited_nodes)))
col3.metric("Cutoffs", len(cutoffs))

# ---------------------------------------------
# Display cutoff details in table format
# ---------------------------------------------
st.subheader("✂️ Alpha–Beta Cutoffs")
if cutoffs:
    st.dataframe(pd.DataFrame(cutoffs))
else:
    st.info("No cutoffs occurred at this depth.")

# ---------------------------------------------
# Build game tree for visualization
# ---------------------------------------------
st.subheader("🌳 Game Tree")

G = nx.DiGraph()

def build_tree(node, level):
    if level == depth:
        return
    for i in range(2):
        child = node * 2 + i + 1
        G.add_edge(node, child)
        build_tree(child, level + 1)

build_tree(0, 0)

# ---------------------------------------------
# Generate safe layout (no Graphviz dependency)
# ---------------------------------------------
pos = nx.spring_layout(G, seed=42)

# ---------------------------------------------
# Draw the game tree
# ---------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=1400,
    node_color="lightgreen",
    ax=ax
)
st.pyplot(fig)

# ---------------------------------------------
# Explanation section
# ---------------------------------------------
st.subheader("📘 Explanation of Alpha–Beta Cutoffs")
st.markdown("""
- **Alpha (α)** represents the best value for the maximizing player  
- **Beta (β)** represents the best value for the minimizing player  
- A **cutoff occurs when β ≤ α**  
- **Alpha cutoff** happens at minimizing nodes  
- **Beta cutoff** happens at maximizing nodes  
- Cutoffs reduce the number of nodes evaluated
""")

# ---------------------------------------------
# Footer
# ---------------------------------------------
st.markdown("---")
st.markdown("Alpha–Beta Search with Cutoffs | AI Algorithms Project ♟️")
