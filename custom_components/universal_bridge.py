from lfx.custom import CustomComponent
from lfx.template.field.base import Output

class UniversalBridge(CustomComponent):
    display_name = "Universal Bridge"
    description = "Connects anything to Groq System Message without hiding."
    icon = "Zap"

    def build_config(self):
        return {
            "input_text": {
                "display_name": "Input Text",
                "multiline": True,
                "info": "Paste your text here or connect from another component."
            },
        }

    def build(self, input_text: str) -> str:
        # Ye function kisi bhi text ko Groq ke liye 'Safe' bana deta hai
        return str(input_text)
