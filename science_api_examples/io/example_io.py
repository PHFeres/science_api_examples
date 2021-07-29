from science_api.io import IOBaseClass


class ExampleIO(IOBaseClass):


    def __init__(self, input_data):

        self.input_data = input_data

    def get_output(self) -> dict:

        return {"greet": f"hello {self.input_data['name']}"}
