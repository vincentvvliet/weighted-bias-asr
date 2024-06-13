import pandas as pd

from .filepath_manager import FilepathManager


class AsrOutputData:
    """
    Based on a similar implementation by @kmjones.

    Handles the creation of a Pandas Dataframe containing all the information from the performance error-data.

    Attributes:
        filepath_manager: A FilepathManager instance to handle file retrieval and reading.
    """

    def __init__(self, filepath_manager: FilepathManager):
        self.filepath_manager = filepath_manager

    def build_dataframe(self, speaking_style=0):
        error_rates = self.filepath_manager.get_error_rates()
        speaker_groups = self.filepath_manager.get_speaker_groups()
        asr_models = self.filepath_manager.get_asr_models()

        speaking_style_folder = self.filepath_manager.get_speaking_style_folders()[speaking_style]
        speaking_style_infix = self.filepath_manager.get_speaking_style_infixes()[speaking_style]

        d = {}

        for model in asr_models:
            # Initialize for each model
            d[model] = []

        for group in speaker_groups:
            for model in asr_models:
                model_error_filepath = self.filepath_manager.get_output_path(
                    speaking_style_folder=speaking_style_folder,
                    speaking_style_infix=speaking_style_infix,
                    speaker_group=group, asr_model=model)

                d[model].append((group, pd.read_csv(model_error_filepath)))

        return pd.DataFrame(data=d)
