import cv2
import numpy as np
from rembg import remove
from PIL import Image
import io
import sys

with open(sys.argv[1], 'rb') as f:
    input_data = f.read()
output_data = remove(input_data)
img = Image.open(io.BytesIO(output_data)).convert('L')

img_np = np.array(img)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(img_np)

white_bg = np.ones_like(enhanced) * 255
mask = enhanced > 0
result = np.where(mask, enhanced, white_bg)

cv2.imwrite('source-prepped.png', result)
