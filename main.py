import json

from src.asr_output_data import AsrOutputData
from src.bias_calculation import performance_difference
from src.filepath_manager import FilepathManager
from src.process import process_output
from src.visualize import plot_statistics


def main():
    filepath_manager = FilepathManager('config.json')
    asr_output_data = AsrOutputData(filepath_manager=filepath_manager)

    result_per_speaker_df = {}
    result_per_group_df = {}

    # Read error-data for both Read and HMI speaking style
    for speaking_style_index in range(0, 2):
        data_frame = asr_output_data.build_dataframe(speaking_style_index)

        for model in filepath_manager.asr_models:
            for _, data in data_frame[model].items():
                group = data[0]
                key = model + '_' + group + '_' + filepath_manager.speaking_style_folders[speaking_style_index]

                # Process model output data
                result_per_speaker_df[key], result_per_group_df[key] = process_output(data)

    # Write error rates to file
    with open(f'results/error_rates_per_speaker.txt','w') as file:
        file.write(json.dumps(result_per_speaker_df, indent=4))

    with open(f'results/error_rates_per_group.txt','w') as file:
        file.write(json.dumps(result_per_group_df, indent=4))

    # Bias Calculation
    # TODO:
    # performance_difference(data_frame[error_rate], filepath_manager, 'min', 'absolute')
    # performance_difference(data_frame[error_rate], filepath_manager, 'min', 'relative')

    # Data Visualization
    plot_statistics(result_per_speaker_df)


if __name__ == '__main__':
    main()
