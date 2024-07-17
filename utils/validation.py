from fastapi import HTTPException

class UserNotFound(HTTPException):
    def __init__(self, error_message: str, error_code: str):
        detail = {"error_code": error_code, "error_message": error_message}
        super().__init__(status_code=404, detail=detail)

class NotFoundError(HTTPException):
    def __init__(self, error_message: str, error_code: str):
        detail = {"error_code": error_code, "error_message": error_message}
        super().__init__(status_code=404, detail=detail)

class AlreadyExistsError(HTTPException):
    def __init__(self, error_message: str, error_code: str):
        detail = {"error_code": error_code, "error_message": error_message}
        super().__init__(status_code=409, detail=detail)

class NotExistsError(HTTPException):
    def __init__(self, error_message: str, error_code: str):
        detail = {"error_code": error_code, "error_message": error_message}
        super().__init__(status_code=400, detail=detail)

class DeleteError(HTTPException):
    def __init__(self, error_message: str, error_code: str):
        detail = {"error_code": error_code, "error_message": error_message}
        super().__init__(status_code=500, detail=detail)


# def raise_custom_http_exception(status_code: int, error_message: str, error_code: str):
#     raise HTTPException(
#         status_code=status_code, 
#         detail={"error_code": error_code, "error_message": error_message}
#     )