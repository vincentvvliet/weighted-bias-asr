import json

from src.asr_output_data import AsrOutputData
from src.bias_calculation import get_performance_differences, calculate_weighted_performance_bias, \
    calculate_intergroup_weighted_performance_bias, calculate_total_intergroup_weighted_performance_bias, \
    calculate_overall_weighted_performance_bias, calculate_overall_intergroup_weighted_performance_bias
from src.filepath_manager import FilepathManager
from src.process import read_data
from src.visualize import plot_statistics_per_error_rate, plot_performance_difference, plot_iwpb, plot_wpb, \
    plot_iwpb_simulation, plot_iwpb_heatmap, plot_wpb_simulation


def main():
    print("Retrieving data...")
    filepath_manager = FilepathManager('config.json')
    asr_output_data = AsrOutputData(filepath_manager=filepath_manager)

    result_per_speaker_df = {}
    result_per_group_df = {}

    # Read error-data for both Read and HMI speaking style
    print("Reading data...")
    read_data(asr_output_data, filepath_manager, result_per_group_df, result_per_speaker_df)

    # Write error rates to file
    with open(f'results/error_rates/error_rates_per_speaker.txt', 'w') as file:
        file.write(json.dumps(result_per_speaker_df, indent=4))

    with open(f'results/error_rates/error_rates_per_group.txt', 'w') as file:
        file.write(json.dumps(result_per_group_df, indent=4))

    # Bias Calculation
    print("Calculating performance differences...")
    performance_differences_abs, performance_differences_rel = get_performance_differences(result_per_group_df, filepath_manager)

    # Simulate weights
    plot_iwpb_heatmap(performance_differences_abs)
    print("Performing IWPB simulation...")
    iwpb_w1 = (plot_iwpb_simulation(performance_differences_abs))
    iwpb_w2 = 1 - iwpb_w1

    print("Performing WPB simulation...")
    wpb_w1 = (plot_wpb_simulation(performance_differences_abs))
    wpb_w2 = 1 - wpb_w1

    # Override weights, if necessary
    # iwpb_w1 = iwpb_w2 = wpb_w1 = wpb_w2 = 0.5

    # New bias metrics calculation
    print("Calculating bias via new bias metrics...")
    weighted_bias = calculate_weighted_performance_bias(performance_differences_abs, wpb_w1, wpb_w2)
    overall_bias = calculate_overall_weighted_performance_bias(performance_differences_abs, wpb_w1, wpb_w2, filepath_manager)
    intergroup_weighted_bias = calculate_intergroup_weighted_performance_bias(performance_differences_abs,iwpb_w1, iwpb_w2)
    overall_intergroup_weighted_bias = calculate_overall_intergroup_weighted_performance_bias(performance_differences_abs, iwpb_w1, iwpb_w2, filepath_manager)
    total_intergroup_weighted_bias = calculate_total_intergroup_weighted_performance_bias(performance_differences_abs, iwpb_w1, iwpb_w2)

    # Data Visualization
    print("Starting data visualization...")

    # Plot the combined performance differences
    plot_performance_difference(performance_differences_abs, performance_differences_rel)

    # Plot statistics per error rates
    plot_statistics_per_error_rate(result_per_speaker_df)

    # Plot the weighted performance bias
    plot_wpb(weighted_bias, filepath_manager, wpb_w1)

    # Plot the intergroup weighted performance bias
    plot_iwpb(intergroup_weighted_bias, filepath_manager, iwpb_w1)

if __name__ == '__main__':
    main()
    print("Successfully terminated.")

