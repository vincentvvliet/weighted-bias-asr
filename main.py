from src.process import statistics_per_asr_model
from src.asr_performance_data import AsrPerformanceData
from src.filepath_manager import FilepathManager

def main():
    # Initialize dataframe creation
    filepath_manager = FilepathManager('config.json')
    asr_performance_data = AsrPerformanceData(filepath_manager=filepath_manager)

    # Read data
    speaking_style_index = 1
    data_frame = asr_performance_data.build_dataframe(speaking_style_index)

    # Data Processing
    for i, error_rate in enumerate(filepath_manager.error_rates):
        error_rate_name = data_frame.columns[i]

        statistics_per_asr_model(data_frame[error_rate], filepath_manager, error_rate_name, speaking_style_index)

    # Data visualization
    # TODO: implement


if __name__ == '__main__':
    main()
