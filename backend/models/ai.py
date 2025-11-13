from pydantic import BaseModel

class AIQuery(BaseModel):
    prompt: str