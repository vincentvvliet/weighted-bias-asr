import pandas as pd


# TODO: update functionality to conform with new data
def process_data_per_speaker_group(data_frames, metric='median', input_type='NoAug', speech_type='Read', error_rate='WER') -> None:
    """
    Processes data per speaker group based on metric, input_type, speech_type, and error_rate.
    Writes processed data to an output file in results/.

    :param data_frames: Panda's DataFrame containing error rate data
    :param metric: specific metric to calculate, based on available Panda's Dataframe functions
    :param input_type: NoAug or SpAug or SpSpecAug
    :param speech_type: Read or Hmi
    :param error_rate: WER or CER
    :return:
    """

    # Get the pandas function for the specified metric
    metric_func = getattr(pd.Series, metric)
    values = {}

    speech_type_keywords = {
        'Read': ['DC_Read_', 'DOA_Read_', 'DT_Read_', 'NnA_Read_', 'NnT_Read_'],
        'Hmi': ['DC_Hmi_', 'DOA_Hmi_', 'DT_Hmi_', 'NnA_Hmi_', 'NnT_Hmi_']
    }

    # Check for valid speech type
    if speech_type not in speech_type_keywords:
        print(f"Invalid speech_type: {speech_type}. Valid options are 'Read' or 'Hmi'.")
        return

    # Apply the metric function
    for file_path, df in data_frames.items():
        if input_type in file_path and any(keyword in file_path for keyword in speech_type_keywords[speech_type]):
            metric_value = metric_func(df['Value'])
            values[file_path] = metric_value

    # Write to output file
    output = ''
    for file_path, metric_value in values.items():
        output_string = f'{metric.capitalize()} value for {file_path}: {metric_value}\n'
        print(output_string)
        output += output_string

    with open(f'results/{metric}-{input_type}-{speech_type}-{error_rate}.txt', 'w') as file:
        file.write(output)


def process_data_per_speech_type(data_frames, metric='median', input_type='NoAug', speech_type='Read', error_rate='WER') -> None:
    """
        Processes data per speech type based on metric, input_type, speech_type, and error_rate. For the specified speech
        type, the values for all files within the matching directory are combined and processed together.
        Writes processed data to an output file in results/.

        :param data_frames: Panda's DataFrame containing error rate data
        :param metric: specific metric to calculate, based on available Panda's Dataframe functions
        :param input_type: NoAug or SpAug or SpSpecAug
        :param speech_type: Read or Hmi
        :param error_rate: WER or CER
        :return:
        """

    # Get the pandas function for the specified metric
    metric_func = getattr(pd.Series, metric)

    # Filter on speech type
    speech_type_keywords = {
        'Read': ['DC_Read_', 'DOA_Read_', 'DT_Read_', 'NnA_Read_', 'NnT_Read_'],
        'Hmi': ['DC_Hmi_', 'DOA_Hmi_', 'DT_Hmi_', 'NnA_Hmi_', 'NnT_Hmi_']
    }

    # Check for valid speech type
    if speech_type not in speech_type_keywords:
        print(f"Invalid speech_type: {speech_type}. Valid options are 'Read' or 'Hmi'.")
        return

    # Combine values for each speaker group
    combined_values = []
    for file_path, df in data_frames.items():
        if input_type in file_path and any(keyword in file_path for keyword in speech_type_keywords[speech_type]):
            combined_values.append(df['Value'])

    if combined_values:
        # Concatenate values and apply the metric function
        combined_series = pd.concat(combined_values, ignore_index=True)
        overall_metric_value = metric_func(combined_series)
        output = f'Overall {metric.capitalize()} value for {input_type} {speech_type} {error_rate} data: {overall_metric_value}'
        print(output)
        with open(f'results/overall-{metric}-{input_type}-{speech_type}-{error_rate}.txt', 'w') as file:
            file.write(output + '\n')
    else:
        print(f'No data found for {input_type} {speech_type}.')