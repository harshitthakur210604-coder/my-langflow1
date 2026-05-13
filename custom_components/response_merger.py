from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output
from lfx.schema.message import Message

class ResponseMerger(Component):
    display_name: str = "Response Merger"
    description: str = "Combines outputs from Generator and Analyzer for a single Chat Output."
    name = "ResponseMerger"
    icon = "Merge"

    inputs = [
        MessageTextInput(name="input1", display_name="Generator Output", info="Connect Generator here."),
        MessageTextInput(name="input2", display_name="Analyzer Output", info="Connect Analyzer here."),
    ]

    outputs = [
        Output(display_name="Final Response", name="final_out", method="merge_outputs"),
    ]

    def merge_outputs(self) -> Message:
        # Check which input has data and return it
        text1 = self.input1.strip() if self.input1 else ""
        text2 = self.input2.strip() if self.input2 else ""
        
        if text1:
            return Message(text=text1)
        if text2:
            return Message(text=text2)
            
        return Message(text="No response generated.")
