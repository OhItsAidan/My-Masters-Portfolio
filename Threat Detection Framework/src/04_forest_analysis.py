import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# This is 1 of 2 graph scripts so we can compare the models performance with and without the assistance of a Markov Model.
# The Isolation Forest, by itself, translates raw machine learning scores into a baseline for analysis


# ------ Histogram -------

def generate_histogram(histogram_df, current_dir):
    print(f"Ingesting scored data...")

    fig1, ax1 = plt.subplots(figsize = (10, 6))

    percentile_value = 0.05 # 5th Percentile
    threshold_score = histogram_df['anomaly_score'].quantile(percentile_value)

    ax1.axvline(
        x = threshold_score,
        color = '#A1045A',
        linestyle = '--',
        linewidth = 2,
        label = f"Anomaly Threshold ({int(percentile_value * 100)}th Percentile: {threshold_score:.2f})"
    )

    ax1.legend(loc = 'upper right', frameon = True)

    sns.histplot(
        data = histogram_df,
        x = 'anomaly_score',
        bins = 50,
        color = "#426C96",
        ax = ax1
    )

    ax1.set_title("Isolation Forest Anomaly Score Distribution", pad = 15, fontweight = 'bold')
    ax1.set_xlabel("Anomaly Score", fontweight = 'bold')
    ax1.set_ylabel("Frequency", fontweight = 'bold')

    output_path_1 = current_dir / "deliverables" / "isolation_forest_histogram.png"
    fig1.savefig(output_path_1, bbox_inches = "tight", dpi = 300)
    print(f"Plot saved to: {output_path_1.name}")
    plt.close(fig1)




    # ------SCATTER GRAPH -------
def generate_scatter_graph(raw_df, current_dir):

    raw_df['prediction'] = raw_df['anomaly_score'].apply(lambda x: -1 if x < 0 else 1)


    features_df = raw_df.drop(columns = ['prediction', 'anomaly_score', 'timestamp', 'user_id'], errors = 'ignore')
    features_df = features_df.select_dtypes(include = ['number'])

    scalar = StandardScaler()
    scaled_features = scalar.fit_transform(features_df)

    # Priciple Component Analysis
    pca = PCA(n_components = 2) 
    reduced_features = pca.fit_transform(scaled_features)

    scatter_df = pd.DataFrame(reduced_features, columns =['Component 1', 'Component 2'])
    scatter_df['Status'] = raw_df['prediction'].map({1: 'Routine (Cluster)', -1: 'Anomaly (Isolated)'})

    fig2, ax2 = plt.subplots(figsize = (10, 6))

    sns.scatterplot(
        s = 10,
        data = scatter_df,
        x = 'Component 1',
        y = 'Component 2',
        hue = 'Status',
        palette = {'Routine (Cluster)': '#63C5DA', 'Anomaly (Isolated)': '#A1045A'},
        alpha = 0.6,
        edgecolor = None,
        ax = ax2
    )

    ax2.set_title("Isolation Forest Scatter Graph: Distribution of Email Communications")
    ax2.set_xlabel("Component 1", fontweight = 'bold')
    ax2.set_ylabel("Component 2", fontweight = 'bold')
    ax2.legend(title = 'Classification')

    output_path_2 = current_dir / "deliverables" / "isolation_forest_scatter_graph.png"
    fig2.savefig(output_path_2, bbox_inches = "tight", dpi = 300)
    print(f"Plot saved to: {output_path_2.name}")
    plt.close(fig2)


def analyse_forest():
    current_dir = Path(__file__).parent.parent
    parquet_file = current_dir / "deliverables" / "enron_scored_features.parquet"

    try:
        prime_df = pd.read_parquet(parquet_file)
    except FileNotFoundError:
        print(f"Could not find .parquet file in {current_dir / 'deliverables'}")
        return
    
    generate_histogram(histogram_df = prime_df, current_dir = current_dir)
    generate_scatter_graph(raw_df = prime_df, current_dir = current_dir)  



if __name__ == "__main__":
    analyse_forest()
    

       