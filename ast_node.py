# ast_node.py

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        """
        Initialize an AST Node.

        :param node_type: 'operator' for AND/OR, 'operand' for conditions
        :param left: Left child node (for operators)
        :param right: Right child node (for operators)
        :param value: The value (e.g., 'age > 30' for conditions or 'AND' for operators)
        """
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        if self.type == "operator":
            return f"({self.left} {self.value} {self.right})"
        return str(self.value)
