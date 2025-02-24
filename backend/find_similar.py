import torch
import numpy as np
import pymysql
import json
from make_collage import *


def hex_to_rgb(hex_color):
    # Convert hex to RGB
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def get_database_colors():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Innuendo-1991',
        database='file_properties'
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, colors FROM file_properties.properties")
            data = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    ids = []
    color_vectors = []

    for row in data:
        id, color_json = row
        parsed_list = json.loads(color_json)
        last = parsed_list[-1]
        ln = len(parsed_list)
        for i in range(5 - ln):
            parsed_list.append(last)
        color_array = []
        for i in range(len(parsed_list)):
            color_array.append(hex_to_rgb(parsed_list[i]))
        color_array = np.array(color_array)
        ids.append(id)
        color_vectors.append(color_array)
    color_vectors = np.array(color_vectors)
    return ids, torch.tensor(color_vectors, dtype=torch.float32)


def find_similar_images(target_colors, n=1):
    ids, color_vectors = get_database_colors()

    # Ensure target_colors is a 2D tensor with shape (1, 15) where 15 is the flattened color vector length
    target_tensor = torch.tensor(target_colors, dtype=torch.float32).view(1, -1)  # Flatten and add batch dimension

    # Flatten the color_vectors to match the target tensor shape
    color_vectors_flattened = color_vectors.view(color_vectors.size(0), -1)

    # Calculate cosine similarity
    similarities = torch.nn.functional.cosine_similarity(color_vectors_flattened, target_tensor, dim=1)

    # Get top n indices
    top_indices = torch.argsort(similarities, descending=True)[:n]

    # Fetch the result ids
    result_ids = [ids[i] for i in top_indices]

    return result_ids


def fetch_filenames(target_colors, n=4):
    similar_ids = find_similar_images(target_colors, n)
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Innuendo-1991',
        database='file_properties'
    )
    cursor = connection.cursor()
    query = "SELECT file_name FROM file_properties.properties WHERE id IN (%s)"
    id_placeholders = ','.join(['%s'] * len(similar_ids))
    query = query % id_placeholders

    cursor.execute(query, tuple(similar_ids))
    photo_filenames = cursor.fetchall()
    print(photo_filenames)
    cursor.close()
    connection.close()
    image_paths = []
    for name in photo_filenames:
        image_paths.append("uploads/"+name[0])
    return image_paths


target_colors = [255, 0, 0] * 5  # TODO: make targetcolors interface in the website
images = fetch_filenames(target_colors, 4)
print(images)
# create_collage(images)
