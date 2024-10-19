# app.py

from flask import Flask, request, jsonify
from rule_engine import create_rule, evaluate_rule  
from models import Rule, init_db  
from werkzeug.urls import quote  

app = Flask(__name__)
session = init_db()  

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Rule Engine API!"})  

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.json.get('rule') 
    if not rule_string:
        return jsonify({"error": "Rule string is required"}), 400  

    rule_ast = create_rule(rule_string)  
    new_rule = Rule(name=f"Rule {rule_string[:10]}...", rule_string=rule_string)  
    session.add(new_rule) 
    session.commit()  

    return jsonify({"message": "Rule created", "ast": str(rule_ast)}), 201  

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    rule_id = request.json.get('rule_id')  
    user_data = request.json.get('data')  

    if rule_id is None or user_data is None:
        return jsonify({"error": "Rule ID and user data are required"}), 400  

    rule = session.query(Rule).filter_by(id=rule_id).first()  
    if not rule:
        return jsonify({"error": "Rule not found"}), 404  

    rule_ast = create_rule(rule.rule_string)  
    result = evaluate_rule(rule_ast, user_data)  

    return jsonify({"result": result}), 200  

if __name__ == '__main__':
    app.run(debug=True)  
