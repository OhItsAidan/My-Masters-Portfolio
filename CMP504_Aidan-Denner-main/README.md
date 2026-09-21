An Insider Threat Detection Framework

## Overview
This repository contains the codebase for a two-layer machine learning pipeline designed to detect insider threats. It integrates an unsupervised Isolation Forest with a Hidden Markov Model.
The dataset this pipeline is designed around is the Enron Email Corpus.

## Prerequisites
Ensure you have Python 3.8+ installed. All required dependencies are in requirements.txt.

## Setup
1. Extract the project to your machine.
2. Download the May 7, 2015 version of the raw Enron Email Corpus (`enron_mail_2015007.tar.gz`) and place it inside deliverables. The raw Corpus can be downloaded here: http://www.cs.cmu.edu/~enron/
4. Open Windows PowerShell (or whatever terminal you prefer), navigate to the root directory of the project, install the required packages:

```powershell
pip install -r requirements.txt
