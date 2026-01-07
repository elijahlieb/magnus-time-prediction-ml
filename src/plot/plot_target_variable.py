import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path 
import sys 

# Root of the project 
PROJECT_ROOT = Path.cwd().parent
sys.path.append(str(PROJECT_ROOT))

# Import the path 
from src.utils.config import (FIGURES_DIR)

# Function to show the distribution of target variable and download it 
def plot_target_variable(df, target, name, unit):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[target].dropna(), bins=100, kde=True)

    plt.title("Figure 1", fontsize=12, fontweight='bold')
    plt.xlabel(f"{name} ({unit})")
    plt.ylabel("Count")

    plt.tight_layout()

    # ✅ SAVE FIRST
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        FIGURES_DIR / "time_spent_distribution.png",
        dpi=300,
        bbox_inches="tight"
    )

    # THEN SHOW
    plt.show()

    print("Image saved in results/figures")

