import tensorflow_hub as hub
import tensorflow as tf
import matplotlib.pyplot as plt
import PIL
import numpy as np
hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
def load_img(path_to_img):
  max_dim = 512
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img
def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)
def style(content_image:str,style_image:str) -> int:
    """Style pic to another pic

    Args:
        content_image (str): path to input
        style_image (str): path to target

    Returns:
        int: 1 if sucess 0 if not
    """
    global state
    state=None
    try:
      stylized_image = hub_model(tf.constant(load_img(content_image)), tf.constant(load_img(style_image)))[0]
      tensor_to_image(stylized_image).save(f'{content_image}_style.png')
    except: return 0
    return 1,state