import json

from src.asr_output_data import AsrOutputData
from src.bias_calculation import get_performance_differences, calculate_weighted_performance_bias, \
    calculate_intergroup_weighted_performance_bias, calculate_total_intergroup_weighted_performance_bias
from src.filepath_manager import FilepathManager
from src.process import process_wer
from src.visualize import plot_statistics_per_error_rate, plot_performance_difference, plot_iwpb, plot_wpb, \
    plot_iwpb_simulation, plot_iwpb_heatmap, plot_iwpb_3d


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
                result_per_speaker_df[key], result_per_group_df[key] = process_wer(data)

    # Write error rates to file
    with open(f'results/error_rates/error_rates_per_speaker.txt', 'w') as file:
        file.write(json.dumps(result_per_speaker_df, indent=4))

    with open(f'results/error_rates/error_rates_per_group.txt', 'w') as file:
        file.write(json.dumps(result_per_group_df, indent=4))

    # Bias Calculation
    performance_differences_abs, performance_differences_rel = get_performance_differences(result_per_group_df, filepath_manager)

    # New bias metrics calculation
    w1, w2, bp = 0.5, 0.5, 1
    weighted_bias = calculate_weighted_performance_bias(performance_differences_abs, w1, w2, bp)
    intergroup_weighted_bias = calculate_intergroup_weighted_performance_bias(performance_differences_abs,w1, w2, bp)
    total_intergroup_weighted_bias = calculate_total_intergroup_weighted_performance_bias(performance_differences_abs, w1, w2, bp)

    # Data Visualization
    # Plot the combined performance differences
    plot_performance_difference(performance_differences_abs, performance_differences_rel, filepath_manager)

    # Plot statistics per error rates
    plot_statistics_per_error_rate(result_per_speaker_df)

    # Plot the weighted performance bias
    plot_wpb(weighted_bias)

    # Plot the intergroup weighted performance bias
    plot_iwpb(intergroup_weighted_bias)

    # Simulate weights
    plot_iwpb_simulation(performance_differences_abs, bp)
    plot_iwpb_heatmap(performance_differences_abs, bp)
    plot_iwpb_3d(performance_differences_abs, bp)

if __name__ == '__main__':
    main()

