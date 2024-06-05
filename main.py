import os
import pandas as pd
import numpy as np
from src.visualize import plot_histogram, plot_box_plot, plot_line_plot, combined_plots, combined_plots_2
from src.process import process_data_per_speaker_group, process_data_per_speech_type
from src.asr_performance_data import AsrPerformanceData
from src.filepath_manager import FilepathManager

def main():
    # Initialize dataframe creation
    filepath_manager = FilepathManager('config.json')
    asr_performance_data = AsrPerformanceData(filepath_manager=filepath_manager)

    # Read data
    data_frame = asr_performance_data.build_dataframe()

    # Data Processing
    for error_rate in filepath_manager.error_rates:
        error_rate_frame = preprocess_data(data_frame[error_rate])

        # TODO: Process new data
        # Process the data based on specific metric, input_type, and speech_type
        # process_data_per_speaker_group(error_rate_frame, metric='std', input_type='NoAug', speech_type='Read', error_rate=error_rate)

        # Process data per error_rate, per speech type
        # process_data_per_speech_type(error_rate_frame, metric='std', input_type='NoAug', speech_type='Read', error_rate=error_rate)

    # Data visualization
    # TODO: implement


def preprocess_data(df):
    """
    Drop NaN and infinite values.

    :param df: Pandas Dataframe to be processed
    :return: Preprocessed Dataframe
    """
    df = df.dropna()
    df = df[~df.isin([np.inf, -np.inf])]
    return df


if __name__ == '__main__':
    main()
