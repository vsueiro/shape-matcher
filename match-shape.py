import os
import cv2
from skimage.metrics import structural_similarity as ssim

def get_similarity(image1_path, image2_path):
    # Load the images
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # Compute similarity
    return ssim(img1, img2)

def compare_with_folder(folder_path, base_image_path):
    # List all png files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    # Calculate similarity index for each image
    similarities = {}
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        similarity_index = get_similarity(base_image_path, image_path)
        similarities[image_file] = similarity_index

    # Sort by similarity (higher first)
    sorted_images = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    return sorted_images

# Path to the base image and the folder
base_image_path = './user-shapes/1.png'
folder_path = './shapes/'

# Get sorted images by similarity
sorted_images_by_similarity = compare_with_folder(folder_path, base_image_path)

print(sorted_images_by_similarity)
