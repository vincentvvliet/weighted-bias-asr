import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


def plot_statistics(data):
    # Convert the JSON data into a pandas DataFrame
    rows = []
    for key, value in data.items():
        model, group, speaking_style = key.split('_')
        for rate_type in ['WER', 'MER']:
            rows.append([model, group, speaking_style, rate_type, value[rate_type]])

    df = pd.DataFrame(rows, columns=['Model', 'Group', 'SpeakingStyle', 'RateType', 'Rates'])

    # Compute statistics for each combination of Model, Group, SpeakingStyle, and RateType
    stats = df.explode('Rates').groupby(['Model', 'Group', 'SpeakingStyle', 'RateType'])['Rates'].agg(
        ['median', 'std', 'max', 'min']).reset_index()

    # Plotting
    metrics = ['median', 'std', 'max', 'min']
    rate_types = ['WER', 'MER']
    groups = df['Group'].unique()
    models = df['Model'].unique()

    for rate_type in rate_types:
        fig, axes = plt.subplots(1, len(metrics), figsize=(20, 5), sharey=True)
        fig.suptitle(f'Statistics for {rate_type}', fontsize=16)

        bar_width = 0.2
        for i, metric in enumerate(metrics):
            ax = axes[i]
            ax.set_title(metric.capitalize())

            x = np.arange(len(models))
            for j, group in enumerate(groups):
                group_stats = stats[(stats['RateType'] == rate_type) & (stats['Group'] == group)]
                group_stats = group_stats.groupby('Model').agg({metric: 'mean'}).reindex(models).reset_index()
                bar_positions = x + (j - len(groups) / 2) * bar_width

                ax.bar(bar_positions, group_stats[metric], bar_width, label=group)

            ax.set_xticks(x)
            ax.set_xticklabels(models)
            ax.set_xlabel('Model')
            if i == 0:
                ax.set_ylabel('Value')
            ax.legend(title='Group')

        plt.tight_layout()
        plt.subplots_adjust(top=0.85)
        plt.savefig(f'plots/histogram-statistics-{rate_type}.png')
        plt.close()