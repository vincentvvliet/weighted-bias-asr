import json


def process_output_per_group(df):
    substitutions = 0
    insertions = 0
    deletions = 0
    hits = 0
    total_words = 0

    # Iterate over file
    for index, row in df[1].iterrows():
        substitutions += row['Sub']
        insertions += row['Ins']
        deletions += row['Del']
        hits += row['Corr']
        total_words += row['# Wrd']

    # Calculate error rates
    wer = (substitutions + insertions + deletions) / total_words
    mer = 1 - (hits / (substitutions + insertions + deletions + hits))

    return {'WER': wer, 'MER': mer, }


def process_output(df):
    total_substitutions = 0
    total_insertions = 0
    total_deletions = 0
    total_hits = 0
    total_words = 0
    wer_per_speaker = []
    mer_per_speaker = []

    # Iterate over file
    for index, row in df[1].iterrows():
        total_substitutions = row['Sub']
        total_insertions = row['Ins']
        total_deletions = row['Del']
        total_hits = row['Corr']
        total_words = row['# Wrd']

        # Calculate error rates for current speaker
        wer_per_speaker.append((row['Sub'] + row['Ins'] + row['Del']) / row['# Wrd'])
        mer_per_speaker.append((row['Sub'] + row['Ins'] + row['Del']) / (row['Sub'] + row['Ins'] + row['Del'] + row['Corr']))

    # Calculate total error rates
    total_wer = (total_substitutions + total_insertions + total_deletions) / total_words
    total_mer = 1 - (total_hits / (total_substitutions + total_insertions + total_deletions + total_hits))

    result_per_speaker_df = {'WER': wer_per_speaker, 'MER': mer_per_speaker, }
    result_per_group_df = {'WER': total_wer, 'MER': total_mer, }

    # Write error rates to file
    with open(f'results/error_rates_per_speaker.txt', 'w') as file:
        file.write(json.dumps(result_per_speaker_df, indent=4))

    with open(f'results/error_rates_per_group.txt', 'w') as file:
        file.write(json.dumps(result_per_group_df, indent=4))

    return result_per_speaker_df, result_per_group_df
