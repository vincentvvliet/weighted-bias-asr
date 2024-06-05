import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_histogram(data_frames, error_rate='WER', input_type='NoAug', speech_type='Read'):
    combined_values = []

    for file_path, df in data_frames.items():
        if input_type in file_path and speech_type in file_path:
            combined_values.append(df['Value'])

    if combined_values:
        combined_series = pd.concat(combined_values, ignore_index=True)

        plt.figure(figsize=(10, 6))
        plt.hist(combined_series, bins=30, edgecolor='k', alpha=0.7)
        plt.title(f'Histogram of {error_rate} {input_type} {speech_type} Values')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.savefig(f'plots/histogram-{error_rate}-{input_type}-{speech_type}.png')
        plt.close()
    else:
        print(f'No data found for {input_type} {speech_type}.')


def plot_box_plot(data_frames, error_rate='WER', input_type='NoAug', speech_type='Read'):
    combined_values = []

    for file_path, df in data_frames.items():
        if input_type in file_path and speech_type in file_path:
            combined_values.append(df.assign(file=file_path))

    if combined_values:
        combined_df = pd.concat(combined_values, ignore_index=True)

        plt.figure(figsize=(12, 6))
        sns.boxplot(x='file', y='Value', data=combined_df)
        plt.xticks(rotation=90)
        plt.title(f'Box Plot of {error_rate} {input_type} {speech_type} Values')
        plt.xlabel('Files')
        plt.ylabel('Values')
        plt.grid(True)
        plt.savefig(f'plots/boxplot-{error_rate}-{input_type}-{speech_type}.png')
        plt.close()
    else:
        print(f'No data found for {input_type} {speech_type}.')


def plot_line_plot(data_frames, error_rate='WER', input_type='NoAug', speech_type='Read'):
    combined_values = []

    for file_path, df in data_frames.items():
        if input_type in file_path and speech_type in file_path:
            combined_values.append(df.assign(file=file_path))

    if combined_values:
        combined_df = pd.concat(combined_values, ignore_index=True)

        plt.figure(figsize=(12, 6))
        sns.lineplot(x='file', y='Value', data=combined_df)
        plt.xticks(rotation=90)
        plt.title(f'Line Plot of {error_rate} {input_type} {speech_type} Values')
        plt.xlabel('Files')
        plt.ylabel('Values')
        plt.savefig(f'plots/lineplot-{error_rate}-{input_type}-{speech_type}.png')
        plt.close()
    else:
        print(f'No data found for {input_type} {speech_type}.')


def combined_plots(data_frames, error_rate='WER', input_type='NoAug', speech_type='Read'):
    combined_values = []

    for file_path, df in data_frames.items():
        if input_type in file_path and speech_type in file_path:
            combined_values.append(df.assign(file=file_path))

    if combined_values:
        combined_df = pd.concat(combined_values, ignore_index=True)

        fig, axs = plt.subplots(2, 1, figsize=(12, 12))

        # Histogram
        sns.histplot(combined_df['Value'], bins=30, kde=True, ax=axs[0])
        axs[0].set_title(f'Histogram of {error_rate} {input_type} {speech_type} Values')
        axs[0].set_xlabel('Values')
        axs[0].set_ylabel('Frequency')

        # Box plot
        sns.boxplot(x='file', y='Value', data=combined_df, ax=axs[1])
        axs[1].set_title(f'Box Plot of {error_rate} {input_type} {speech_type} Values')
        axs[1].set_xlabel('Files')
        axs[1].set_ylabel('Values')
        axs[1].tick_params(axis='x', rotation=90)

        plt.tight_layout()
        plt.savefig(f'plots/combined_plot-{error_rate}-{input_type}-{speech_type}.png')
        plt.close()
    else:
        print(f'No data found for {input_type} {speech_type}.')


# TODO: fix key error, find better way of organizing data
def combined_plots_2(data_frames, error_rate, input_types, speech_types):
    fig, axs = plt.subplots(len(input_types), len(speech_types), figsize=(15, 10))

    for i, input_type in enumerate(input_types):
        for j, speech_type in enumerate(speech_types):
            key = f'{error_rate}_{input_type}_{speech_type}'
            print(f'Plotting {key} for {speech_type}')
            df = data_frames.get(key)
            if df is not None:
                axs[i, j].hist(df['Value'], bins=30, alpha=0.7, edgecolor='k')
                axs[i, j].set_title(f'{error_rate} {input_type} {speech_type}')
            else:
                print(f'No data found for {input_type} {speech_type}.')
                axs[i, j].axis('off')  # Hide subplot if DataFrame is None

    fig.suptitle('Combined Histograms', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'plots/combined_plot_2-{error_rate}.png')
    plt.close()