from fastapi import APIRouter, Security
from models.user import User
from utils.response import objectEntity, objectsEntity

from database.db import db
from typing import Annotated
import base64
from bson import ObjectId

from utils.security import get_current_active_user
from utils.validation import AlreadyExistsError, NotExistsError
from models.assignment import ProgrammingAssignment, ProgrammingAssignmentUpdate

coding_assignment=APIRouter(prefix='/coding_assignment', tags=["Coding Assignment"])

@coding_assignment.post("/create_programming_question")
async def create_programming_question(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    assignment: ProgrammingAssignment
):
    assignment_in = db.coding_assignment.insert_one(dict(assignment))
    if assignment_in.acknowledged:
        return {"msg": "success", "db_entry_id": str(assignment_in.inserted_id)}
    raise AlreadyExistsError()
    
@coding_assignment.get('/get/{assignment_id}')
async def get_coding_assignment(assignment_id: str, current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    find = db.coding_assignment.find_one(filter={'_id': ObjectId(assignment_id)})
    if find:
        return objectEntity(find)
    raise NotExistsError()

@coding_assignment.delete('/delete/{assignment_id}')
async def delete_coding_assignment(assignment_id: str, current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    find = db.coding_assignment.find_one_and_delete(filter={'_id': ObjectId(assignment_id)})
    if find:
        return {'msg': "Assignment Deleted"}
    raise NotExistsError()

@coding_assignment.put('/update/{assgn_id}')
async def update_coding_assignment(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    assgn_id: str,
    assgn: ProgrammingAssignmentUpdate
):
    assgn = db.coding_assignment.find_one_and_update({"_id": ObjectId(assgn_id)}, {"$set": dict(assgn)})
    if not assgn:
        raise NotExistsError()
    return {"msg": "Assigment Updated"}

# @coding_assignment.post('/run/{assignment_id}')
# async def run_code(assignment_id: str, request: CodeExecutionRequest):
#     find = db.coding_assignment.find_one(filter={'assignment_id': assignment_id})
#     try:
#         if find:
#             code = base64.b64decode(request.code).decode()
#             test_cases = find['test_cases']
#             results = []
#             exec_globals = {}
#             exec(code, exec_globals)
#             functions = [obj for obj in exec_globals.values() if callable(obj)]

#             if not functions:
#                 raise ValueError("No callable function found in the provided code.")
            
#             function = functions[0]

#             for test_case in test_cases:
#                 inputs = test_case['inputs']
#                 expected_output = test_case['output']

#                 try:
#                     output = function(*inputs)
#                     results.append({
#                         'inputs': inputs,
#                         'expected_output': expected_output,
#                         'output': output,
#                         'is_correct': output == expected_output
#                     })
#                 except Exception as e:
#                     results.append({
#                         'inputs': inputs,
#                         'expected_output': expected_output,
#                         'output': None,
#                         'is_correct': False,
#                         'error': str(e)
#                     })
#             return {'results': results}
        
#         raise NotExistsError()
#     except Exception as e:
#         return {'message' : 'error', 'error': str(e)}