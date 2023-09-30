import cv2
from deepface import DeepFace
import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

numpyImages = load_images_from_folder('registered_users')

img2 = cv2.imread('img2.jpg')

for i in range(5):
    ans = []
    for images in numpyImages:
        result = DeepFace.verify(img2, images, enforce_detection=False)
        ans.append(result['verified'])
    print(ans)
    ans.clear()
