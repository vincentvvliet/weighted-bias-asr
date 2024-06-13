import json

from src.asr_output_data import AsrOutputData
from src.asr_performance_data import AsrPerformanceData
from src.bias_calculation import performance_difference
from src.filepath_manager import FilepathManager
from src.process import statistics_per_asr_model, process_output_per_speaker, process_output_per_group
from src.visualize import plot_statistics


def main():
    # Initialize dataframe creation
    filepath_manager = FilepathManager('config.json')
    asr_performance_data = AsrPerformanceData(filepath_manager=filepath_manager)
    statistics = []

    # Read error-data for both Read and HMI speaking style
    for speaking_style_index in range(0, 2):
        data_frame = asr_performance_data.build_dataframe(speaking_style_index)

        # Data Processing per error rate
        for i, error_rate in enumerate(filepath_manager.error_rates):
            error_rate_name = data_frame.columns[i]

            # Calculate statistics (saved in /results/statistics)
            statistics.append((statistics_per_asr_model(data_frame[error_rate], filepath_manager, error_rate_name,
                                                        speaking_style_index), speaking_style_index, error_rate_name))

            # Bias Calculation
            performance_difference(data_frame[error_rate], filepath_manager, 'min', 'absolute')
            performance_difference(data_frame[error_rate], filepath_manager, 'min', 'relative')

            # Data visualization
            # TODO

    plot_statistics(statistics)
    print(statistics)

def test():
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

                # Process data
                result_per_speaker_df[key] = process_output_per_speaker(data)
                result_per_group_df[key] = process_output_per_group(data)

    # Write error rates to file
    with open(f'results/error_rates_per_group.txt','w') as file:
        file.write(json.dumps(result_per_group_df, indent=4))

    with open(f'results/error_rates_per_speaker.txt','w') as file:
        file.write(json.dumps(result_per_speaker_df, indent=4))

    # Data Visualization
    plot_statistics(result_per_speaker_df)


if __name__ == '__main__':
    # main()
    test()
