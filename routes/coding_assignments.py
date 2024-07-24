from fastapi import APIRouter, Security
from models.model import User
from utils.response import objectEntity, objectsEntity

from database.db import db
from typing import Annotated
import base64

from utils.security import get_current_active_user
from utils.validation import AlreadyExistsError, NotExistsError
from models.model import CodingAssignment, SuccessCreateResponse

coding_assignment=APIRouter(prefix='/coding_assignment', tags=["Coding Assignment"])

@coding_assignment.post('/create', )
async def create_coding_assignment(coding_assignment_input: CodingAssignment, current_user: 
                        Annotated[User, Security(get_current_active_user, scopes=["user"])],) -> SuccessCreateResponse:
    find = db.coding_assignment.find_one(filter={'assignment_id': coding_assignment_input.assignment_id})
    if find:
        raise AlreadyExistsError('Duplicated Assignment ID')
    coding_assignment_in = db.coding_assignment.insert_one({
       'assignment_id' : coding_assignment_input.assignment_id,
       'assignment_name' : coding_assignment_input.assignment_name,
       'course_id' : coding_assignment_input.course_id,
       'due_date' : coding_assignment_input.due_date,
       'questions' : coding_assignment_input.questions
    })
    if coding_assignment_in.acknowledged:
        return {'message' : 'success', 'db_entry_id': str(coding_assignment_in.inserted_id)}
    else:
        raise AlreadyExistsError()
    
@coding_assignment.get('/get/{assignment_id}')
async def get_coding_assignment(assignment_id: str, current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    find = db.coding_assignment.find_one(filter={'assignment_id': assignment_id})
    if find:
        return objectEntity(find)
    raise NotExistsError()

@coding_assignment.post('/run/{assignment_id}')
async def run_code(assignment_id: str, request: CodeExecutionRequest):
    find = db.coding_assignment.find_one(filter={'assignment_id': assignment_id})
    try:
        if find:
            code = base64.b64decode(request.code).decode()
            test_cases = find['test_cases']
            results = []
            exec_globals = {}
            exec(code, exec_globals)
            functions = [obj for obj in exec_globals.values() if callable(obj)]

            if not functions:
                raise ValueError("No callable function found in the provided code.")
            
            function = functions[0]

            for test_case in test_cases:
                inputs = test_case['inputs']
                expected_output = test_case['output']

                try:
                    output = function(*inputs)
                    results.append({
                        'inputs': inputs,
                        'expected_output': expected_output,
                        'output': output,
                        'is_correct': output == expected_output
                    })
                except Exception as e:
                    results.append({
                        'inputs': inputs,
                        'expected_output': expected_output,
                        'output': None,
                        'is_correct': False,
                        'error': str(e)
                    })
            return {'results': results}
        
        raise NotExistsError()
    except Exception as e:
        return {'message' : 'error', 'error': str(e)}