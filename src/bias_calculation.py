import pandas as pd
import json


# TODO: Add comments
def get_performance_differences(df, fpm):
    performance_diff_abs_min = performance_difference(df, fpm, baseline_type='min', diff_type='absolute')
    performance_diff_abs_avg = performance_difference(df, fpm, baseline_type='norm', diff_type='absolute')
    performance_diff_rel_min = performance_difference(df, fpm, baseline_type='min', diff_type='relative')
    performance_diff_rel_avg = performance_difference(df, fpm, baseline_type='norm', diff_type='relative')

    # Combine absolute values and relative values seperately
    performance_diff_combined_abs = combine_performance_differences(performance_diff_abs_min, performance_diff_abs_avg,
                                                                    {}, {})
    performance_diff_combined_rel = combine_performance_differences({}, {}, performance_diff_rel_min,
                                                                    performance_diff_rel_avg)

    with open(f'results/performance_differences_combined_abs.txt','w') as file:
        file.write(json.dumps(performance_diff_combined_abs, indent=4))

    with open(f'results/performance_differences_combined_rel.txt','w') as file:
        file.write(json.dumps(performance_diff_combined_rel, indent=4))

    # Return combined the performance differences
    return performance_diff_combined_abs, performance_diff_combined_rel


def combine_performance_differences(abs_min, abs_avg, rel_min, rel_avg):
    combined = {}

    # Collect all model keys from all dictionaries
    all_models = set(abs_min.keys()) | set(abs_avg.keys()) | set(rel_min.keys()) | set(rel_avg.keys())

    for model in all_models:
        combined[model] = {}

        # Collect all group keys for each model from all dictionaries
        all_groups = (set(abs_min.get(model, {}).keys()) |
                      set(abs_avg.get(model, {}).keys()) |
                      set(rel_min.get(model, {}).keys()) |
                      set(rel_avg.get(model, {}).keys()))

        for group in all_groups:
            combined[model][group] = (
                    abs_min.get(model, {}).get(group, []) +
                    abs_avg.get(model, {}).get(group, []) +
                    rel_min.get(model, {}).get(group, []) +
                    rel_avg.get(model, {}).get(group, [])
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
                        'RateType': rate_type,
                        'SpeakingStyle': speaking_style,
                        'PerformanceDiff': performance_diff,
                        'BaselineType': baseline_type
                    })

    with open(f'results/performance_difference_{baseline_type}_{diff_type}.txt','w') as file:
        file.write(json.dumps(performance_difference_df, indent=4))

    return performance_difference_df

def weighted_bias_metric():
    # TODO: Implement
    return


def weighted_bias_metric_2():
    # TODO: Implement
    return