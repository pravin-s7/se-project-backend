from fastapi import HTTPException

class UserNotFound(HTTPException):
    def __init__(self, error_message: str, error_code: str = 404):
        detail = {"error_code": error_code, "error_message": error_message}
        super().__init__(status_code=error_code, detail=detail)

class NotFoundError(HTTPException):
    def __init__(self, error_message: str, error_code: str = 404):
        detail = {"error_code": error_code, "error_message": error_message}
        super().__init__(status_code=error_code, detail=detail)

class AlreadyExistsError(HTTPException):
    def __init__(self, error_message: str = 'Entity Already Exists', error_code: str = 409):
        detail = {"error_code": error_code, "error_message": error_message}
        super().__init__(status_code=error_code, detail=detail)

class NotExistsError(HTTPException):
    def __init__(self, error_message: str = 'Could Not Find The Requested Resource', error_code: str = 404):
        detail = {"error_code": error_code, "error_message": error_message}
        super().__init__(status_code=error_code, detail=detail)

class DeleteError(HTTPException):
    def __init__(self, error_message: str, error_code: str = 500):
        detail = {"error_code": error_code, "error_message": error_message}
        super().__init__(status_code=error_code, detail=detail)


# def raise_custom_http_exception(status_code: int, error_message: str, error_code: str):
#     raise HTTPException(
#         status_code=status_code, 
#         detail={"error_code": error_code, "error_message": error_message}
#     )