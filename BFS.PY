import heapq
import random
from collections import deque

class Node:
    def __init__(self, state, parent=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.cost = cost  # g(n) -> Cost from start node to this node
        self.heuristic = heuristic  # h(n) -> Heuristic cost to goal
        
    def __lt__(self, other):
        """ For priority queue (A*) comparison based on f(n) = g(n) + h(n) """
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def breadth_first_search(start, goal, neighbors_fn):
    """BFS uses a queue (FIFO) and expands all nodes at the current depth level first."""
    frontier = deque([Node(start)])  # Initialize with the start node
    explored = set()  # Keep track of visited nodes
    
    while frontier:
        node = frontier.popleft()  # FIFO: dequeue the next node
        if node.state == goal:
            return reconstruct_path(node)
        
        explored.add(node.state)
        
        for neighbor in neighbors_fn(node.state):
            if neighbor not in explored:
                frontier.append(Node(neighbor, node))
    return None  # Return None if no path is found

def a_star_search(start, goal, neighbors_fn, heuristic_fn):
    """A* uses a priority queue (min-heap) based on f(n) = g(n) + h(n)."""
    frontier = []
    heapq.heappush(frontier, Node(start, heuristic=heuristic_fn(start, goal)))
    explored = set()
    
    while frontier:
        node = heapq.heappop(frontier)  # Get the node with the lowest f(n)
        
        if node.state == goal:
            return reconstruct_path(node)
        
        explored.add(node.state)
        
        for neighbor in neighbors_fn(node.state):
            if neighbor not in explored:
                new_cost = node.cost + 1  # Assuming uniform step cost
                heapq.heappush(frontier, Node(neighbor, node, new_cost, heuristic_fn(neighbor, goal)))
    return None  # Return None if no path is found

def reconstruct_path(node):
    """Reconstruct the path by following parent nodes."""
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]  # Return reversed path (from start to goal)

def combined_search(start, goal, neighbors_fn, heuristic_fn):
    """
    Combined search that alternates between BFS and A*.
    It has a 40% chance to switch to A* on each step.
    """
    # Start with BFS as default
    current_algorithm = 'BFS'
    
    if random.random() <= 0.4:
        current_algorithm = 'A*'

    if current_algorithm == 'BFS':
        return breadth_first_search(start, goal, neighbors_fn)
    else:
        return a_star_search(start, goal, neighbors_fn, heuristic_fn)

# Heuristic function (example for grid-based problems like pathfinding)
def heuristic_fn(node, goal):
    # Example heuristic: Manhattan distance (assuming grid-like structure)
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# Neighbors function (example for grid-based problems)
def neighbors_fn(node):
    # Example: grid movement (up, down, left, right)
    x, y = node
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

# Example usage:
start = (0, 0)
goal = (2, 2)

# Perform the combined search with a 40% chance of switching to A*
path = combined_search(start, goal, neighbors_fn, heuristic_fn)

path
