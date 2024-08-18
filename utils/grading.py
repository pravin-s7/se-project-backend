from database.db import db
from utils.response import objectsEntity
from bson import ObjectId
from datetime import datetime, timezone

def get_course_data():
    return objectsEntity(db.course.find({}, {"course_id": 1}))

def get_registered_users(course_id):
    return objectsEntity(db.user.find({"courses": {"$in": [course_id]}}))

def get_assignments(course_id):
    return objectsEntity(db.assignment.find({"$and": [{"course_id": course_id}, {"assgn_type": "GA"}]}))

def get_coding_assignments(course_id):
    return objectsEntity(db.coding_assignment.find({"$and": [{"course_id": course_id}, {"assgn_type": "GrPA"}]}))

def evaluate_assignment(assignment, course_registered_users):
    if not assignment['evaluated'] and datetime.now(timezone.utc) > datetime(assignment['deadline']):
        for user in course_registered_users:
            user_id = user['user_id']
            submission = db.submission.find_one({"user_id": user_id, "assgn_id": ObjectId(assignment['_id'])})
            mark = 0
            if submission and submission['answer'] == assignment['answers']:
                mark = 1
            db.assignment_mark.insert_one({"user_id": user_id, "assgn_id": ObjectId(assignment['_id']), "mark": mark})
        db.assignment.update_one({"_id": ObjectId(assignment['_id'])}, {"$set": {"evaluated": True}})

def evaluate_coding_assignment(coding_assignment, course_registered_users):
    if not coding_assignment['evaluated'] and datetime.now(timezone.utc) > datetime(coding_assignment['deadline']):
        private_test_cases = [testcase['output'] for testcase in coding_assignment['private_testcase']]
        for user in course_registered_users:
            user_id = user['user_id']
            coding_submission = db.submission.find_one({"user_id": user_id, "assgn_id": ObjectId(coding_assignment['_id'])})
            mark = 0
            if coding_submission and coding_submission['answer'] == private_test_cases:
                mark = 1
            db.assignment_mark.insert_one({"user_id": user_id, "assgn_id": ObjectId(coding_assignment['_id']), "mark": mark})
        db.coding_assignment.update_one({"_id": ObjectId(coding_assignment['_id'])}, {"$set": {"evaluated": True}})

def update_course_marks():
    courses = get_course_data()
    for course in courses:
        course_id = course['course_id']
        for week in range(1, 13):
            process_assignments(course_id, week, "GA")
            process_assignments(course_id, week, "GrPA")

def process_assignments(course_id, week, assignment_type):
    users_submissions = aggregate_submissions(course_id, week, assignment_type)
    for submission in users_submissions:
        marks = calculate_marks(submission, course_id, week, assignment_type)
        db.marks.insert_one(marks)

def aggregate_submissions(course_id, week, assignment_type):
    return objectsEntity(db.assignment_mark.aggregate([
        {
            "$lookup": {
                "from": "assignment" if assignment_type == "GA" else "coding_assignment",
                "localField": "assgn_id",
                "foreignField": "_id",
                "as": "assignment_submission"
            }
        },
        {"$unwind": "$assignment_submission"},
        {"$match": {"assignment_submission.assgn_type": assignment_type, "assignment_submission.course_id": course_id, "assignment_submission.week": week}},
        {"$group": {
            "_id": {"user_id": "$user_id", "week": "$assignment_submission.week"},
            "totalAssignments": {"$sum": 1},
            "evaluatedAssignments": {"$sum": {"$cond": [{"$ifNull": ["$assignment_submission.evaluated", False]}, 1, 0]}},
            "all_assignment_marks": {"$push": "$$ROOT"}
        }},
        {"$match": {"$expr": {"$eq": ["$totalAssignments", "$evaluatedAssignments"]}}},
        {"$project": {
            "_id": 0,
            "user_id": "$_id.user_id",
            "all_assignment_marks": {"$map": {"input": "$all_assignment_marks", "as": "mark", "in": {"assgn_id": "$$mark.assgn_id", "user_id": "$$mark.user_id", "mark": "$$mark.mark", "assignment_submission": "$$mark.assignment_submission"}}}
        }},
        {"$group": {"_id": "$user_id", "all_assignment_marks": {"$push": {"$arrayElemAt": ["$all_assignment_marks", 0]}}}}
    ]))

def calculate_marks(submission, course_id, week, assignment_type):
    mark, total_mark = 0, len(submission['all_assignment_marks'])
    for assignment in submission['all_assignment_marks']:
        mark += assignment['mark']
    return {
        'user_id': submission['_id'],
        'course_id': course_id,
        'week': week,
        'assgn_type': assignment_type,
        'mark': round((mark / total_mark) * 100, 0)
    }

def grade_assignment():
    courses = get_course_data()
    for course in courses:
        course_id = course['course_id']
        course_registered_users = get_registered_users(course_id)
        assignments = get_assignments(course_id)
        coding_assignments = get_coding_assignments(course_id)

        for assignment in assignments:
            evaluate_assignment(assignment, course_registered_users)
        
        for coding_assignment in coding_assignments:
            evaluate_coding_assignment(coding_assignment, course_registered_users)

    update_course_marks()
    return "Marks Updated Successfully"