from science_api.io import IOBaseClass


class ExampleIO(IOBaseClass):


    def __init__(self, input_data):

        self.input_data = input_data

    def get_output(self) -> dict:

        responses = list()
        for elem in self.input_data["people"]:

            responses.append(
                f"hello {elem['name']}, you have {elem['money']} {elem['unit']}."
            )

        return {"responses": responses}
