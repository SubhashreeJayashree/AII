def dfs_maze(graph, start, goal, visited=None):
    if visited is None:
        visited = set()

    if start == goal:
        return True

    visited.add(start)

    for neighbor in graph[start]:
        if neighbor not in visited:
            if dfs_maze(graph, neighbor, goal, visited):
                return True

    return False

# Maze structure
maze = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': [],
    'E': ['F'],
    'F': []
}

result = dfs_maze(maze, 'A', 'F')
print("Path Exists:", result)
