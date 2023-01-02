from inference import Transformer

transformer = Transformer('./generator_hayao.pth') #load generator
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os

def get_image(filename:str)->int:
    """Get CSM GAN image.

    Args:
        filename (str): path to saved image
    Returns:
        int: 1 if success
             0 if failed
    """
    try:
        image = cv2.imread(filename)
        image= cv2.resize(image,(768, 512))

        anime_img = (transformer.transform(image) + 1) / 2

        # plt.imshow(anime_img[0])
        # plt.show()
        # plt.imsave(f'./{filename}_anime.png', anime_img[0])
        plt.imsave(f'{filename}_anime.jpg', anime_img[0])
    except Exception as e: return 0
    return 1


