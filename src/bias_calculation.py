import pandas as pd

# TODO: Add comments

def performance_difference(df, fpm, baseline_type, type):
    df = pd.Series(data=df, index=fpm.asr_models)
    for model in fpm.asr_models:
        model_df = pd.DataFrame(df[model])
        performance_diff = pd.DataFrame() # TODO: add performance difference to dataframe
        baseline_performance = model_df.min() if baseline_type == 'min' else model_df.mean()
        for item in model_df.items():
            if type == 'absolute':
                # bias = bias_i - baseline_performance
                return
            elif type == 'relative':
                # bias = (bias_i - baseline_performance) / baseline_performance
                return

    return


def weighted_bias_metric():
    # TODO: Implement
    return

def weighted_bias_metric_2():
    # TODO: Implement
    return