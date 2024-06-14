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

        bar_width = 0.15
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

            # Set the same y-axis range for all subplots within the same plot
            for ax in axes:
                ax.set_ylim(0, 1)

        plt.tight_layout()
        plt.subplots_adjust(top=0.85)
        plt.savefig(f'plots/histogram-statistics-{rate_type}.png')
        plt.close()

def plot_performance_difference(abs_diff, rel_diff, fpm):
    fig, axes = plt.subplots(2, 1, figsize=(20, 12), sharex=True)

    for diff_type, ax, diff_data in zip(['absolute', 'relative'], axes, [abs_diff, rel_diff]):
        rows = []
        for model, groups in diff_data.items():
            for group, data in groups.items():
                for item in data:
                    rows.append([model, group, item['SpeakingStyle'], item['RateType'], item['PerformanceDiff'], item['BaselineType']])

        df = pd.DataFrame(rows, columns=['Model', 'Group', 'SpeakingStyle', 'RateType', 'PerformanceDiff', 'BaselineType'])

        # Create a new column for combined group and speaking style for better visualization
        df['GroupModelStyle'] = df['Model'] + '-' + df['SpeakingStyle']

        sns.barplot(data=df, x='Group', y='PerformanceDiff', hue='GroupModelStyle', ax=ax, ci=None)
        ax.set_title(f'Bias ({diff_type.capitalize()})')
        ax.set_ylabel('Bias (Difference)' if diff_type == 'absolute' else 'Bias (Relative)')

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, title='Model-SpeakingStyle', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    plt.tight_layout()
    plt.savefig(f'plots/performance_differences_1.png')
    plt.show()
