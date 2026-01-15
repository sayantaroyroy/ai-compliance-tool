from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from models import AnalysisRequest, ComplianceResponse, RiskScore
from logic import (
    check_gdpr_risk, 
    check_copyright_risk, 
    check_social_risk, 
    extract_text_from_image, 
    extract_text_from_audio
)

app = FastAPI(title="AI Compliance & Risk API")

# --- 1. FRONTEND ROUTE ---
@app.get("/")
def read_root():
    """
    Serves the HTML Dashboard.
    """
    return FileResponse('index.html')

# --- 2. TEXT ENDPOINT ---
@app.post("/analyze", response_model=ComplianceResponse)
def analyze_content(request: AnalysisRequest):
    """
    Analyzes raw text input for compliance risks.
    """
    # Run all checks
    gdpr_result = check_gdpr_risk(request.text_content)
    copyright_result = check_copyright_risk(request.text_content)
    social_result = check_social_risk(request.text_content)

    return ComplianceResponse(
        gdpr_risk=RiskScore(**gdpr_result),
        copyright_risk=RiskScore(**copyright_result),
        social_platform_risk=RiskScore(**social_result)
    )

# --- 3. IMAGE ENDPOINT (Vision) ---
@app.post("/analyze/image", response_model=ComplianceResponse)
async def analyze_image_file(file: UploadFile = File(...)):
    """
    Analyzes an uploaded image file (PNG/JPG) for text-based compliance risks.
    """
    # Read bytes and extract text
    image_data = await file.read()
    extracted_text = extract_text_from_image(image_data)
    
    # Handle empty/unreadable images
    if not extracted_text:
        return ComplianceResponse(
            gdpr_risk=RiskScore(score=0, reason="No text detected in image", level="LOW"),
            copyright_risk=RiskScore(score=0, reason="No text detected", level="LOW"),
            social_platform_risk=RiskScore(score=0, reason="No text detected", level="LOW")
        )

    # Run checks on extracted text
    gdpr_result = check_gdpr_risk(extracted_text)
    copyright_result = check_copyright_risk(extracted_text)
    social_result = check_social_risk(extracted_text)

    # Append source info to reason for clarity
    gdpr_result["reason"] += " (Source: Image)"

    return ComplianceResponse(
        gdpr_risk=RiskScore(**gdpr_result),
        copyright_risk=RiskScore(**copyright_result),
        social_platform_risk=RiskScore(**social_result)
    )

# --- 4. AUDIO ENDPOINT (Hearing) ---
@app.post("/analyze/audio", response_model=ComplianceResponse)
async def analyze_audio_file(file: UploadFile = File(...)):
    """
    Analyzes an uploaded AUDIO file (MP3/WAV) for voice-based compliance risks.
    """
    # Read bytes and transcribe
    audio_data = await file.read()
    extracted_text = extract_text_from_audio(audio_data)
    
    # Handle silence/unintelligible audio
    if not extracted_text:
        return ComplianceResponse(
            gdpr_risk=RiskScore(score=0, reason="No speech detected", level="LOW"),
            copyright_risk=RiskScore(score=0, reason="No speech detected", level="LOW"),
            social_platform_risk=RiskScore(score=0, reason="No speech detected", level="LOW")
        )

    # Run checks on transcribed text
    gdpr_result = check_gdpr_risk(extracted_text)
    copyright_result = check_copyright_risk(extracted_text)
    social_result = check_social_risk(extracted_text)

    # Append transcript to reason so the user knows what was heard
    gdpr_result["reason"] += f" [Transcript: '{extracted_text}']"

    return ComplianceResponse(
        gdpr_risk=RiskScore(**gdpr_result),
        copyright_risk=RiskScore(**copyright_result),
        social_platform_risk=RiskScore(**social_result)
    )