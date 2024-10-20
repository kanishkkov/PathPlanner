from flask import Flask, jsonify
import sqlite3
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Connect to the APCourses database and query data
@app.route('/api/apcourses', methods=['GET'])
def get_ap_courses():
    try:
        with sqlite3.connect('APCourses.sqlite') as connection:
            crsr = connection.cursor()
            crsr.execute("SELECT * FROM apcourses")
            ap_courses = crsr.fetchall()

            # Format the result as a list of dictionaries to return as JSON
            course_list = []
            for course in ap_courses:
                course_dict = {
                    'exam_name': course[0],
                    'min_score': course[1],
                    'num_credit': course[2],
                    'equiv_course': course[3]
                }
                course_list.append(course_dict)

            return jsonify(course_list)
    except sqlite3.OperationalError as e:
        return jsonify({"error": str(e)}), 500

# Connect to the CourseRec database and query data
@app.route('/api/courserec', methods=['GET'])
def get_course_recs():
    try:
        with sqlite3.connect('CourseRec.sqlite') as connection:
            crsr = connection.cursor()
            crsr.execute("SELECT * FROM courserec")
            course_recs = crsr.fetchall()

            # Format the result as a list of dictionaries to return as JSON
            course_list = []
            for course in course_recs:
                # Convert the PRERECS field (text) into an array
                prerecs_array = json.loads(course[5]) if course[5] else []

                course_dict = {
                    'id': course[0],
                    'subject': course[1],
                    'course_number': course[2],
                    'course_name': course[3],
                    'num_credit': course[4],
                    'prerequisites': prerecs_array
                }
                course_list.append(course_dict)

            return jsonify(course_list)
    except sqlite3.OperationalError as e:
        return jsonify({"error": str(e)}), 500
    

# Basic index route
@app.route('/')
def index():
    return "Welcome to the API! Use /api/apcourses or /api/courserec."

if __name__ == '__main__':
    app.run(debug=True)
