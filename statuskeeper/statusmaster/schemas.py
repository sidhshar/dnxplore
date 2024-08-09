from ninja import Schema
from pydantic import Field, constr

class ScanSchema(Schema):
    id: int
    name: constr(max_length=255)
    status: constr(max_length=255)

class ProgressSchema(Schema):
    scan_id: int
    progress_percentage: int = Field(..., ge=0, le=100)
