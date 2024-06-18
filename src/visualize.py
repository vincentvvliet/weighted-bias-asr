import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


def plot_statistics_per_error_rate(data):
    # Convert the JSON data into a pandas DataFrame
    rows = []
    for key, value in data.items():
        model, group, speaking_style = key.split('_')
        for rate_type in ['WER']:
            rows.append([model, group, speaking_style, rate_type, value[rate_type]])

    df = pd.DataFrame(rows, columns=['Model', 'Group', 'SpeakingStyle', 'RateType', 'Rates'])

    # Compute statistics for each combination of Model, Group, SpeakingStyle, and RateType
    stats = df.explode('Rates').groupby(['Model', 'Group', 'SpeakingStyle', 'RateType'])['Rates'].agg(
        ['median', 'std', 'max', 'min']).reset_index()

    # Plotting
    metrics = ['median', 'std', 'max', 'min']
    rate_types = ['WER']
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

# TODO: output different every time
# TODO: absolute seems smaller than relative?
def plot_performance_difference(performance_differences_abs, performance_differences_rel, fpm):
    # Convert the nested dictionaries into a DataFrame for easier plotting
    def convert_to_dataframe(performance_differences):
        records = []
        for model, groups in performance_differences.items():
            for group, diffs in groups.items():
                for diff in diffs:
                    records.append({
                        'Model': model,
                        'Group': group,
                        'SpeakingStyle': diff['SpeakingStyle'],
                        'PerformanceDiff': diff['PerformanceDiff'],
                        'RateType': diff['RateType'],
                        'BaselineType': diff['BaselineType'],
                    })
        return pd.DataFrame(records)

    df_abs = convert_to_dataframe(performance_differences_abs)
    df_rel = convert_to_dataframe(performance_differences_rel)

    # Create a combined column for Group and SpeakingStyle
    df_abs['GroupSpeakingStyle'] = df_abs['Group'] + '-' + df_abs['SpeakingStyle']
    df_rel['GroupSpeakingStyle'] = df_rel['Group'] + '-' + df_rel['SpeakingStyle']

    # Create a combined column for Model and SpeakingStyle for hue
    df_abs['ModelSpeakingStyle'] = df_abs['Model'] + '-' + df_abs['BaselineType']
    df_rel['ModelSpeakingStyle'] = df_rel['Model'] + '-' + df_rel['BaselineType']

    # Define the color palette to ensure similar colors for same models
    palette = {
        'NoAug-min': 'skyblue',
        'NoAug-norm': 'deepskyblue',
        'SpAug-min': 'lightcoral',
        'SpAug-norm': 'indianred',
        'SpSpecAug-min': 'lightgreen',
        'SpSpecAug-norm': 'seagreen'
    }

    # Create the subplots
    fig, axes = plt.subplots(2, 1, figsize=(18, 12), sharex=True)

    # Plot for absolute performance differences
    sns.barplot(data=df_abs, x='GroupSpeakingStyle', y='PerformanceDiff', hue='ModelSpeakingStyle', ax=axes[0], palette=palette, errorbar=None)
    axes[0].set_ylabel('Bias (Absolute)')
    axes[0].grid(True)
    axes[0].set_ylim(0, 1)

    # Plot for relative performance differences
    sns.barplot(data=df_rel, x='GroupSpeakingStyle', y='PerformanceDiff', hue='ModelSpeakingStyle', ax=axes[1], palette=palette, errorbar=None)
    axes[1].set_ylabel('Bias (Relative)')
    axes[1].grid(True)
    axes[1].set_ylim(0, 5)

    # Set common x-label
    axes[1].set_xlabel('Group')

    # Adjust the legend
    axes[0].legend(title='Model and Bias Metric', bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[1].legend(title='Model and Bias Metric', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Tight layout for better spacing
    plt.tight_layout()

    # Save the figure
    plt.savefig('plots/performance_differences_combined.png')
    plt.close()


def plot_wpb(wpb_values):
    models = ['NoAug', 'SpSpecAug', 'SpAug']
    groups = ['DC', 'NnT', 'DT', 'NnA', 'DOA']

    x = np.arange(len(groups))
    width = 0.2

    # Colorblind-friendly palette
    colors = sns.color_palette("colorblind", n_colors=len(models))

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, wpb_values['NoAug'].values(), width, label='NoAug', color=colors[0])
    rects2 = ax.bar(x, wpb_values['SpSpecAug'].values(), width, label='SpSpecAug', color=colors[1])
    rects3 = ax.bar(x + width, wpb_values['SpAug'].values(), width, label='SpAug', color=colors[2])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('WPB Values')
    ax.set_title('Weighted Performance Bias by Model and Group')
    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.legend()
    ax.grid(True)
    ax.yaxis.grid(True, linestyle='--', which='both', color='grey', alpha=0.7)

    # Tight layout for better spacing
    plt.tight_layout()

    # Save the figure
    plt.savefig('plots/wpb.png')
    plt.close()


def plot_iwpb(iwpb_values):
    models = ['NoAug', 'SpSpecAug', 'SpAug']
    groups = ['DC', 'NnT', 'DT', 'NnA', 'DOA']

    x = np.arange(len(groups))
    width = 0.2

    # Colorblind-friendly palette
    colors = sns.color_palette("colorblind", n_colors=len(models))

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, iwpb_values['NoAug'].values(), width, label='NoAug', color=colors[0])
    rects2 = ax.bar(x, iwpb_values['SpSpecAug'].values(), width, label='SpSpecAug', color=colors[1])
    rects3 = ax.bar(x + width, iwpb_values['SpAug'].values(), width, label='SpAug', color=colors[2])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('IWPB Values')
    ax.set_title('Intergroup Weighted Performance Bias by Model and Group')
    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.legend()
    ax.grid(True)
    ax.yaxis.grid(True, linestyle='--', which='both', color='grey', alpha=0.7)

    # Tight layout for better spacing
    plt.tight_layout()

    # Save the figure
    plt.savefig('plots/iwpb.png')
    plt.close()

