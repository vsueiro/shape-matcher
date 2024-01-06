from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim
import base64
import io

app = Flask(__name__)

def get_similarity(img1, image2_path):
    # Load the second image
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # Print dimensions
    print("Image 1 dimensions:", img1.shape)  # Height x Width for img1
    print("Image 2 dimensions:", img2.shape)  # Height x Width for img2

    # Compute similarity
    return ssim(img1, img2)

def base64_to_image(base64_string):
    encoded_data = base64_string.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

def save_base64_as_image(base64_string, output_path):
    encoded_data = base64_string.split(',')[1]
    image_data = base64.b64decode(encoded_data)
    with open(output_path, 'wb') as file:
        file.write(image_data)

def compare_with_folder(folder_path, base_image):
    # List all png files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    # Calculate similarity index for each image
    similarities = {}
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        similarity_index = get_similarity(base_image, image_path)
        similarities[image_file] = similarity_index

    # Sort by similarity (higher first)
    sorted_images = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    return sorted_images

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    base_image_base64 = data['image']
    folder_path = './static/shapes/'

    # Save the base64 string as an image
    # output_path = './user-shapes/received_image.png'
    # save_base64_as_image(base_image_base64, output_path)

    # Convert base64 to image here
    base_image = base64_to_image(base_image_base64)

    # Get sorted images by similarity
    sorted_images_by_similarity = compare_with_folder(folder_path, base_image)

    return jsonify(sorted_images_by_similarity)


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
