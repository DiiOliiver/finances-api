from typing import Dict, Optional

from pydantic import BaseModel


class CurrentUser(BaseModel):
    user_pk: str
    name: str
    email: str
    roles: Optional[Dict] = None
