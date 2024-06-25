# Integrating Base Performance and Performance Differences in Automatic Speech Recognition Metrics
This repository contains the codebase for my BSc thesis titled "Integrating Performance Differences and Actual Performance in Automatic Speech Recognition Metrics" for the [CSE3000 Research Project 2024](https://github.com/TU-Delft-CSE/Research-Project) at the TU Delft. The project proposes a new bias metric that takes both performance difference and base performance into account.

The repository consists of multiple components:
- `asr_output_data.py`: handles the processing of the recognised output
- `bias_calculation.py`: handles the calculation of the bias, including the new metrics
- `filepath_manager.py`: handles file reading
- `process.py`: calculates performance metrics
- `visualize.py`: handles data visualisation

## Usage
Once the `config.json` file (see below) has been properly created, the program can be run by calling `python main.py`.


## The config.json File
This is where the information used by the Filepath manager (inspired by @kmjones) on what data the code should expect and where. This should include the following:

- ASR models: names of the ASR models under evaluation
- Speaker groups: names of the predefined demographic groups
- Speaking styles, each containing an id, name and abbreviation
- Filepaths to the extracted features. Expects one file per speaking style. The value of the speaking_style field should be equal to the corresponding speaking style's id.
- Filepaths to the ASR recognition output. A filepath template can be given. The one that is there at the moment expects the names of each necessary file to be derived from the ASR model name(s) and speaking style abbreviation(s).

For more information on the functionality, please check the relevant files in the `src` folder. 

