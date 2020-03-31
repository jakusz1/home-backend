from collections import Counter
from urllib import request
from sklearn.cluster import KMeans

import cv2
import numpy as np

def _filter_rgb_by_diversity(rgb_list, threshold):
    filtered_rgb_list = []

    for rgb in rgb_list:
        red = int(rgb[0])
        green = int(rgb[1])
        blue = int(rgb[2])

        if abs(red - green) + abs(green - blue) + abs(blue - red) > threshold:
            filtered_rgb_list.append(rgb)

    return filtered_rgb_list

def get_color_from_album_url(album_url, number_of_colors=4, color_diversity_threshold=100):
    response = request.urlopen(album_url)
    image = cv2.imdecode(np.asarray(bytearray(response.read()), dtype="uint8"), cv2.IMREAD_COLOR)
    rgb_matrix = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).reshape(image.shape[0] * image.shape[1], 3)
    filtered_rgb_list = _filter_rgb_by_diversity(rgb_matrix, color_diversity_threshold)

    if filtered_rgb_list:
        clf = KMeans(n_clusters=min(len(filtered_rgb_list), number_of_colors))
        labels = clf.fit_predict(filtered_rgb_list)
        counts = Counter(labels)
        center_colors = clf.cluster_centers_
        best_rgb, best_score = [0, 0, 0], 0

        for i in range(center_colors.shape[0]):
            score = counts[i]
            if score > best_score:
                best_rgb = center_colors[i]
                best_score = score

        return [int(color) for color in best_rgb]
        
    return []
