import pandas as pd

from .filepath_manager import FilepathManager


class AsrPerformanceData:
    """
    Based on a similar implementation by @kmjones.

    Handles the creation of a Pandas Dataframe containing all the information from the performance data.

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

        for error_rate in error_rates:
            # Initialize for each error_rate
            d[error_rate] = {'Group': []}

            for model in asr_models:
                # Initialize for each model per error rate
                d[error_rate][model] = []

            for group in speaker_groups:
                # TODO: see if group is necessary
                d[error_rate]['Group'].append(group)

                for model in asr_models:
                    model_error_filepath = self.filepath_manager.get_word_error_rate_path(
                        error_rate=error_rate,
                        speaking_style_folder=speaking_style_folder,
                        speaking_style_infix=speaking_style_infix,
                        speaker_group=group, asr_model=model)

                    with open(model_error_filepath, 'r') as file:
                        # Read all lines from the file
                        for line in file.readlines():
                            d[error_rate][model].append(float(line))

        return pd.DataFrame(data=d)
