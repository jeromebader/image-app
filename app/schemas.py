from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

class UserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class ImageSchema(BaseModel):
    file_name: str
    file_path: str
    upload_date: datetime
    user_id: int
    # class Config:
    #     arbitrary_types_allowed = True
