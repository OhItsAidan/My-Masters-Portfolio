import tarfile
import pandas as pd
import email
from pathlib import Path


# This scripts goal is to extract metadata, structure and a range of features the Isolation Forest and Markov Model can use
# for detecting anomalies.

def extract_isolation_forest_features(tar_path, max_emails = 1000000):
    features_list = []
    email_count = 0

    print("Extracting archive...") 

    with tarfile.open(tar_path, "r:gz") as tar:
        for i, member in enumerate(tar):
            if i >= max_emails: 
                break

            if member.isfile() and member.name.endswith('.'):
                f = tar.extractfile(member)
                if f is not None:
                    raw_text = f.read().decode('utf-8', errors = 'ignore') # Decodes the raw text and ignores unreadable characters

                    msg = email.message_from_string(raw_text)

                    subject = msg.get('Subject', '')
                    subject_len = len(subject.strip()) if subject else 0

                    to_header = msg.get('To', '')
                    recipient_count = len(to_header.split(',')) if to_header else 0

                    sender = msg.get('From', 'unknown').strip() if msg.get('From') else "unknown"
                    timestamp = msg.get('Date', 'unknown').strip() if msg.get('Date') else "unknown"

                    has_bcc = 1 if msg.get('Bcc') else 0

                    body = msg.get_payload()
                    body_len = len(body) if isinstance(body, str) else 0

                    # All the features extracted from the dataset
                    features_list.append({
                        "file_path": member.name,
                        "sender": sender,
                        "timestamp": timestamp,
                        "subject_length": subject_len,
                        "body_length": body_len,
                        "has_bcc": has_bcc,
                        "recipient_count": recipient_count

                    })

                    email_count += 1

    df = pd.DataFrame(features_list)

    # To reduce bias I have added some code in to parse timestamps as well as date/time to capture out of hours anomalies

    # The dataset has a strange formatting issue with the date and timestamps, this line here, cleans it up.
    df['clean_timestamp'] = df['timestamp'].str.replace(r'\s*\([A-Z]+\)\s*$', '', regex = True) 

    # Below here is where we are parsing the timestamps to capture any out-of-hours anomalies
    df['parsed_date'] = pd.to_datetime(df['clean_timestamp'], errors = 'coerce', utc = True)
    df['hour_of_day'] = df['parsed_date'].dt.hour.fillna(-1).astype(int)
    df['day_of_week'] = df['parsed_date'].dt.dayofweek.fillna(-1)

    df.drop(columns = ['parsed_date', 'clean_timestamp'], inplace = True)

    return df


# Each script in this project will contain this at the bottom of it to ensure cross platform compatibility.
# It should show the ingesting of one file and outputing the new file into the data folder of the project.
if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent

    tar_file_path = BASE_DIR / "deliverables" / "enron_mail_20150507.tar.gz"
    output_path = BASE_DIR / "deliverables" / "enron_raw_features.parquet"

    df_raw = extract_isolation_forest_features(tar_file_path, max_emails = 1000000)

    df_raw.to_parquet(output_path)
    print(f"Extraction Done. Saved {len(df_raw)} records to {output_path}")