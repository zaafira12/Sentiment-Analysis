# Sentiment Analysis – Student Feedback Classification System

This project is an end-to-end NLP pipeline designed to analyze student feedback and automatically generate:

 Sentiment (Positive / Neutral / Negative)
 Category (e.g., Academic & Curriculum, Infrastructure & Facilities, etc.)
 Subcategory (e.g., Teaching Quality, Classroom Conditions, etc.)

The system uses Hugging Face Transformers, fine-tuned DistilBERT models, and a Flask backend API to deliver real-time predictions.

# Features

Sentiment Analysis
Powered by the CardiffNLP twitter-roberta-base-sentiment-latest model.

Fine-Tuned Category Classifier
DistilBERT model trained to classify broader feedback categories.

Fine-Tuned SubCategory Classifier
DistilBERT model specialized in detailed subcategories.

Unified Prediction Pipeline (FeedbackAnalyzer)
Combines all three models to return a complete analysis in one call. 

category (1)

REST API Backend (Flask)
Exposes /analyze endpoint for front-end or app integration.

ngrok Integration
Allows temporary internet-accessible API for testing.


# Model Training Overview

The training script (see category (1).py) performs the following: 

category (1)

1. Load Dataset

Reads Excel data containing:

Category

SubCategory

FeedbackText

Cleans data and converts labels into numerical IDs.

2️.Tokenization

Uses distilbert-base-uncased tokenizer with max length 512.

3️.Train Category Classifier

Trains DistilBERT using Hugging Face Trainer with:

Epochs: 3

Batch Size: 8

Weight Decay: 0.01

Auto-saving best model

4️.Train SubCategory Classifier

Identical process, but with weighted accuracy, precision, recall, and F1.

5️.Build Combined Analyzer

Loads:

Sentiment model

Category classifier

Subcategory classifier

Provides a single .analyze(text) output like:

{
  "sentiment": "Negative",
  "confidence_score": "0.9812",
  "category": "Academic & Curriculum",
  "subcategory": "Teaching Quality"
}

#Technologies Used

- Python 3

- Hugging Face Transformers

- DistilBERT

- CardiffNLP RoBERTa sentiment model

- Flask

- ngrok

- Pandas / Scikit-learn
