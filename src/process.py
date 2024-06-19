def read_data(asr_output_data, filepath_manager, result_per_group_df, result_per_speaker_df):
    for speaking_style_index in range(0, 2):
        data_frame = asr_output_data.build_dataframe(speaking_style_index)

        for model in filepath_manager.asr_models:
            for _, data in data_frame[model].items():
                group = data[0]
                key = model + '_' + group + '_' + filepath_manager.speaking_style_folders[speaking_style_index]

                # Process model output data
                result_per_speaker_df[key], result_per_group_df[key] = process_wer(data)

def process_wer(df):
    total_substitutions = 0
    total_insertions = 0
    total_deletions = 0
    total_words = 0
    wer_per_speaker = []

    # Iterate over file
    for index, row in df[1].iterrows():
        total_substitutions = row['Sub']
        total_insertions = row['Ins']
        total_deletions = row['Del']
        total_words = row['# Wrd']

        # Calculate error rates for current speaker
        wer_per_speaker.append((row['Sub'] + row['Ins'] + row['Del']) / row['# Wrd'])

    # Calculate total error rates
    total_wer = (total_substitutions + total_insertions + total_deletions) / total_words

    result_per_speaker_df = {'WER': wer_per_speaker }
    result_per_group_df = {'WER': total_wer }

    return result_per_speaker_df, result_per_group_df


def process_output(df):
    # Processes all relevant error rates, but since decision has been made to solely use WER, this remains unused.
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

    return result_per_speaker_df, result_per_group_df
