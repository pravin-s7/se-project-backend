from fastapi import APIRouter, Security
from models.user import User
from models.assignment import CodingSubmission
from utils.response import objectEntity, objectsEntity, responses
import subprocess
from database.db import db
from typing import Annotated, List, Dict, Tuple
from bson import ObjectId

from utils.security import get_current_active_user
from utils.validation import AlreadyExistsError, NotExistsError
from models.assignment import ProgrammingAssignment, ProgrammingAssignmentUpdate

coding_assignment=APIRouter(prefix='/coding_assignment', tags=["Coding Assignment"])

@coding_assignment.post("/create_programming_question", status_code=201, responses=responses)
async def create_programming_question(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    assignment: ProgrammingAssignment
):
    assignment_in = db.coding_assignment.insert_one(dict(assignment))
    if assignment_in.acknowledged:
        return {"msg": "success", "db_entry_id": str(assignment_in.inserted_id)}
    raise AlreadyExistsError()
    
@coding_assignment.get('/get/{assignment_id}', responses=responses)
async def get_coding_assignment(assignment_id: str, current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    find = db.coding_assignment.find_one(filter={'_id': ObjectId(assignment_id)})
    if find:
        return objectEntity(find)
    raise NotExistsError()

@coding_assignment.delete('/delete/{assignment_id}', responses=responses)
async def delete_coding_assignment(assignment_id: str, current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    find = db.coding_assignment.find_one_and_delete(filter={'_id': ObjectId(assignment_id)})
    if find:
        return {'msg': "Assignment Deleted"}
    raise NotExistsError()

@coding_assignment.put('/update/{assgn_id}', status_code=202, responses=responses)
async def update_coding_assignment(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    assgn_id: str,
    assgn: ProgrammingAssignmentUpdate
):
    assgn = db.coding_assignment.find_one_and_update({"_id": ObjectId(assgn_id)}, {"$set": dict(assgn)})
    if not assgn:
        raise NotExistsError()
    return {"msg": "Assigment Updated"}

def run_test_cases(code: str, test_cases: List[Dict[str, str]], language: str) -> Tuple[List[Dict[str, str]], int]:
    results = []
    passed_count = 0

    for testcase in test_cases:
        input_data = testcase['input']
        expected_output = testcase['output']

        if language == 'python':
            result = subprocess.run(
                ["python3", "-c", code],
                input=input_data,
                capture_output=True,
                text=True
            )
        elif language == 'java':
            # Save code to a file
            with open("static/Main.java", "w") as f:
                f.write(code)
            
            # Compile Java code
            compile_result = subprocess.run(
                ["javac", "static/Main.java"],
                capture_output=True,
                text=True
            )

            if compile_result.returncode != 0:
                results.append({
                    "error": compile_result.stderr.strip(),
                    "output": "",
                    "status": "Fail"
                })
                continue

            # Run Java code
            result = subprocess.run(
                ["java", "-cp", "static", "Main"],
                input=input_data,
                capture_output=True,
                text=True
            )
        elif language == 'js':
            if not input_data.endswith('\n'):
                input_data += '\n'
                
            result = subprocess.run(
                ["node", "-e", code], 
                input=input_data, 
                capture_output=True, 
                text=True
            )
        else:
            raise ValueError(f"Unsupported language: {language}")

        result_dict = {
            "error": "",
            "output": result.stdout.strip(),
            "status": ""
        }

        if result.returncode == 0:
            if result.stdout.strip() == expected_output:
                result_dict["status"] = "Pass"
                passed_count += 1
            else:
                result_dict["status"] = "Fail"
        else:
            result_dict["error"] = result.stderr.strip()
            result_dict["status"] = "Fail"
        
        results.append(result_dict)

    return results, passed_count

@coding_assignment.post('/run', responses=responses)
async def run_code(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    submission: CodingSubmission
):

    assgn = db.coding_assignment.find_one({"_id": ObjectId(submission.assgn_id)})
    if not assgn:
        raise NotExistsError()
    
    public_testcases = assgn.get('public_testcase', [])
    private_testcases = assgn.get('private_testcase', [])
    # Run the test cases and get results and passed counts
    public_results, passed_public_count = run_test_cases(submission.code, public_testcases, assgn['language'])
    private_results, passed_private_count = run_test_cases(submission.code, private_testcases, assgn['language'])

    # Return results
    return {
        "public_testcases": public_results,
        "private_testcases": private_results,
        "passed_public_count": f"{passed_public_count}/{len(public_testcases)}",
        "passed_private_count": f"{passed_private_count}/{len(private_testcases)}"
    }