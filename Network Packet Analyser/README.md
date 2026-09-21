## Network-Packet-Analyser-ML-Project
This is a Machine Learning program designed to analyse network packets from a dataset. It uses whats called a Random Forest Classifier to categorise network traffic anomalies. Think of it like a sorting algorithm!


## Key Features
* **Automated Data Hygiene:** Ingests RAW CSV datasets, and cleans it up so binary feature distributions are normalised.
* **Feature Engineering & Encoding:** `LabelEncoder` is used for multi-class target vectors and one-hot encoding (`pd.get_dummies`) to handle categorical protocol and service variables.
* **Ensemble Classification ("Heimdall"):** Deploys a `RandomForestClassifier` with 102 estimators and a fixed random seed for complete reproducibility.
* **Comprehensive Evaluation:** Generates full classification reports alongside custom-styled visualizations for **Receiver Operating Characteristic (ROC)** curves and **Precision-Recall (PR)** curves per threat category.


## Libraries
* **Language:** Python 3.14+ using a Jupyter Notebook
* **Data Manipulation:** `pandas`, `numpy`
* **Machine Learning:** `scikit-learn` (`RandomForestClassifier`, `LabelEncoder`)
* **Graphs and Visuals:** `matplotlib`, `seaborn`

---

###
Use this command to make sure the correct libraries are installed:

```bash
pip install pandas numpy seaborn matplotlib scikit-learn