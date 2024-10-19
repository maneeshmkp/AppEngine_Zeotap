# rule_engine.py

import re
from ast_node import Node

def create_rule(rule_string):
    """
    Parse a rule string and convert it into an AST.
    
    :param rule_string: A string representing the rule (e.g., "(age > 30 AND department = 'Sales') OR (age < 25)")
    :return: The root node of the generated AST.
    """
    tokens = re.split(r'(\(|\)|AND|OR)', rule_string.replace(' ', ''))
    tokens = [token for token in tokens if token]  # Filter out empty strings

    def parse_expression(tokens):
        stack = []
        while tokens:
            token = tokens.pop(0)
            if token == '(':
                stack.append(parse_expression(tokens))
            elif token == ')':
                break
            elif token in ('AND', 'OR'):
                operator = Node('operator', stack.pop(), None, token)
                operator.right = parse_expression(tokens)
                stack.append(operator)
            else:
                # Create operand (a condition)
                stack.append(Node('operand', value=token))
        return stack[0]

    return parse_expression(tokens)

def combine_rules(rules, operator="AND"):
    """
    Combine multiple rules into a single AST.
    
    :param rules: A list of rule strings.
    :param operator: The operator to use for combination (AND/OR).
    :return: The combined AST.
    """
    combined_ast = create_rule(rules[0])
    for rule in rules[1:]:
        new_rule_ast = create_rule(rule)
        combined_ast = Node('operator', combined_ast, new_rule_ast, operator)
    return combined_ast

def evaluate_rule(ast, data):
    """
    Evaluate an AST against a given set of user data.
    
    :param ast: The AST representing the rule.
    :param data: A dictionary containing user attributes (e.g., {"age": 35, "department": "Sales"}).
    :return: True if the rule is satisfied, False otherwise.
    """
    if ast.type == 'operand':
        condition = ast.value
        field, op, value = re.split(r'(>=|<=|=|>|<)', condition)
        field = field.strip()
        value = value.strip().strip("'")
        data_value = str(data.get(field, ''))

        if op == '>':
            return int(data_value) > int(value)
        elif op == '<':
            return int(data_value) < int(value)
        elif op == '=':
            return data_value == value

    elif ast.type == 'operator':
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result

    return False
