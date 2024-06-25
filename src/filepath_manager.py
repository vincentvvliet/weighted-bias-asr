import json


class FilepathManager:
    """
    Based on a similar implementation by @kmjones.

    Handles the error-data retrieval step. Generates paths from which to retrieve error-data based on config.json.

    Attributes:
        base_path: TODO
        error_rates: TODO
        speaking_style_folders: TODO
        speaking_style_infixes: TODO
        speaker_groups: TODO
        asr_models: TODO
        path_templates: TODO
    """

    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = json.load(file)

        self.base_path = self.config['base_path']
        self.error_rates = self.config['error_rates']
        self.speaking_style_folders = self.config['speaking_style_folders']
        self.speaking_style_infixes = self.config['speaking_style_infixes']
        self.speaker_groups = self.config['speaker_groups']
        self.asr_models = self.config['asr_models']
        self.path_templates = self.config['path_templates']

    def _generate_path(self, template, **kwargs):
        return template.format(base_path=self.base_path, **kwargs)

    def get_word_error_rate_path(self, error_rate, speaking_style_folder, speaking_style_infix, speaker_group, asr_model):
        # Public method to get the path for an error rate file
        template = self.path_templates['error_rate_file']
        return self._generate_path(template, error_rate=error_rate, speaking_style_folder=speaking_style_folder,
                                   speaking_style_infix=speaking_style_infix, speaker_group=speaker_group,
                                   asr_model=asr_model)
    def get_output_path(self, speaking_style_folder, speaking_style_infix, speaker_group, asr_model):
        # Public method to get the path for an output file
        template = self.path_templates['output_file']
        return self._generate_path(template, speaking_style_folder=speaking_style_folder, speaker_group=speaker_group, asr_model=asr_model)

    def get_error_rates(self):
        return self.error_rates

    def get_speaker_groups(self):
        return self.speaker_groups

    def get_asr_models(self):
        return self.asr_models

    def get_speaking_style_folders(self):
        return self.speaking_style_folders

    def get_speaking_style_infixes(self):
        return self.speaking_style_infixes
