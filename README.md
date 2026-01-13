
# README — Magnus Time Prediction
## Predicting Human Thinking Time in Chess
### An empirical study based on Magnus Carlsen’s blitz games

## Project Overview

Modern chess engines achieve superhuman strength but fail to reproduce essential aspects of human behavior, particularly the temporal dynamics of decision-making. While recent research has focused on predicting human moves and playing style, the time humans spend thinking before playing a move remains largely unexplored.

This project investigates whether human thinking time can be predicted empirically from real chess game data. Focusing on blitz games played by Magnus Carlsen, we construct machine learning models to predict the time spent on individual moves using information available in real time (position, game phase, time pressure, and game dynamics).

The long-term goal is to contribute to more human-aligned chess AI systems, by integrating realistic time management into imitation-based engines and educational tools.

## Repository Structure

```graphql
magnus-time-prediction/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── README.md          # Instructions to obtain raw data
│   └── raw/            # Here is the folder where the data must be 
│
├── src/
│   ├── data_loading/      # PGN parsing and dataset construction
│   ├── feature_engineering/ # Feature extraction
│   ├── models/            # Model training (Random Forest, Neural Networks)
│   └── utils/             # Configuration, I/O, plotting utilities
│
├── notebooks/
│   ├── 01_data_processing.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_website_sample.ipynb
│
├── results/
│   ├── figures/           # Generated plots and board visualizations
│   ├── metrics/           # Model evaluation results
│   └── models/            # Saved models (excluded from GitHub if large)
```


## Data 

Due to size constraints, the datasets used in this project are not included directly in the GitHub repository.
They are publicly available on Zenodo.

### Zenodo archive

The Zenodo repository contains two compressed archives:

1. **Raw game data**
   - `magnus_carlsen_blitz_pgns.zip`  
   This archive contains 250 PGN files corresponding to blitz games played by Magnus Carlsen on chess.com. 

2. **Processed datasets**
   - `magnus_time_prediction_dataset.zip`  
   This archive contains the following CSV files, intended to be placed in `results/metrics/`:

   - `data_magnus_moves.csv`  
     The full move-level dataset used for training and evaluating the models.

   - `data_sample_magnus.csv`  
     A fixed small sample dataset used for rapid experimentation and visualization, avoiding repeated random sampling.

   - `data_shuffled_magnus.csv`  
     A shuffled version of the full dataset to ensure reproducibility across training runs. 

The datasets can be downloaded from Zenodo at:

**(https://zenodo.org/records/18230736)**


## Reproducibility

To reproduce the experiments:

1. Clone this repository.

```bash
git clone https://github.com/elijahlieb/magnus-time-prediction-ml.git
cd magnus-time-prediction-ml
```
Or download the zip file of the code in GitHub. 

2. Download both ZIP archives from Zenodo.

3. Extract:
   - the PGN files into data/raw/ if you wish to rebuild the dataset from scratch 
   - the CSV files into `results/metrics/` if you want to directly train and evaluate the models. 

4. Install dependencies:

   ```bash
   pip install -r requirements.txt

5. Run the notebooks in order.




## Reproducibility

This section describes how to fully reproduce the experiments presented in the report.

### 1. Clone the repository

```bash
git clone https://github.com/elijahlieb/magnus-time-prediction-ml.git
cd magnus-time-prediction-ml
```


### 2. Download the data from Zenodo

Download the two ZIP archives from the associated Zenodo record:
- magnus_carlsen_blitz_pgns.zip
- magnus_time_prediction_dataset.zip

Extract:
- the PGN files into data/raw/ if you wish to rebuild the dataset from scratch
- the CSV files into results/metrics/ if you want to directly train and evaluate the models

### 3. Create and activate a virtual environment

We strongly recommend using a virtual environment to ensure dependency isolation.

On Windows
```bash
python -m venv venv
venv\Scripts\activate
```

On macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Open the project in VS Code

```bash
code .
```

Make sure that the Python extension is installed and the selected Python interpreter corresponds to the virtual environment (venv)

### 6. Run the notebooks

Open and run the notebooks in the following order:

- notebooks/01_data_processing.ipynb
- notebooks/02_model_training.ipynb
- notebooks/03_website_sample.ipynb

Each notebook is self-contained and assumes that the data folders follow the structure described above.


## Models 

The project evaluates several model families:

- Linear models (Linear Regression, Ridge, Lasso),
- A Random Forest regressor,
- A multilayer perceptron (neural network).

Models are evaluated using standard regression metrics, with a focus on the coefficient of determination (R²).


## Report 

The full research report associated with this project is available on Zenodo: https://zenodo.org/records/18230933

## Purpose and Outlook

This project is an exploratory study demonstrating that human thinking time in chess can be predicted in a non-trivial way from game context.
Beyond modeling a single player, it opens the door to more general approaches that incorporate player skill level and playing style, potentially enriching human-like chess bots and educational tools.


## License 

The code in this repository is provided for academic and educational purposes.
The datasets are released under the license specified in the corresponding Zenodo record.


## Author

Elijah Liebskind
Student in bachelor 3 of CPES DAC from PSL 
Personal project – Data Science / Machine Learning
2025
