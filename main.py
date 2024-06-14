import json

from src.asr_output_data import AsrOutputData
from src.bias_calculation import performance_difference, get_performance_differences, combine_performance_differences
from src.filepath_manager import FilepathManager
from src.process import process_output
from src.visualize import plot_statistics, plot_performance_difference


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

    # Bias Calculation
    performance_differences = get_performance_differences(result_per_group_df, filepath_manager)

    # Plot the combined performance differences
    plot_performance_difference(performance_differences, filepath_manager)

    # Data Visualization
    plot_statistics(result_per_speaker_df)


if __name__ == '__main__':
    main()
