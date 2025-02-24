
import cv2
import numpy as np


def collage_creation(image_paths):
    n = int(len(image_paths) ** 0.5)
    images = []
    img_dim = 900 // n
    for i in range(len(image_paths)):
        images.append(cv2.imread(image_paths[i]))
    for i in range(len(image_paths)):
        images[i] = cv2.resize(images[i], (img_dim, img_dim))

    # Create a blank canvas for the collage
    collage = np.zeros((900, 900, 3), dtype=np.uint8)

    cnt = 0
    for i in range(0, 900, img_dim):
        for j in range(0, 900, img_dim):
            collage[i:i + img_dim, j:j + img_dim] = images[cnt]
            cnt += 1

    cv2.imwrite("collages/collage.jpg", collage)

imgs = ['uploads/cuteTuring.png', 'uploads/apple jack.png', 'uploads/rainbow dash.png', 'uploads/fluttershy.jpg']
collage_creation(imgs)