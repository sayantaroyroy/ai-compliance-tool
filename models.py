from pydantic import BaseModel
from typing import Optional

# INPUT: What the user sends us
class AnalysisRequest(BaseModel):
    text_content: str
    region: str = "EU"  # Default to EU (stricter)
    media_type: str = "text" # text, image, or audio

# OUTPUT: What we send back
class RiskScore(BaseModel):
    score: int  # 0 to 100
    reason: str
    level: str  # LOW, MEDIUM, HIGH

class ComplianceResponse(BaseModel):
    gdpr_risk: RiskScore
    copyright_risk: RiskScore
    social_platform_risk: RiskScore