import numpy as np
import cv2
from sklearn.cluster import KMeans
import json

def get_dominant_colors(image, k=5):
    image = cv2.imread(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image)

    colors = kmeans.cluster_centers_
    colors = colors.astype(int)

    hex = []
    for col in colors:
        r, g, b = col[0], col[1], col[2]
        hex.append(f"#{r:02x}{g:02x}{b:02x}".upper())

    json_string = json.dumps(hex)


    return json_string