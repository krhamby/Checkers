class Node:
    def __init__(self, currentBoard, parent=None, children=[]):
        self.state = currentBoard
        self.parent = parent
        self.children = children
        self.heuristic = None