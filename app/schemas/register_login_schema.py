from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)

    @field_validator("name", "email")
    def strip_fields(cls, v):
        return v.strip()

    @field_validator("password")
    def validate_password(cls,v):
        if v!=v.strip():
            raise ValueError("Password cannot have leading or trailing spcaces")

        return v





class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    def strip_fields(cls,v):
        return v.strip()

    @field_validator("password")
    def validate_password(cls, v):
        if v != v.strip():
            raise ValueError("Password cannot have leading or trailing spcaces")

        return v


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
