#!/usr/bin/env python3
"""
Generate synthetic autism detection dataset with facial images
Creates positive (autism indicators) and negative (typical development) samples
"""

import numpy as np
import cv2
import os
from pathlib import Path
import random

def create_dataset_folders(base_path='datasets'):
    """Create dataset directory structure"""
    paths = {
        'positive': os.path.join(base_path, 'positive'),
        'negative': os.path.join(base_path, 'negative')
    }
    
    for path in paths.values():
        os.makedirs(path, exist_ok=True)
    
    return paths

def generate_face_image(width=224, height=224, face_type='positive'):
    """
    Generate synthetic face image with autism/typical development indicators
    
    Autism indicators (positive):
    - Limited eye contact (eyes looking away)
    - Unusual facial symmetry
    - Reduced facial expression
    
    Typical development (negative):
    - Direct eye contact
    - Symmetric face
    - Natural facial expression
    """
    
    # Create base image (skin tone background)
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    if face_type == 'positive':
        # Autism indicators - brownish/reddish skin tone
        img[:, :] = (120, 100, 140)  # BGR format
        
        # Eyes looking away (not centered)
        left_eye_x = random.randint(40, 60)
        right_eye_x = random.randint(160, 180)
        eye_y = random.randint(70, 90)
        
        # Pupils looking to the side
        pupil_offset = random.randint(8, 15)
        cv2.circle(img, (left_eye_x + pupil_offset, eye_y), 12, (0, 0, 0), -1)
        cv2.circle(img, (right_eye_x + pupil_offset, eye_y), 12, (0, 0, 0), -1)
        
        # Limited expression - flat mouth
        cv2.line(img, (80, 160), (144, 160), (50, 30, 30), 3)
        
        # Asymmetric face
        cv2.ellipse(img, (105, 110), (45, 55), 0, 0, 180, (140, 120, 160), 3)
        cv2.ellipse(img, (119, 110), (35, 55), 0, 0, 180, (140, 120, 160), 3)
        
    else:
        # Typical development - peachy/warm skin tone
        img[:, :] = (180, 150, 130)  # BGR format
        
        # Eyes looking forward (centered)
        left_eye_x = 70
        right_eye_x = 154
        eye_y = 85
        
        # Pupils looking forward
        cv2.circle(img, (left_eye_x, eye_y), 12, (0, 0, 0), -1)
        cv2.circle(img, (right_eye_x, eye_y), 12, (0, 0, 0), -1)
        cv2.circle(img, (left_eye_x, eye_y), 5, (100, 150, 200), -1)
        cv2.circle(img, (right_eye_x, eye_y), 5, (100, 150, 200), -1)
        
        # Natural smile
        cv2.ellipse(img, (112, 165), (35, 20), 0, 0, 180, (50, 30, 30), 3)
        
        # Symmetric face
        cv2.ellipse(img, (112, 110), (50, 60), 0, 0, 180, (200, 170, 150), 3)
    
    # Add nose
    cv2.line(img, (112, 100), (112, 145), (100, 80, 100), 2)
    
    # Add some noise for realism
    noise = np.random.normal(0, 15, img.shape).astype(np.uint8)
    img = cv2.add(img, noise)
    
    # Add slight blur
    img = cv2.GaussianBlur(img, (5, 5), 0)
    
    return img

def generate_dataset(num_positive=100, num_negative=100, output_dir='datasets'):
    """Generate complete synthetic dataset"""
    
    print("=" * 60)
    print("Generating Autism Detection Dataset")
    print("=" * 60)
    
    paths = create_dataset_folders(output_dir)
    
    # Generate positive samples (autism indicators)
    print(f"\nGenerating {num_positive} positive samples (autism indicators)...")
    for i in range(num_positive):
        img = generate_face_image(face_type='positive')
        filename = os.path.join(paths['positive'], f'autism_{i:04d}.jpg')
        cv2.imwrite(filename, img)
        if (i + 1) % 20 == 0:
            print(f"  ✓ {i + 1}/{num_positive} positive samples created")
    
    # Generate negative samples (typical development)
    print(f"\nGenerating {num_negative} negative samples (typical development)...")
    for i in range(num_negative):
        img = generate_face_image(face_type='negative')
        filename = os.path.join(paths['negative'], f'typical_{i:04d}.jpg')
        cv2.imwrite(filename, img)
        if (i + 1) % 20 == 0:
            print(f"  ✓ {i + 1}/{num_negative} negative samples created")
    
    print("\n" + "=" * 60)
    print("Dataset Generation Complete!")
    print("=" * 60)
    print(f"\n📊 Dataset Statistics:")
    print(f"   Positive samples: {num_positive}")
    print(f"   Negative samples: {num_negative}")
    print(f"   Total samples: {num_positive + num_negative}")
    print(f"\n📁 Location: {os.path.abspath(output_dir)}/")
    print(f"   ├── positive/")
    print(f"   └── negative/")
    print(f"\n✅ Ready to train! Run: python ml_model/train_model.py")
    
    return paths

if __name__ == '__main__':
    # Generate dataset with default parameters
    # You can modify these numbers as needed
    generate_dataset(
        num_positive=100,   # 100 autism indicator images
        num_negative=100,   # 100 typical development images
        output_dir='datasets'
    )
