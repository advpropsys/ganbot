from inference import Transformer
transformer = Transformer('./generator_CSM_init.pth')
import cv2
from PIL import Image
import matplotlib.pyplot as plt



image = cv2.imread('MG_1_1_New_York_City-1.jpg')
image = cv2.resize(image, (768, 512))

anime_img = (transformer.transform(image) + 1) / 2

plt.imshow(anime_img[0])
plt.show()
plt.imsave('test.png', anime_img[0])