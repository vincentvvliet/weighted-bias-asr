import pandas as pd
import json


def get_performance_differences(df, fpm):
    performance_diff_abs_min = performance_difference(df, fpm, baseline_type='min', diff_type='absolute')
    performance_diff_abs_norm = performance_difference(df, fpm, baseline_type='norm', diff_type='absolute')
    performance_diff_rel_min = performance_difference(df, fpm, baseline_type='min', diff_type='relative')
    performance_diff_rel_norm = performance_difference(df, fpm, baseline_type='norm', diff_type='relative')

    # Combine absolute values and relative values seperately
    performance_diff_combined_abs = combine_performance_differences(performance_diff_abs_min, performance_diff_abs_norm,
                                                                    {}, {})
    performance_diff_combined_rel = combine_performance_differences({}, {}, performance_diff_rel_min,
                                                                    performance_diff_rel_norm)

    bias = {'abs_min': convert_to_bias_values(performance_diff_abs_min.copy()),
            'abs_norm': convert_to_bias_values(performance_diff_abs_norm.copy()),
            'rel_min': convert_to_bias_values(performance_diff_rel_min.copy()),
            'rel_norm': convert_to_bias_values(performance_diff_rel_norm.copy())}

    with open(f'results/bias/old/performance_difference_values.json','w') as file:
        json.dump(bias, file)


    with open(f'results/bias/old/performance_differences_combined_abs.json','w') as file:
        file.write(json.dumps(performance_diff_combined_abs, indent=4))

    with open(f'results/bias/old/performance_differences_combined_rel.json','w') as file:
        file.write(json.dumps(performance_diff_combined_rel, indent=4))

    # Return combined the performance differences
    return performance_diff_combined_abs, performance_diff_combined_rel


def convert_to_bias_values(df):
    for model in df.keys():
        for group in df[model].keys():
            df[model][group] = df[model][group][0]['PerformanceDiff']

    return df


# TODO: Fix combine
def combine_performance_differences(abs_min, abs_norm, rel_min, rel_norm):
    combined = {}

    # Collect all model keys from all dictionaries
    all_models = set(abs_min.keys()) | set(abs_norm.keys()) | set(rel_min.keys()) | set(rel_norm.keys())

    for model in all_models:
        combined[model] = {}

        # Collect all group keys for each model from all dictionaries
        all_groups = (set(abs_min.get(model, {}).keys()) |
                      set(abs_norm.get(model, {}).keys()) |
                      set(rel_min.get(model, {}).keys()) |
                      set(rel_norm.get(model, {}).keys()))

        for group in all_groups:
            combined[model][group] = (
                    abs_min.get(model, {}).get(group, []) +
                    abs_norm.get(model, {}).get(group, []) +
                    rel_min.get(model, {}).get(group, []) +
                    rel_norm.get(model, {}).get(group, [])
            )

    return combined

def performance_difference(df, fpm, baseline_type='min', diff_type='absolute'):
    performance_difference_df = {model: {} for model in fpm.asr_models}
    rows = []

    for rate_type in fpm.error_rates:
        for key, value in df.items():
            model, group, speaking_style = key.split('_')
            rows.append([model, group, speaking_style, rate_type, value[rate_type]])

    df = pd.DataFrame(rows, columns=['Model', 'Group', 'SpeakingStyle', 'RateType', 'Rates'])

    for model in fpm.asr_models:
        model_df = df[df['Model'] == model]

        for rate_type in fpm.error_rates:
            rate_df = model_df[model_df['RateType'] == rate_type]

            for speaking_style in fpm.speaking_style_folders:
                style_df = rate_df[rate_df['SpeakingStyle'] == speaking_style]

                # Determine baseline performance
                if baseline_type == 'min':
                    baseline_performance = style_df['Rates'].min()
                elif baseline_type == 'norm':
                    baseline_performance = style_df['Rates'].mean()
                else:
                    raise ValueError("Invalid baseline_type. Use 'min' or 'norm'.")

                for _, row in style_df.iterrows():
                    current_performance = row['Rates']
                    group = row['Group']

                    if diff_type == 'absolute':
                        performance_diff = current_performance - baseline_performance
                    elif diff_type == 'relative':
                        performance_diff = (current_performance - baseline_performance) / baseline_performance
                    else:
                        raise ValueError("Invalid diff_type. Use 'absolute' or 'relative'.")

                    if group not in performance_difference_df[model]:
                        performance_difference_df[model][group] = []

                    performance_difference_df[model][group].append({
                        "RateType": rate_type,
                        "SpeakingStyle": speaking_style,
                        "PerformanceDiff": performance_diff,
                        "BasePerformance": current_performance,
                        "BaselinePerformance": baseline_performance,
                        "BaselineType": baseline_type
                    })

    with open(f'results/bias/old/performance_difference_{baseline_type}_{diff_type}.json','w') as file:
        file.write(json.dumps(performance_difference_df, indent=4))

    return performance_difference_df


