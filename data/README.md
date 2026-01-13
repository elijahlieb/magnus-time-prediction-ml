# Data instructions

This project relies on chess games played by Magnus Carlsen, provided in PGN 
(Portable Game Notation) format. Due to file size constraints and licensing
considerations, raw PGN files and large generated datasets are not included
directly in this repository. But you can download it in this repository : 
https://zenodo.org/records/18230736 

This document explains how to obtain the data and organize it locally in order
to reproduce the experiments.

---

## 1. Raw data (PGN files)

### Source

The PGN files used in this project were obtained from publicly available games
on chess.com.

You may obtain similar data from:
- chess.com game export
- lichess.org database
- public PGN repositories

Ensure that the PGN files contain clock information for each move, as this is
required to compute thinking time.

---

## 2. Expected directory structure

Once downloaded, place your PGN files in the following directory:

```graphql
data/
└── raw/
|    ├── games_1.pgn
|    ├── games_2.pgn
|    └── ...
```

The directory `data/raw/` is intentionally ignored by GitHub (`.gitignore`), but must exist locally for the code to run.

---

## 3. Sample dataset

For demonstration and testing purposes, a small sample dataset is provided in:


This dataset contains a limited number of blitz games and can be used to:
- test the pipeline
- run notebooks without downloading large datasets
- reproduce figures shown in the README

---

## 4. Generating the full dataset

Once PGN files are placed in `data/raw/`, the dataset can be generated with:

```python
from src.data_loading.file_loader import df_final
from src.utils.config import RAW_DATA_DIR

df = df_final(RAW_DATA_DIR)
```

---

## Notes 

Large generated datasets and trained models are intentionally excluded from
version control.

All required output directories are created automatically by the code.

This setup follows standard reproducible research practices.


