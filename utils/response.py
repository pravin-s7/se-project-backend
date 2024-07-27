from typing import Any
from bson import ObjectId
from datetime import datetime

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
    return {key: str(item[key]) if key == '_id' else item[key] for key in item.keys()}

def convert_to_serializable(item: Any) -> Any:
    if isinstance(item, dict):
        return {key: convert_to_serializable(value) for key, value in item.items()}
    elif isinstance(item, list):
        return [convert_to_serializable(element) for element in item]
    elif isinstance(item, ObjectId):
        return str(item)
    elif isinstance(item, datetime):
        return item.isoformat()
    else:
        return item

def objectsEntity(entity) -> list:
    return [objectEntity(item) for item in entity]