import os
import pandas as pd


def main():
    # Read data
    data_frames = retrieve_data()

    # Process the data based on specific metric, input_type and speech_type
    process_data_per_speaker_group(data_frames, metric='median', input_type='NoAug', speech_type='Read')
    process_data_per_speech_type(data_frames, metric='median', input_type='NoAug', speech_type='Read')


def read_file(file_path):
    with open(file_path, 'r') as file:
        data = [float(line.strip()) for line in file if line.strip()]
    return pd.DataFrame(data, columns=["Value"])


def retrieve_data():
    # Directory and file structure
    base_dir = 'data'
    parent_folders = ['WER', 'CER']
    child_folders = ['NoAug', 'SpAug', 'SpSpecAug']
    sub_folders = ['HMI', 'Rd']
    files_rd = ['DC_Read_{parent}', 'DOA_Read_{parent}', 'DT_Read_{parent}', 'NnA_Read_{parent}', 'NnT_Read_{parent}']
    files_hmi = ['DC_Hmi_{parent}', 'DOA_Hmi_{parent}', 'DT_Hmi_{parent}', 'NnA_Hmi_{parent}', 'NnT_Hmi_{parent}']

    # Read files into dataframes
    data_frames = {}

    for parent in parent_folders:
        for child in child_folders:
            for sub in sub_folders:
                # Determine the correct file naming format
                files = files_hmi if sub == 'HMI' else files_rd
                for file in files:
                    file_name = file.format(parent=parent)
                    file_path = os.path.join(base_dir, parent, child, sub, f'{file_name}s')

                    try:
                        df = read_file(file_path)
                        data_frames[file_path] = df
                    except Exception as e:
                        print(f'Failed to read {file_path}: {e}')

    return data_frames


def process_data_per_speaker_group(data_frames, metric='median', input_type='NoAug', speech_type='Read'):
    values = {}
    metric_func = getattr(pd.Series, metric)  # Get the pandas function for the specified metric

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

    # Print values
    output = ''
    for file_path, metric_value in values.items():
        output += f'{metric.capitalize()} value for {file_path}: {metric_value}'
        print(output)

    # Write to output file
    with open(f'{metric}-{input_type}-{speech_type}.txt', 'w') as file:
        file.write(output + '\n')

def process_data_per_speech_type(data_frames, metric='median', input_type='NoAug', speech_type='Read'):
    # Get the pandas function for the specified metric
    metric_func = getattr(pd.Series, metric)

    # Filter on speech type
    speech_type_keywords = {
        'Read': ['DC_Read_', 'DOA_Read_', 'DT_Read_', 'NnA_Read_', 'NnT_Read_'],
        'Hmi': ['DC_Hmi_', 'DOA_Hmi_', 'DT_Hmi_', 'NnA_Hmi_', 'NnT_Hmi_']
    }

    if speech_type not in speech_type_keywords:
        print(f"Invalid speech_type: {speech_type}. Valid options are 'Read' or 'Hmi'.")
        return

    # Combine values for each speaker group
    combined_values = []

    for file_path, df in data_frames.items():
        if input_type in file_path and any(keyword in file_path for keyword in speech_type_keywords[speech_type]):
            combined_values.append(df['Value'])

    if combined_values:
        combined_series = pd.concat(combined_values, ignore_index=True)
        overall_metric_value = metric_func(combined_series)
        output = f'Overall {metric.capitalize()} value for {input_type} {speech_type} data: {overall_metric_value}'
        print(output)
        with open(f'overall-{metric}-{input_type}-{speech_type}.txt', 'w') as file:
            file.write(output + '\n')
    else:
        print(f'No data found for {input_type} {speech_type}.')


if __name__ == '__main__':
    main()
