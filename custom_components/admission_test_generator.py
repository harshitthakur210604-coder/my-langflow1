from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr
import json, os, re

class AdmissionTestGenerator(Component):
    display_name: str = "Admission Test Generator"
    description: str = "Generates exactly 20 MCQ questions. Fixed for truncation issues."
    name = "AdmissionTestGenerator"
    icon = "GraduationCap"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="input_json", display_name="Input Data (from Router)"),
    ]

    outputs = [
        Output(display_name="Test Questions (JSON)", name="questions_json", method="generate_questions"),
    ]

    def generate_questions(self) -> Message:
        # 1. Parse Input
        try:
            input_data = json.loads(self.input_json)
            name = input_data.get("student_name", "Student")
            raw_class = str(input_data.get("class", "9")).lower()
            target_grade = int(re.search(r'\d+', raw_class).group()) if re.search(r'\d+', raw_class) else 9
        except Exception:
            name, target_grade = "Student", 9

        # 2. Hardcoded Grade-Specific Guardrails
        if target_grade <= 2:
            difficulty = "PRIMARY (Grades 1-2)"
            math_inst = "1-digit addition/subtraction (e.g., 2+3), counting objects."
            sci_inst = "Identifying animals, colors, fruits, and basic body parts."
            eng_inst = "Letter recognition, 3-letter word spellings (CAT, DOG)."
            gk_inst = "National flag colors, national animal, name of current PM."
        elif target_grade <= 5:
            difficulty = "ELEMENTARY (Grades 3-5)"
            math_inst = "Multiplication tables (up to 12), basic division, simple word problems."
            sci_inst = "Parts of a plant, states of matter, basic digestion."
            eng_inst = "Nouns, Verbs, Adjectives, Singular/Plural."
            gk_inst = "State capitals, famous monuments, national dates."
        else:
            difficulty = "MIDDLE/HIGH SCHOOL (Grades 6-9)"
            math_inst = "Fractions, Algebra (x+5=15), Geometry, Ratios."
            sci_inst = "Photosynthesis, Atomic structure, Laws of motion."
            eng_inst = "Tenses, Active/Passive, Clauses, Vocabulary."
            gk_inst = "History, Constitution, Geography, World Affairs."

        # 3. Model Initialization with Higher Max Tokens
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        # Added max_tokens to prevent truncation
        llm = ChatGroq(
            api_key=SecretStr(api_key).get_secret_value(), 
            model="llama-3.1-8b-instant",
            max_tokens=3000,
            temperature=0.1
        )
        
        # 4. Forceful Prompt
        prompt = (
            f"Set an Admission Test for {name} (Class {target_grade}).\n"
            f"Difficulty: {difficulty}\n\n"
            "MANDATORY: You MUST generate EXACTLY 20 questions in total (5 Math, 5 Science, 5 English, 5 GK).\n"
            "DO NOT STOP early. You must complete the entire JSON array.\n\n"
            "SUBJECT FOCUS:\n"
            f"- Math: {math_inst}\n"
            f"- Science: {sci_inst}\n"
            f"- English: {eng_inst}\n"
            f"- GK: {gk_inst}\n\n"
            "STRICT RULES:\n"
            "1. NOHallucinations. Solve math first.\n"
            "2. 'correct' must match an option exactly.\n"
            "3. Format: [{\"id\":1, \"subject\":\"...\", \"question\":\"...\", \"options\":[\"...\"], \"correct\":\"...\"}, ...]\n\n"
            "Return ONLY the JSON array. No other text."
        )
        
        # 5. Execute and Clean Output
        response = llm.invoke(prompt)
        clean_content = response.content.strip()
        clean_content = re.sub(r'^.*?\[', '[', clean_content, flags=re.DOTALL)
        clean_content = re.sub(r'\].*?$', ']', clean_content, flags=re.DOTALL)
        
        return Message(text=clean_content)
