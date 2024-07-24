responses = {
    200: {
        "description": "Successful Response"
    }, 
    404: {
        "description": "Not Found Error", 
        "content": {
            "application/json": {
                "schema": {
                    "type": "object", 
                    "properties": {
                        "error": {"type": "string"}
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error", 
        "content": {
            "Failed to create an user"
        }
    },
    422: {
        "description": "Validation Error", 
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/HTTPValidationError"
                }
            }
        }
    },
}

def objectEntity(item) -> dict:
    return {key: str(item[key]) for key in item.keys()} #need id to delete the resource

def objectsEntity(entity) -> list:
    return [objectEntity(item) for item in entity]