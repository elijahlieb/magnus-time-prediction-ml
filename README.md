
# README — Magnus Time Prediction
## Predicting Human Thinking Time in Chess
### An empirical study based on Magnus Carlsen’s blitz games

## Project Overview

Modern chess engines achieve superhuman strength but fail to reproduce essential aspects of human behavior, particularly the temporal dynamics of decision-making. While recent research has focused on predicting human moves and playing style, the time humans spend thinking before playing a move remains largely unexplored.

This project investigates whether human thinking time can be predicted empirically from real chess game data. Focusing on blitz games played by Magnus Carlsen, we construct machine learning models to predict the time spent on individual moves using information available in real time (position, game phase, time pressure, and game dynamics).

The long-term goal is to contribute to more human-aligned chess AI systems, by integrating realistic time management into imitation-based engines and educational tools.

## Repository Structure

magnus-time-prediction/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── README.md          # Instructions to obtain raw data
│   └── sample/            # Small example dataset (5 blitz games)
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
│   ├── models/            # Saved models (excluded from GitHub if large)
│   └── logs/              # Execution and training logs


### Important note:

GitHub does not track empty folders. All scripts automatically create the required subfolders in results/ if they do not exist, ensuring the project runs correctly after cloning.


## Data 

The dataset is built from publicly available chess games played by Magnus Carlsen on chess.com, provided in PGN (Portable Game Notation) format. Each row of the dataset corresponds to one move played by Magnus Carlsen. Only blitz games are considered. 

Features include temporal variables, game dynamics, positional complexity indicators, and time control information

Due to size constraints, raw PGN files and large generated datasets are not included in this repository.

Instructions for obtaining the data are provided in:

data/README.md


## Installation

### 1. Clone the repository

git clone https://github.com/elijahlieb/magnus-time-prediction-ml.git
cd magnus-time-prediction-ml

### 2. Create a virtual environment (recommended)

python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

### 3. Install dependencies

pip install -r requirements.txt


## Usage 

### 1. Data processing 

from src.data_loading.file_loader import df_final
from src.utils.io import save_dataframe_as_csv
from src.utils.config import DATA_DIR, RESULTS_DIR

df = df_final(DATA_DIR / "raw")
save_dataframe_as_csv(df, RESULTS_DIR / "metrics", "df_MagnusMoves.csv")

All required output directories (results/metrics, results/figures, etc.) are created automatically if they do not exist.

### 2. Model Training 

Models implemented in this project include: Linear Regression (baseline), Random Forest and Multilayer Perceptron (Neural Network). 

Example (Random Forest):

from src.models.random_forest import train_random_forest
model = train_random_forest(X_train, y_train)

### 3. Visualization

from src.utils.plot import plot_target_variable
plot_target_variable(df, "TimeSpend", "Time spent", "seconds")

Figures are saved automatically in results/figures.


## Reproducibility

This repository follows reproducible research practices:

- Clear separation between raw data, code, and results
- Automatic creation of output directories
- Fixed random seeds where applicable
- Example datasets provided for demonstration

Large models and datasets are intentionally excluded from GitHub and must be generated locally.

## Relation to Existing Work

This project is inspired by recent efforts to model human behavior in chess, notably the Maia project (McIlroy-Young et al., 2021). While Maia focuses on move selection, this work addresses the complementary problem of modeling human thinking time, a key component of realistic human-AI alignment.

## Author 

Elijah Liebskind
Student in bachelor 3 of CPES DAC from PSL 
Personal project – Data Science / Machine Learning
2025
