"""
Image processing utilities
"""
from PIL import Image, ImageTk

def resize_image(image, max_width=400, max_height=300):
    """
    Resize image to fit within max dimensions while preserving aspect ratio
    
    Args:
        image: PIL Image object
        max_width: Maximum width
        max_height: Maximum height
        
    Returns:
        Resized PIL Image
    """
    width, height = image.size
    
    # Calculate the ratio of the width and height to the max dimensions
    width_ratio = max_width / width
    height_ratio = max_height / height
    
    # Use the smaller ratio to ensure the image fits within bounds
    ratio = min(width_ratio, height_ratio)
    
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    
    return image.resize((new_width, new_height), Image.LANCZOS)

def convert_to_tk_image(pil_image):
    """
    Convert PIL Image to Tkinter PhotoImage
    
    Args:
        pil_image: PIL Image object
        
    Returns:
        Tkinter PhotoImage
    """
    return ImageTk.PhotoImage(pil_image)