import cv2
import numpy as np
from PIL import Image
import os

def analyze_image_realism(image_path):
    """
    Analyzes an image for common AI generation flaws like 
    over-smoothing (blurriness) and unnatural contrast.
    """
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    # Check if the image loaded successfully
    if image is None:
        return {"error": "Could not read image file. Check the file path."}
    
    # Convert the image to grayscale (black and white) because texture/sharpness 
    # math is easier and more accurate without color interference
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 1. Calculate Sharpness using Laplacian Variance
    # AI-generated images often suffer from artificial over-smoothing or weird blurring.
    # A low variance score means the image is blurry; a high score means it's sharp.
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # 2. Calculate Contrast using Pixel Standard Deviation
    # Measures how varied the lighting is across the image.
    contrast = gray.std()
    
    # Combine these metrics into a simple calculated "Realism Score" (Scaled roughly from 0 to 100)
    # We balance sharpness and contrast to create a baseline index.
    raw_score = (laplacian_var / 4.0) + (contrast / 1.5)
    score = min(max(raw_score, 10.0), 99.0) # Keep score safely between 10 and 99
    
    # Generate actionable tips based on what the math reveals
    tips = []
    if laplacian_var < 80:
        tips.append("High over-smoothing detected. Background details or textures may look artificially blurred.")
    if contrast < 30:
        tips.append("Low contrast variance. Lighting might look flat or unnaturally uniform.")
    if not tips:
        tips.append("Sharpness and contrast look well-balanced. Minimal distortion artifacts found.")
        
    # Return structured data (JSON format)
    return {
        "realism_score": round(score, 2),
        "metrics": {
            "sharpness_index": round(laplacian_var, 2),
            "contrast_index": round(contrast, 2)
        },
        "tips": tips
    }

# --- Local Test Block ---

if __name__ == "__main__":
    # Get the absolute path to the image in the current folder
    test_file = os.path.abspath("test_image.png")
    print(f"Looking for image at: {test_file}")
    
    result = analyze_image_realism(test_file)
    print("\nAnalysis Result:")
    print(result)