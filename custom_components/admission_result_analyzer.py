from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr
import os

class AdmissionResultAnalyzer(Component):
    display_name: str = "Admission Result Analyzer"
    description: str = "Analyzes test results and provides personalized AI feedback."
    name = "AdmissionResultAnalyzer"
    icon = "LineChart"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="student_info", display_name="Student Info", info="Name, Class, etc."),
        MessageTextInput(name="test_data", display_name="Test Data (JSON)", info="The original questions and student's answers."),
        MessageTextInput(name="score_summary", display_name="Score Summary", info="Total marks, correct/wrong count."),
    ]

    outputs = [
        Output(display_name="AI Analytics Report", name="analytics_report", method="analyze_results"),
    ]

    def analyze_results(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")

        prompt = (
            f"You are an Academic Counselor for Bharat AI Guru. Analyze the following admission test result:\n\n"
            f"STUDENT INFO: {self.student_info}\n"
            f"SCORE SUMMARY: {self.score_summary}\n"
            f"DETAILED TEST DATA: {self.test_data}\n\n"
            "TASK:\n"
            "1. Provide a professional 'Analytical Report'.\n"
            "2. Identify specific strengths (e.g., 'Excellent in Math Logic').\n"
            "3. Identify areas of improvement (e.g., 'Needs to focus on English Tenses').\n"
            "4. Give a personalized 'Guru's Advice' for the student's upcoming session in the target class.\n"
            "5. Keep the tone encouraging, professional, and insightful.\n\n"
            "Format the output in clean Markdown."
        )
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
