from ninja import Schema
from pydantic import Field, constr

# class ScanSchema(Schema):
#     id: int
#     name: constr(max_length=255)
#     status: constr(max_length=255)

# class ProgressSchema(Schema):
#     scan_id: int
#     progress_percentage: int = Field(..., ge=0, le=100)


class AuthSchema(Schema):
    name: str
    password: str

class ScanUpdateSchema(Schema):
    name: constr(max_length=255)

class ScanInSchema(Schema):
    name: str

class ScanOutSchema(Schema):
    id: int
    name: str
    status: str

class ProgressInSchema(Schema):
    scan_id: int
    progress_percentage: int = Field(..., ge=0, le=100)

class ProgressOutSchema(Schema):
    id: int
    scan_id: int
    progress_percentage: int = Field(..., ge=0, le=100)
