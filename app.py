# app.py

from flask import Flask, request, jsonify
from rule_engine import create_rule, evaluate_rule  # Ensure these functions are implemented
from models import Rule, init_db  # Ensure the Rule model and init_db function are implemented
from werkzeug.urls import quote  # Note: You may need to adjust this import based on your usage

app = Flask(__name__)
session = init_db()  # Initialize the database session

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Rule Engine API!"})  # Basic route for root URL

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.json.get('rule')  # Using .get() to avoid KeyError
    if not rule_string:
        return jsonify({"error": "Rule string is required"}), 400  # Return error if rule_string is missing

    rule_ast = create_rule(rule_string)  # Create AST from rule string
    new_rule = Rule(name=f"Rule {rule_string[:10]}...", rule_string=rule_string)  # Create a new Rule object
    session.add(new_rule)  # Add new rule to the session
    session.commit()  # Commit the session to save the new rule

    return jsonify({"message": "Rule created", "ast": str(rule_ast)}), 201  # Return success message and AST

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    rule_id = request.json.get('rule_id')  # Using .get() to avoid KeyError
    user_data = request.json.get('data')  # Ensure user data is provided

    if rule_id is None or user_data is None:
        return jsonify({"error": "Rule ID and user data are required"}), 400  # Return error if inputs are missing

    rule = session.query(Rule).filter_by(id=rule_id).first()  # Query for the rule by ID
    if not rule:
        return jsonify({"error": "Rule not found"}), 404  # Return error if rule not found

    rule_ast = create_rule(rule.rule_string)  # Create AST from the stored rule string
    result = evaluate_rule(rule_ast, user_data)  # Evaluate the rule against the user data

    return jsonify({"result": result}), 200  # Return the evaluation result

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask development server
