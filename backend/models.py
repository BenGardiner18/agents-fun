from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Account Models
class AccountBase(BaseModel):
    name: str
    industry: Optional[str] = None
    plan: Optional[str] = None
    status: Optional[str] = None

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Contact Models
class ContactBase(BaseModel):
    account_id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    title: Optional[str] = None
    role: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Email Models
class EmailBase(BaseModel):
    contact_id: int
    subject: str
    body: Optional[str] = None

class EmailCreate(EmailBase):
    pass

class EmailUpdate(EmailBase):
    pass

class Email(EmailBase):
    id: int
    sent_at: datetime

    class Config:
        from_attributes = True

# Call Models
class CallBase(BaseModel):
    contact_id: int
    call_type: str
    duration: Optional[int] = None
    outcome: Optional[str] = None

class CallCreate(CallBase):
    pass

class CallUpdate(CallBase):
    pass

class Call(CallBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Call Transcript Models
class CallTranscriptBase(BaseModel):
    call_id: int
    transcript: str

class CallTranscriptCreate(CallTranscriptBase):
    pass

class CallTranscriptUpdate(CallTranscriptBase):
    pass

class CallTranscript(CallTranscriptBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Response Models
class MessageResponse(BaseModel):
    message: str 