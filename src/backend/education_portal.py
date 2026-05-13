from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Bharat AI Guru - Educational Portal")

# 1. Configuration Data (Byju's style categories)
INDIAN_LANGUAGES = [
    "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", "Kannada", "Kashmiri", 
    "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi", "Nepali", "Odia", 
    "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil", "Telugu", "Urdu", "English"
]

CLASSES = ["Nursery", "LKG", "UKG"] + [f"{i}th" for i in range(1, 13)]

BOARDS = ["CBSE", "ICSE", "UP Board", "Bihar Board", "Maharashtra Board", "Rajasthan Board", "Other State Boards"]

# 2. Student Data Model
class StudentRegistration(BaseModel):
    full_name: str
    email: str
    phone: str
    student_class: str
    board: str
    language: str
    target_subject: str

# 3. Registration Endpoint
@app.post("/register")
async def register_student(student: StudentRegistration):
    # Validation logic
    if student.language not in INDIAN_LANGUAGES:
        raise HTTPException(status_code=400, detail="Language not supported")
    
    if student.student_class not in CLASSES:
        raise HTTPException(status_code=400, detail="Invalid Class")

    # Yahan hum student ko database mein save karenge
    # Aur uske baad Langflow ko ye batayenge ki naya bacha aa gaya hai
    
    return {
        "status": "success",
        "message": f"Namaste {student.full_name}! Welcome to Bharat AI Guru.",
        "config": {
            "persona": "Guru Ji",
            "syllabus": "NCERT" if student.board in ["CBSE", "UP Board", "Bihar Board"] else "State Specific",
            "language_mode": student.language
        }
    }

# 4. Langflow Connector (Brain Link)
@app.get("/get_guru_instructions/{student_id}")
async def get_guru_instructions(student_class: str, board: str, language: str):
    """
    Ye function Langflow ko dynamic prompt bhejega
    """
    prompt = (
        f"You are a master teacher. Teach a student from {board} in {language} language. "
        f"The student is in {student_class}. Follow the NCERT syllabus strictly. "
        f"Use simple stories for Nursery-5th, and deep concepts for 9th-12th."
    )
    return {"dynamic_prompt": prompt}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
