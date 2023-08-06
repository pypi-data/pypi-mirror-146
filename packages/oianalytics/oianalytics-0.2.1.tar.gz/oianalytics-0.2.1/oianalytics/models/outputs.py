from typing import Union, Optional
import io
import time
import pandas as pd

from oianalytics import api


# Output classes
class FileOutput:
    def __init__(self, file_name: str, content: Union[io.StringIO, io.BytesIO]):
        self.output_type = "file"
        self.file_name = file_name
        self.content = content

    @classmethod
    def from_pandas(
        cls,
        data: Union[pd.Series, pd.DataFrame],
        file_name: str,
        file_type: str = "csv",
        **kwargs,
    ):
        # Init
        bio = io.BytesIO()

        # Write data
        if file_type == "excel":
            data.to_excel(bio, **kwargs)
        elif file_type == "csv":
            data.to_csv(bio, **kwargs)
        else:
            raise NotImplementedError(f"Unsupported file_type: {file_type}")
        bio.seek(0)

        # Create object
        return cls(file_name=file_name, content=bio)

    def send_to_oianalytics(
        self, api_credentials: Optional[api.OIAnalyticsAPICredentials] = None
    ):
        api.endpoints.upload_file(
            file_content=self.content,
            file_name=self.file_name,
            api_credentials=api_credentials,
        )


class Temporisation:
    def __init__(self, duration=10):
        self.output_type = "temporisation"
        self.duration = duration

    def send_to_oianalytics(self):
        time.sleep(self.duration)


class OIModelOutputs:
    def __init__(self):
        self.output_type = "outputs_consolidation"
        self.model_outputs = []

    def add_output(self, output_object: Union[FileOutput, Temporisation]):
        self.model_outputs.append(output_object)

    def send_to_oianalytics(self):
        for model_output in self.model_outputs:
            model_output.send_to_oianalytics()
