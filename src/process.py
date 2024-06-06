import pandas as pd
import numpy as np
import json


def preprocess_data(df):
    """
    Drop NaN and infinite values.

    :param df: Pandas Dataframe to be processed
    :return: Preprocessed Dataframe
    """
    df = df.dropna()
    df = df[~df.isin([np.inf, -np.inf])]
    return df


def convert_max_min_to_range(result):
    for model in result:
        max_value = result[model].pop('max', None)
        min_value = result[model].pop('min', None)
        if max_value is not None and min_value is not None:
            result[model]['range'] = f'{max_value}-{min_value}'


def statistics_per_asr_model(df, fpm, error_rate, speaking_style):
    df = pd.Series(data=df, index=fpm.asr_models)

    result = {'NoAug': {}, 'SpAug': {}, 'SpSpecAug': {}, 'Whisper': {}, 'FT-Wpr': {}}
    metrics = ['median', 'std', 'max', 'min']

    for model in fpm.asr_models:
        model_df = pd.DataFrame(df[model])
        model_df = preprocess_data(model_df)
        for metric in metrics:
            metric_func = getattr(pd.Series, metric)
            result[model][metric] = metric_func(model_df, axis=0).tolist()[0]

    convert_max_min_to_range(result)

    with open(f'results/statistics-{fpm.speaking_style_folders[speaking_style]}-{error_rate}.txt', 'w') as file:
        file.write(json.dumps(result, indent=4))
