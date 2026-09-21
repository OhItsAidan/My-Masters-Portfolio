import pandas as pd
import numpy as np
from hmmlearn import hmm
from pathlib import Path
import time
import sys
import random
import threading


def the_hidden_one(input_parquet, output_csv):

    # This here is the Hidden Markov Model that will track behavioural state transitions across the Enron dataset.

    # For this script specficially we are splitting the timeline into Pre-Crisis: Baseline Operations and Post Crisis
    # This is so we can see the change in employee behaviour differences from the moment they were being investigated by the authorities.

    print(f"Loading data from {input_parquet.name}... ")
    enron_df = pd.read_parquet(input_parquet)

    print("Arranging emails chronologically by sender...")

    # Parsing Enron timestamps
    enron_df['clean_timestamp'] = enron_df['timestamp'].str.replace(r'\s*\([A-Z]+\)\s*$', '', regex = True)
    enron_df['parsed_date'] = pd.to_datetime(enron_df['clean_timestamp'], errors = 'coerce', utc = True)
    enron_df = enron_df.dropna(subset = ['parsed_date'])

    # This bit just ensures the program does not crash due to null values
    enron_df = enron_df.dropna(subset = ['anomaly_score'])

    # To filter out the noise: A chain must have 10+ emails to be considered a full sequence
    email_counts = enron_df['sender'].value_counts()
    valid_senders = email_counts[email_counts >= 10].index
    enron_df = enron_df[enron_df['sender'].isin(valid_senders)].copy()

    enron_df = enron_df.sort_values(by = ['sender', 'parsed_date'])

    print(f"Filtered down to  {len(valid_senders)} senders.")

    # This is the point where we slice the data into the two time periods: Pre and Post Crisis
    pivot_date = pd.to_datetime('2001-10-22', utc = True)
    print(f"Slicing dataset at: {pivot_date}")

    pre_crisis_df = enron_df[enron_df['parsed_date'] < pivot_date].copy()
    post_crisis_df = enron_df[enron_df['parsed_date'] >= pivot_date].copy()

    print(f"Pre-Crisis (Baseline): {len(pre_crisis_df)}")
    print(f"Post-Crisis (Doom): {len(post_crisis_df)}")


    print(f"Preparing data for Markov Model...")

    # These emission vectors point the model to the categorical states.
    pre_emission_vector = pre_crisis_df['markov_state'].to_numpy().reshape(-1, 1)
    pre_timeline_boundary = pre_crisis_df.groupby('sender', sort = False).size().tolist()

    post_emission_vector = post_crisis_df['markov_state'].to_numpy().reshape(-1, 1)
    post_timeline_boundary = post_crisis_df.groupby('sender', sort = False).size().tolist()

    print("Initialising Model...")

    # MODEL CONFIGURATION
    # CategoricalHMM is used for behavioural profiling as it strictly defines 4 states which can be seen as 'Rooms'
    hmm_pre_crisis = hmm.CategoricalHMM(
        n_components = 4,
        n_iter = 100,
        random_state = 42
    )

    hmm_post_crisis = hmm.CategoricalHMM(
        n_components = 4,
        n_iter = 100,
        random_state = 42
    )
    training_complete = False

    def spin_animation():
        nonlocal training_complete
        while not training_complete:
            roll = f"{random.randint(1, 20):2d}"
            sys.stdout.write(f'\r>>> ROLLING FOR INSIGHT... Hold on to your butts! d{roll}') # This is a custom spinner function I made thats been... slightly tweaked to use a random integer
            sys.stdout.flush()
            time.sleep(0.1)

    spinner_thread = threading.Thread(target = spin_animation)

    start_time = time.time()
    spinner_thread.start()

    try:
        hmm_pre_crisis.fit(pre_emission_vector, lengths = pre_timeline_boundary)
        hmm_post_crisis.fit(post_emission_vector, lengths = post_timeline_boundary)
    finally:
        training_complete = True
        spinner_thread.join()

        sys.stdout.write('\r' + ' ' * 60 + '\r')
        sys.stdout.flush()

    if hmm_pre_crisis.monitor_.converged:
        print("Pre-Crisis run successful.")
    else:
        print("CRITICAL FAILURE: The model has flatlined")

    if hmm_post_crisis.monitor_.converged:
        print("Post-Crisis run successful.")
    else:
        print("CRITICAL FAILURE: The model has flatlined")

    end_time = time.time()
    minutes, seconds = divmod(end_time - start_time, 60)

    print(f"Completed in {int(minutes)}m {seconds:.2f}s")

    print("Decoding hidden states...")
    pre_crisis_df['predicted_hidden_state'] = hmm_pre_crisis.predict(pre_emission_vector, lengths = pre_timeline_boundary)
    post_crisis_df['predicted_hidden_state'] = hmm_post_crisis.predict(post_emission_vector, lengths = post_timeline_boundary)

    # Makes sure the states are properly and logically aligned.
    # Without this, the anomaly scores would be inverted. 
   
   # --- PRE CRISIS SEVERITY ALIGNMENT ---
    pre_crisis_df['predicted_hidden_state'] = hmm_pre_crisis.predict(pre_emission_vector, lengths = pre_timeline_boundary)
    pre_state_mean = pre_crisis_df.groupby('predicted_hidden_state')['anomaly_score'].mean()
    pre_severity = pre_state_mean.sort_values(ascending = False).index.tolist()
    pre_severity_alignment = {old_state: new_state for new_state, old_state in enumerate(pre_severity)}
    pre_crisis_df['threat_profile'] = pre_crisis_df['predicted_hidden_state'].map(pre_severity_alignment)


    # --- POST CRISIS SEVERITY ALIGNMENT ---
    post_crisis_df['predicted_hidden_state'] = hmm_post_crisis.predict(post_emission_vector, lengths = post_timeline_boundary)
    post_state_mean = post_crisis_df.groupby('predicted_hidden_state')['anomaly_score'].mean()
    post_severity = post_state_mean.sort_values(ascending = False).index.tolist()
    post_severity_alignment = {old_state: new_state for new_state, old_state in enumerate(post_severity)}
    post_crisis_df['threat_profile'] = post_crisis_df['predicted_hidden_state'].map(post_severity_alignment)


    # The Matrix Extraction
    print("\n --- PRE-CRISIS TRANSITION MATRIX ---")
    print("Rows = Current Hidden State | Columns = Next Hidden State")

    pre_aligned_matrix = hmm_pre_crisis.transmat_[np.ix_(pre_severity, pre_severity)]
    pre_crisis_matrix_df = pd.DataFrame(pre_aligned_matrix).round(4)
    print(pre_crisis_matrix_df)

    state_label = [f"State {i}" for i in range(pre_aligned_matrix.shape[0])]
    pre_crisis_matrix_df.index = state_label
    pre_crisis_matrix_df.columns = state_label

    pre_crisis_csv_path = output_csv.parent / "transition_matrix_pre.csv"
    pre_crisis_matrix_df.to_csv(pre_crisis_csv_path)
    print(f"Pre-Crisis Matrix saved to {pre_crisis_csv_path.name}")


    print("\n --- POST-CRISIS TRANSITION MATRIX ---")
    print("Rows = Current Hidden State | Columns = Next Hidden State")

    post_aligned_matrix = hmm_post_crisis.transmat_[np.ix_(post_severity, post_severity)]
    post_crisis_matrix_df = pd.DataFrame(post_aligned_matrix).round(4)
    print(post_crisis_matrix_df)

    post_crisis_matrix_df.index = state_label
    post_crisis_matrix_df.columns = state_label
    
    post_crisis_csv_path = output_csv.parent / "transition_matrix_post.csv"
    post_crisis_matrix_df.to_csv(post_crisis_csv_path)
    print(f"Post-Crisis Matrix saved to {post_crisis_csv_path.name}")

    

    final_result = pd.concat([pre_crisis_df, post_crisis_df])
    final_result = final_result.drop(columns = ['predicted_hidden_state'])

    final_result.to_csv(output_csv, index = False)
    print(f"\n Timeline saved to {output_csv.name}")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent

    input_file = BASE_DIR / "deliverables" / "enron_multiclass_states.parquet"
    output_file = BASE_DIR / "deliverables" / "hidden_states.csv"

    the_hidden_one(input_file, output_file)

