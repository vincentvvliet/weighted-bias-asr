from src.process import statistics_per_asr_model
from src.asr_performance_data import AsrPerformanceData
from src.filepath_manager import FilepathManager
from src.bias_calculation import performance_difference, weighted_bias_metric, weighted_bias_metric_2

def main():
    # Initialize dataframe creation
    filepath_manager = FilepathManager('config.json')
    asr_performance_data = AsrPerformanceData(filepath_manager=filepath_manager)

    # Read data for both Read and HMI speaking style
    for speaking_style_index in range(0, 2):
        data_frame = asr_performance_data.build_dataframe(speaking_style_index)

        # Data Processing per error rate
        for i, error_rate in enumerate(filepath_manager.error_rates):
            error_rate_name = data_frame.columns[i]

            statistics_per_asr_model(data_frame[error_rate], filepath_manager, error_rate_name, speaking_style_index)
            print("Successfully processed for speaking style index " + str(speaking_style_index) + " and error rate " + str(error_rate_name))

            # Bias Calculation
            performance_difference(data_frame[error_rate], filepath_manager, 'min', 'absolute')
            performance_difference(data_frame[error_rate], filepath_manager, 'min', 'relative')

            # Data visualization
            # TODO: implement



if __name__ == '__main__':
    main()
