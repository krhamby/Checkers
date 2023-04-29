class Node:
    def __init__(self, currentBoard, parent=None, children=[]):
        self.state = currentBoard
        self.parent = parent
        self.children = children
        self.heuristic = 0
        
    def __str__(self) -> str:
        return f"Node: {self.state}" 