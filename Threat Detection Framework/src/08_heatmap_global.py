import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

sns.set_theme(style = "whitegrid", context = "paper", font_scale = 1.2)


 # Just like the previous set of heatmaps this one functions the same, but this one is for the whole timeline.
def plot_global_matrix():

    current_dir = Path(__file__).parent.parent
    global_csv = current_dir / "deliverables" / "transition_matrix_global.csv"
   

    try:
        global_df = pd.read_csv(global_csv, index_col = 0)

    except FileNotFoundError:
        print(f"Could not find .csv files in {current_dir / 'deliverables'}")
        return


    plt.figure(figsize = (14, 6))

    sns.heatmap(
        global_df,
        annot = True,
        fmt = ".1%",
        cmap = "Greys",
        cbar = True,
        vmin = 0, vmax = 1
    )

    plt.title("Enron Matrix (Global)", pad = 15, fontweight = 'bold')
    plt.xlabel("Transition To (Time t+1)", fontweight = 'bold')
    plt.ylabel("Transition From (Time t)", fontweight = 'bold')


    output_path = current_dir / "deliverables" / "global_hmm_transistion_heatmaps.png"
    plt.savefig(output_path,bbox_inches = "tight", dpi = 300)
    print("Exported: global_hmm_transition_heatmaps.png")
    plt.close()

if __name__ == "__main__":
    plot_global_matrix()

