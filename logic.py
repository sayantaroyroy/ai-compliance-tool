import re
import pytesseract
from PIL import Image
import io
import speech_recognition as sr
from pydub import AudioSegment

# --- MEDIA EXTRACTION (Eyes & Ears) ---

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Converts raw image bytes into a string of text using Tesseract OCR.
    """
    try:
        # 1. Open the image from the raw bytes (in-memory)
        image = Image.open(io.BytesIO(image_bytes))
        
        # 2. Use Tesseract to read the text
        text = pytesseract.image_to_string(image)
        
        # 3. Clean up the text
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return "" 

def extract_text_from_audio(audio_bytes: bytes) -> str:
    """
    Transcribes audio bytes to text using SpeechRecognition (Google Web Speech API).
    """
    try:
        # 1. Load audio from bytes (supports mp3, wav, etc.) using pydub
        #    This is crucial because SpeechRecognition prefers WAV.
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # 2. Export to WAV format in-memory
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        
        # 3. Initialize Recognizer
        recognizer = sr.Recognizer()
        
        # 4. Record the audio from the buffer
        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)
            
        # 5. Transcribe using Google's free API
        text = recognizer.recognize_google(audio_data)
        return text
        
    except sr.UnknownValueError:
        return "" # Audio was unintelligible (or silence)
    except Exception as e:
        print(f"Audio Error: {e}")
        return ""


# --- RISK SCANNERS (The Brain) ---

def check_gdpr_risk(text: str) -> dict:
    """
    Analyzes text for GDPR risks (PII detection).
    """
    risk_score = 0
    reasons = []

    # 1. Check for Email Addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    if emails:
        risk_score += 40
        reasons.append(f"Found {len(emails)} email address(es)")

    # 2. Check for Phone Numbers (Simple international pattern)
    phone_pattern = r'\+?[0-9][0-9\-\s]{7,15}'
    phones = re.findall(phone_pattern, text)
    valid_phones = [p for p in phones if len(re.sub(r'\D', '', p)) > 9]
    
    if valid_phones:
        risk_score += 40
        reasons.append(f"Found {len(valid_phones)} phone number(s)")

    # Determine Final Level
    if risk_score == 0:
        return {"score": 0, "reason": "No PII detected", "level": "LOW"}
    elif risk_score >= 80:
        return {"score": 90, "reason": "Multiple PII types found: " + ", ".join(reasons), "level": "HIGH"}
    else:
        return {"score": 50, "reason": "Potential PII found: " + ", ".join(reasons), "level": "MEDIUM"}


def check_copyright_risk(text: str) -> dict:
    """
    Analyzes text for copyright infringement using Jaccard Similarity.
    """
    protected_texts = [
        "all rights reserved by compu-global-hyper-mega-net",
        "just do it",
        "i have a dream that one day this nation will rise up",
        "may the force be with you",
        "to be or not to be that is the question"
    ]

    input_tokens = set(text.lower().split())
    highest_similarity = 0.0
    match_found = None

    for protected in protected_texts:
        protected_tokens = set(protected.split())
        
        intersection = input_tokens.intersection(protected_tokens)
        union = input_tokens.union(protected_tokens)
        
        if len(union) == 0:
            continue
            
        similarity = len(intersection) / len(union)
        
        if similarity > highest_similarity:
            highest_similarity = similarity
            match_found = protected

    score = int(highest_similarity * 100)
    
    if score > 50:
        return {
            "score": score, 
            "reason": f"High similarity ({score}%) to protected phrase: '{match_found}'", 
            "level": "HIGH"
        }
    elif score > 20:
            return {
            "score": score, 
            "reason": f"Partial similarity ({score}%) to protected content.", 
            "level": "MEDIUM"
        }
    else:
        return {"score": 0, "reason": "Original content", "level": "LOW"}


def check_social_risk(text: str) -> dict:
    """
    Analyzes text for Social Media violations (Toxicity, Engagement Bait).
    """
    toxic_keywords = ["stupid", "idiot", "hate you", "kill", "die", "scam"]
    engagement_bait = ["like for like", "follow back", "instant cash", "free money", "dm for price"]
    
    text_lower = text.lower()
    score = 0
    reasons = []

    for word in toxic_keywords:
        if word in text_lower:
            score += 30
            reasons.append(f"Contains toxic word: '{word}'")

    for phrase in engagement_bait:
        if phrase in text_lower:
            score += 25
            reasons.append(f"Contains engagement bait: '{phrase}'")

    score = min(score, 100)

    if score > 60:
        return {"score": score, "reason": "High risk of moderation: " + ", ".join(reasons), "level": "HIGH"}
    elif score > 0:
        return {"score": score, "reason": "Potential content warning: " + ", ".join(reasons), "level": "MEDIUM"}
    else:
        return {"score": 0, "reason": "Safe for posting", "level": "LOW"}