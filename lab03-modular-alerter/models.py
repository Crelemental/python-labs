from pydantic import BaseModel, Field, IPvAnyAddress
from typing import Literal

class FirewallLog(BaseModel):
    src_ip: IPvAnyAddress
    action: Literal["ALLOW", "BLOCK"]

class SecurityAlert(BaseModel):
    source_ip: str
    denied_count: int
    severity: str = Field(default="HIGH")
    message: str