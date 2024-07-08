import json
import numpy as np
from flask import Flask, render_template, request, jsonify

import keras
import pickle



app = Flask(__name__)

# Load trained model
model = keras.models.load_model('./data/simple_chatbot0.h5')

# Load tokenizer object
with open('./data/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load label encoder object
with open('./data/label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# Parameters
max_len = 20

# Load intents file
with open('./data/intents_compiled.json') as file:
    data = json.load(file)


from PIL import Image
import random

def generate_random_image(width, height, output_file):
    """
    Generate a random image of given width and height with multiple gradients.

    Parameters:
    width (int): Width of the image.
    height (int): Height of the image.
    output_file (str): File path where the image will be saved.
    """
    # Randomly determine the number of gradients (between 1 and 2 for this example)
    num_gradients = np.random.randint(1, 3)  # This returns a scalar integer
    
    # Initialize an empty array for the image
    image_array = np.zeros((height, width, 3), dtype=np.float64)

    def generate_non_black_color():
        """
        Generate a color that is not too close to black.
        """
        while True:
            color = np.random.randint(100, 256, 3)
            if np.sum(color) > 100:  # Threshold to avoid colors too close to black
                return color

    for _ in range(num_gradients):
        # Randomly choose a base color for each gradient, ensuring it's not too close to black
        base_color = generate_non_black_color()

        # Create an empty array for the gradient
        gradient = np.zeros((height, width, 3), dtype=np.float64)

        # Randomly choose a gradient type
        gradient_type = random.choice(['linear', 'radial'])

        if gradient_type == 'linear':
            # Randomly choose a direction for the linear gradient
            angle = random.uniform(0, 2 * np.pi)
            cos_angle = np.cos(angle)
            sin_angle = np.sin(angle)
            
            for y in range(height):
                for x in range(width):
                    # Calculate the linear gradient factor based on direction
                    factor = (x * cos_angle + y * sin_angle) / (np.sqrt(width**2 + height**2))
                    factor = np.clip(factor, 0, 1)  # Ensure factor is within [0, 1]
                    gradient[y, x] = base_color * factor

        elif gradient_type == 'radial':
            # Calculate the center of the image
            center_x, center_y = width // 2, height // 2
            max_distance = np.sqrt(center_x**2 + center_y**2)
            
            for y in range(height):
                for x in range(width):
                    # Calculate the radial gradient factor
                    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                    factor = distance / max_distance
                    factor = np.clip(factor, 0, 1)  # Ensure factor is within [0, 1]
                    gradient[y, x] = base_color * factor
        
        # Add the gradient to the image array
        image_array += gradient

    # Normalize the final image array to ensure values are within [0, 255]
    image_array = np.clip(image_array / num_gradients, 0, 255).astype(np.uint8)

    # Create an image from the numpy array
    final_image = Image.fromarray(image_array)

    # Save the image
    final_image.save(output_file)


@app.before_request
def before_request():
    generate_random_image(24,15,"./static/random_image.png")


@app.route('/')
def index():
    # generate_random_image(256,256,"./static/random_image.png")
    # background_image = "../random_image.png"
    # return render_template('index.html', background_image=background_image)
    generate_random_image(24,15,"./static/random_image.png")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # Preprocess the user message
    sequence = tokenizer.texts_to_sequences([user_message])
    padded_sequence = keras.preprocessing.sequence.pad_sequences(sequence, truncating='post', maxlen=max_len)
    
    # Predict the intent
    result = model.predict(padded_sequence)
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    # Find the corresponding response
    for intent in data['intents']:
        if intent['tag'] == tag[0]:
            response = np.random.choice(intent['responses'])
            break

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host='0.0.0.0', port=8000)
