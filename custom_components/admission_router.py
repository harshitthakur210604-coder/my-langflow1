from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, DropdownInput
from lfx.schema.message import Message
import json

class AdmissionRouter(Component):
    display_name: str = "Admission Flow Router"
    description: str = "Routes the request to either Test Generation or Result Analysis."
    name = "AdmissionRouter"
    icon = "Split"

    inputs = [
        MessageTextInput(name="input_data", display_name="Input JSON", info="JSON containing task and student details."),
        DropdownInput(name="task_type", display_name="Manual Task Override", options=["Auto", "GENERATE", "ANALYZE"], value="Auto"),
    ]

    outputs = [
        Output(display_name="Generator Data", name="gen_out", method="route_to_gen"),
        Output(display_name="Analyzer Data", name="ana_out", method="route_to_ana"),
    ]

    def _parse_input(self):
        try:
            data = json.loads(self.input_data)
            return data
        except:
            return {"task": self.task_type if self.task_type != "Auto" else "GENERATE"}

    def route_to_gen(self) -> Message:
        data = self._parse_input()
        if data.get("task") == "GENERATE" or self.task_type == "GENERATE":
            return Message(text=self.input_data)
        return Message(text="")

    def route_to_ana(self) -> Message:
        data = self._parse_input()
        if data.get("task") == "ANALYZE" or self.task_type == "ANALYZE":
            return Message(text=self.input_data)
        return Message(text="")
