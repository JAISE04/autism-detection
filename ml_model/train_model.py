#!/usr/bin/env python3
"""
Data preprocessing script for training the autism detection model
"""

import numpy as np
import cv2
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

def load_images_from_folder(folder_path, img_size=(224, 224)):
    """
    Load images from folder
    
    Expected folder structure:
    datasets/
    ├── positive/
    │   ├── image1.jpg
    │   └── image2.jpg
    └── negative/
        ├── image1.jpg
        └── image2.jpg
    """
    images = []
    labels = []
    
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return None, None
    
    # Load positive samples (autism indicators)
    positive_path = os.path.join(folder_path, 'positive')
    if os.path.exists(positive_path):
        for filename in os.listdir(positive_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                try:
                    img = cv2.imread(os.path.join(positive_path, filename))
                    if img is not None:
                        img = cv2.resize(img, img_size)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        images.append(img)
                        labels.append(1)  # Positive
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    # Load negative samples (no autism indicators)
    negative_path = os.path.join(folder_path, 'negative')
    if os.path.exists(negative_path):
        for filename in os.listdir(negative_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                try:
                    img = cv2.imread(os.path.join(negative_path, filename))
                    if img is not None:
                        img = cv2.resize(img, img_size)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        images.append(img)
                        labels.append(0)  # Negative
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    if len(images) == 0:
        print("No images found in dataset!")
        return None, None
    
    return np.array(images), np.array(labels)

def preprocess_images(images):
    """Normalize image pixel values"""
    return images.astype('float32') / 255.0

def create_dataset(dataset_path='datasets', test_size=0.2, val_size=0.1):
    """
    Create training, validation, and test datasets
    
    Usage:
    X_train, X_val, X_test, y_train, y_val, y_test = create_dataset()
    """
    
    print("Loading images...")
    X, y = load_images_from_folder(dataset_path)
    
    if X is None:
        print("Failed to load images. Please ensure dataset structure is correct:")
        print("datasets/")
        print("├── positive/")
        print("│   └── [images showing autism indicators]")
        print("└── negative/")
        print("    └── [images without autism indicators]")
        return None
    
    print(f"Loaded {len(X)} images")
    print(f"Positive samples: {np.sum(y)}")
    print(f"Negative samples: {len(y) - np.sum(y)}")
    
    # Preprocess images
    print("Preprocessing images...")
    X = preprocess_images(X)
    
    # Split into train+val and test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    # Split train+val into train and val
    val_size_adjusted = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size_adjusted, random_state=42, stratify=y_temp
    )
    
    print(f"\nDataset split:")
    print(f"Training set: {len(X_train)} samples")
    print(f"Validation set: {len(X_val)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def train_model_script():
    """Script to train the model"""
    
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from autism_detector import AutismDetector
    
    # Create dataset
    result = create_dataset()
    if result is None:
        print("Cannot proceed with training without dataset")
        return
    
    X_train, X_val, X_test, y_train, y_val, y_test = result
    
    # Initialize model
    print("\nInitializing model...")
    detector = AutismDetector()
    
    # Train model
    print("Training model...")
    history = detector.train(
        X_train, y_train,
        X_val, y_val,
        epochs=50,
        batch_size=32
    )
    
    # Evaluate on test set
    print("\nEvaluating on test set...")
    test_loss, test_accuracy = detector.model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {test_accuracy*100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Save training history
    with open('ml_model/training_history.pkl', 'wb') as f:
        pickle.dump(history.history, f)
    
    print("\nModel training complete!")
    print(f"Model saved to: {detector.model_path}")

if __name__ == '__main__':
    print("=" * 50)
    print("Autism Detection Model - Data Preprocessing")
    print("=" * 50)
    
    # Check if dataset exists
    if not os.path.exists('datasets'):
        print("\n⚠️  Dataset folder not found!")
        print("\nTo train the model, create the following structure:")
        print("  datasets/")
        print("  ├── positive/")
        print("  │   └── [images of children showing autism indicators]")
        print("  └── negative/")
        print("      └── [images of children without autism indicators]")
        print("\nPlace high-quality, labeled images in these folders.")
    else:
        # Try to load and train
        try:
            train_model_script()
        except Exception as e:
            print(f"Error during training: {e}")
            import traceback
            traceback.print_exc()
