# For generating random numbers
# Used to generate random mask size and location
import random # For generating random numbers
# provides support for arrays and a wide variety of mathematical functions.
# It is essential for handling data and performing mathematical operations in our project.
# Used to make masks for the images
# Installation: `pip install numpy`
import numpy as np

# Import PyTorch libraries
# A popular open-source deep learning framework
# Used for building and training neural networks in our project.
# Installation: `pip install torch torchvision torchaudio`
import torch

# Used for image processing in this project
# Installation: `pip install pillow`
from PIL import Image

def create_mask(image):
    # Create a binary mask with a random hole
    # using a random size (between 1/5 and 2/5 of original image size)
    #   rectangle mask at random location
    # note that the mask region has the value 1, and 0 for non-mask region
    mask = np.zeros((image.height, image.width), dtype=np.uint8)
    min_mask_size = (image.height // 5, image.width // 5)
    max_mask_size = (2 * image.height // 5, 2 * image.width // 5)
    # Randomly select mask dimensions within the specified range
    mask_height = random.randint(min_mask_size[0], max_mask_size[0])
    mask_width = random.randint(min_mask_size[1], max_mask_size[1])
    # Randomly select the top-left corner coordinates of the mask
    x1 = random.randint(0, image.width - mask_width)
    y1 = random.randint(0, image.height - mask_height)
    x2, y2 = x1 + mask_width, y1 + mask_height
    # Fill the mask with 1s in the selected region
    mask[y1:y2, x1:x2] = 1

    # Convert the mask to a PIL image
    return Image.fromarray(mask * 255)

# process the image before save it into png for better visualization
def postprocess(image):
    """
    This function post-processes the image tensor to convert it into an image that can be
    saved to disk. It clamps the tensor values, scales them to the range [0, 255], and
    converts the tensor to a NumPy array.

    Args:
        image (torch.Tensor): Image tensor to be post-processed.

    Returns:
        Image: A PIL Image object containing the post-processed image.
    """
    image = torch.clamp(image, -1., 1.)
    image = (image + 1) / 2.0 * 255.0
    image = image.permute(1, 2, 0)
    image = image.cpu().numpy().astype(np.uint8)
    return Image.fromarray(image)