import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


sns.set_theme(style = "whitegrid", context = "paper", font_scale = 1.2)


    # This script is outputs the graphs needed to examine the first half of results from the HMM
    # Heatmaps are generated and show the hotspots of where the entities within the network lie in terms of their threat states
    # Reds show the Pre-Crisis states
    # Greens show the Post-Crisis states
    # The last output is a line graph that will show the behaviour of one person on the Enron Email Corpus.
    # For the demonstration this will be the CEO Jeffery Skilling although any email from the corpus can be chosen by replacing the email on the marked line. 

def plot_matrix():

    current_dir = Path(__file__).parent.parent
    pre_csv = current_dir / "deliverables" / "transition_matrix_pre.csv"
    post_csv = current_dir / "deliverables" / "transition_matrix_post.csv"

    try:
        pre_crisis_df = pd.read_csv(pre_csv, index_col = 0)
        post_crisis_df = pd.read_csv(post_csv, index_col = 0)

    except FileNotFoundError:
        print(f"Could not find .csv files in {current_dir / 'deliverables'}")
        return


    # PRE-CRISIS HEATMAP

    fig1, ax1 = plt.subplots(figsize = (14, 6))

    sns.heatmap(
        pre_crisis_df,
        annot = True,
        fmt = ".1%",
        cmap = "Reds",
        cbar = True,
        ax = ax1,
        vmin = 0, vmax = 1
    )

    ax1.set_title("Pre-Crisis Matrix: Baseline Operations", pad = 15, fontweight = 'bold')
    ax1.set_xlabel("Transition To (Time t+1)", fontweight = 'bold')
    ax1.set_ylabel("Transition From (Time t)", fontweight = 'bold')

    output_path_1 = current_dir / "deliverables" / "hmm_transition_heatmap_baseline.png"
    fig1.savefig(output_path_1, bbox_inches = "tight", dpi = 300)
    print("Image exported: hmm_transition_heatmap_baseline.png")
    plt.close(fig1)

    # POST-CRISIS HEATMAP

    fig2, ax2= plt.subplots(figsize = (14, 6))

    sns.heatmap(
        post_crisis_df,
        annot = True,
        fmt = ".1%",
        cmap = "Greens",
        cbar = True,
        ax = ax2,
        vmin = 0, vmax = 1
        )
    
    ax2.set_title("Post-Crisis Matrix", pad = 15, fontweight = 'bold')
    ax2.set_xlabel("Transition To (Time t+1)", fontweight = 'bold')
    ax2.set_ylabel("Transition From (Time t)", fontweight = 'bold')


    output_path_2 = current_dir / "deliverables" / "hmm_transition_heatmap_post.png"
    fig2.savefig(output_path_2, bbox_inches = "tight", dpi = 300)
    print("Exported: hmm_transition_heatmap_post.png")
    plt.close(fig2)


    # The graph to measure the threat states of one person is a separate function.

def plot_single_timeline():
    current_dir = Path(__file__).parent.parent
    states_csv =  current_dir / "deliverables" / "hidden_states.csv"

    try:
        target_df = pd.read_csv(states_csv)
    except FileNotFoundError:
        print(f"Could not find hidden_states.csv in {current_dir/ 'deliverables'}")
        return

    target_df['parsed_date'] = pd.to_datetime(target_df['parsed_date'], utc = True)

    enron_df = target_df[target_df['sender'] == 'jeff.skilling@enron.com'].copy() # CHANGE THIS EMAIL FOR A DIFFERENT EMPLOYEE
    enron_df = enron_df.sort_values('parsed_date')


    fig3, ax = plt.subplots(figsize = (12, 5), dpi = 300)

    ax.step(enron_df['parsed_date'], enron_df['threat_profile'], where = 'post', color = '#b22222', linewidth = 2)

    state_labels = ['State 0\n(Routine)', 'State 1\n(Irregular)', 'State 2\n(Suspicious)', 'State 3\n(Critical)']
    ax.set_yticks([0, 1, 2, 3])
    ax.set_ylabel(state_labels, fontsize = 10)
    ax.set_ylim(-0.2, 3.2)


    # These are markers to plot specific events on the timeline, it will allow us to easily compare what a persons threat state was at the time of the event.
    resign_date = np.datetime64('2001-08-14')
    ax.axvline(x = resign_date, color = 'black', linestyle = '--', linewidth = 1.5, alpha = 0.7)
    ax.text(resign_date, 2.5, 'CEO Resigns', rotation = 0, verticalalignment = 'center', color = 'black', fontsize = 10, fontweight = 'bold')

    sec_date = np.datetime64('2001-10-22')
    ax.axvline(x = sec_date, color = 'black', linestyle = '--', linewidth = 1.5, alpha = 0.7)
    ax.text(sec_date, 2.5, 'SEC Investigation\n Announced', rotation = 0, verticalalignment = 'center', color = 'grey', fontsize = 10, fontweight = 'bold')

    ax.set_title("CEO Escalation Timeline", fontsize = 14, fontweight = 'bold', pad = 15)
    ax.set_xlabel("Chronological Timeline", fontsize = 12, fontweight = 'bold')
    ax.set_ylabel("Inferred Hidden State", fontsize = 12, fontweight = 'bold')
    ax.grid(axis = 'y', linestyle = '--', alpha = 0.6)
    ax.grid(axis = 'x', linestyle = '--', alpha = 0.3)
    plt.tight_layout()


    output_path_3 = current_dir / "deliverables" / "CEO_escalation_timeline.png"
    fig3.savefig(output_path_3, bbox_inches = "tight", dpi = 300)
    print("Exported: CEO_escalation_timeline.png")
    plt.close(fig3)

if __name__ == "__main__":
    plot_matrix()
    plot_single_timeline()
