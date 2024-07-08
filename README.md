# Chatbot with Random Gradient Background

This project implements a simple chatbot using TensorFlow and Flask, and it generates a random gradient background image on each request. The chatbot uses a pre-trained model to respond to user inputs based on defined intents.

## Project Structure

├── app.py
├── data
│ ├── intents_compiled.json
│ ├── label_encoder.pickle
│ ├── simple_chatbot0.h5
│ └── tokenizer.pickle
├── static
│ └── random_image.png
├── templates
│ └── index.html
└── README.md

## Files

- **app.py**: The main Flask application script.
- **chatbot_training.py**: Script for training the chatbot model.
- **data/intents_compiled.json**: JSON file containing the intents and responses.
- **data/label_encoder.pickle**: Pickle file for the label encoder.
- **data/simple_chatbot0.h5**: The trained chatbot model.
- **data/tokenizer.pickle**: Pickle file for the tokenizer.
- **static/random_image.png**: The generated random gradient image.
- **templates/index.html**: The HTML template for the web interface.
- **README.md**: Documentation file for the project.

## Requirements

- Flask
- TensorFlow
- numpy
- Pillow
- scikit-learn
- colorama

You can install the required packages using the following command:

```bash
pip install Flask tensorflow numpy Pillow scikit-learn colorama

