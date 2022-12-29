from inference import Transformer
transformer = Transformer('./generator_CSM_init.pth')
import cv2
import random
import matplotlib.pyplot as plt
import numpy as np
import imutils


image = imutils.url_to_image('https://blog-www.pods.com/wp-content/uploads/2019/04/MG_1_1_New_York_City-1.jpg')
image = cv2.resize(image, (768, 512))

anime_img = (transformer.transform(image) + 1) / 2

plt.imshow(anime_img[0])
plt.show()
plt.imsave('test.png', anime_img[0])