def calculate_weighted_performance_bias(df, w1, w2, bp):
    """
    Calculate Weighted Performance Bias (WPB).

    :param df: The performance difference dataframe.
    :param w1: Weight for performance difference.
    :param w2: Weight for base performance.
    :param bp: Baseline performance.
    :return: Weighted Performance Bias (WPB) for each model and group.
    """
    weighted_bias = {model: {} for model in df.keys()}

    for model in df.keys():
        for group in df[model].keys():
            n = len(df[model][group])
            total_bias = 0
            for record in df[model][group]:
                pd_i = abs(record['PerformanceDiff'])
                base_i = record['BasePerformance']
                total_bias += (w1 * (pd_i / bp)) + (w2 * base_i)

            weighted_bias[model][group] = total_bias / n

    with open(f'results/bias/new/weighted_performance_bias.txt', 'w') as file:
        file.write(json.dumps(weighted_bias, indent=4))

    return weighted_bias


def calculate_intergroup_weighted_performance_bias(df, w1, w2, bp):
    """
    Calculate Intergroup Weighted Performance Bias (IWPB).

    :param df: The performance difference dataframe.
    :param w1: Weight for performance difference.
    :param w2: Weight for base performance.
    :param bp: Baseline performance.
    :return: Intergroup Weighted Performance Bias (IWPB) for each model and group.
    """
    intergroup_weighted_bias = {model: {} for model in df.keys()}

    for model in df.keys():
        groups = list(df[model].keys())
        n = len(groups)

        for i in range(n):
            group_i = groups[i]
            base_i = df[model][group_i][0]['BasePerformance']  # Base performance for group i
            total_bias = 0
            count = 0

            for j in range(n):
                if i != j:
                    group_j = groups[j]
                    base_j = df[model][group_j][0]['BasePerformance']  # Base performance for group j
                    pd_ij = abs(base_i - base_j)
                    total_bias += (w1 * (pd_ij / bp)) + (w2 * base_i)
                    count += 1

            intergroup_weighted_bias[model][group_i] = total_bias / count if count != 0 else 0

    with open(f'results/bias/new/intergroup_weighted_performance_bias.txt', 'w') as file:
        file.write(json.dumps(intergroup_weighted_bias, indent=4))

    return intergroup_weighted_bias


def calculate_total_intergroup_weighted_performance_bias(df, w1, w2, bp):
    """
    Calculate total Intergroup Weighted Performance Bias (IWPB).

    :param df: The performance difference dataframe.
    :param w1: Weight for performance difference.
    :param w2: Weight for base performance.
    :param bp: Baseline performance.
    :return: total Intergroup Weighted Performance Bias (IWPB) for each model.
    """
    total_intergroup_weighted_bias = {model: 0 for model in df.keys()}

    for model in df.keys():
        groups = list(df[model].keys())
        n = len(groups)
        total_bias = 0

        for i in range(n):
            base_i = df[model][groups[i]][0]['BasePerformance']  # Base performance for group i

            for j in range(n):
                if i != j:
                    base_j = df[model][groups[j]][0]['BasePerformance']  # Base performance for group j
                    pd_ij = abs(base_i - base_j)
                    total_bias += (w1 * (pd_ij / bp)) + (w2 * base_i)

        total_intergroup_weighted_bias[model] = total_bias / (n * (n - 1))

    return total_intergroup_weighted_bias