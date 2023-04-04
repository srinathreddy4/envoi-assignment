from flask import Flask, jsonify, request

import requests

app = Flask(__name__)

consultants_url = 'http://localhost:8080/api/consultants'
assignments_url = 'http://localhost:8081/api/assignments'

# response_consultants = requests.get(consultants_url).json()
# response_assignments = requests.get(assignments_url).json()


@app.route('/matching_consultant', methods=['GET'])
def get_matching_consultant():

    response_consultants = requests.get(consultants_url).json()
    consultants_skills = {}

    for consultant in response_consultants:
        if not consultant['assigned']:
            consultants_skills[consultant['name']] = consultant['skills']

    assignment_name = request.args.get('assignment_name')

    assignment_skills = find_assignments_by_name(assignment_name)

    matching_consultant = find_consultant(assignment_skills, consultants_skills)

    return jsonify({'matching_consultant': matching_consultant})

def find_assignments_by_name(assignment_name: str):
    response_assignments = requests.get(assignments_url).json()
    for assignment in response_assignments:
        if assignment['name'] == assignment_name:
            return assignment['skills']
    return None

def find_consultant(assignment_skills, consultants_skills):
    for name, skills in consultants_skills.items():
        if set(assignment_skills).issubset(set(skills)):
            return name
        else:
            print("No match found")
    return None

# import pdb;
# pdb.set_trace()

if __name__ == '__main__':
    app.run(debug=True)
