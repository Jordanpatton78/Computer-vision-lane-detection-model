import os
import random
from PIL import Image, ImageEnhance, ImageFilter
import cv2

def augment_image(img):
    # List of transformations to apply
    transformations = [
        lambda x: x.transpose(Image.FLIP_LEFT_RIGHT),            # Horizontal flip
        lambda x: x.transpose(Image.FLIP_TOP_BOTTOM),            # Vertical flip
        lambda x: x.rotate(random.choice([90, 180, 270])),       # Random rotation
        lambda x: x.filter(ImageFilter.GaussianBlur(radius=2)),  # Blur
        lambda x: ImageEnhance.Contrast(x).enhance(1.5),         # Contrast adjustment
        lambda x: ImageEnhance.Brightness(x).enhance(1.2),       # Brightness adjustment
    ]
    # Apply a random transformation
    return random.choice(transformations)(img)

def augment_folder(input_folder, output_folder, target_count):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load all images in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    
    # Calculate the number of augmented images per original image
    images_to_add = target_count - len(image_files)
    augmentations_per_image = max(1, images_to_add // len(image_files))
    
    counter = 0
    for img_name in image_files:
        img_path = os.path.join(input_folder, img_name)
        img = Image.open(img_path)
        
        # Save original image in the output folder
        img.save(os.path.join(output_folder, f"{img_name.split('.')[0]}_original.jpg"))
        
        # Generate augmented images
        for i in range(augmentations_per_image):
            augmented_img = augment_image(img)
            augmented_img.save(os.path.join(output_folder, f"{img_name.split('.')[0]}_aug_{i}.jpg"))
            counter += 1
            if counter >= images_to_add:
                break
        if counter >= images_to_add:
            break
    
    print(f"Generated {counter} augmented images in '{output_folder}'.")

# Usage
input_folder = 'images'   # Replace with path to your folder of images
output_folder = 'aug_images' # Replace with path to your output folder
target_count = 100  # Specify the total number of images you want in the output folder

augment_folder(input_folder, output_folder, target_count)
