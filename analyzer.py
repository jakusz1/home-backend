from collections import Counter
from urllib import request

import cv2
import numpy as np
from sklearn.cluster import KMeans


def _filter_colors_by_min_diversity(colors, min_diversity):
    filtered_colors = []

    for color in colors:
        red, green, blue = (int(param) for param in color)
        if abs(red - green) + abs(green - blue) + abs(blue - red) > min_diversity:
            filtered_colors.append(color)
    return filtered_colors


def _get_colors_from_url(url):
    response = request.urlopen(url)
    bgr_image = cv2.imdecode(
        np.asarray(bytearray(response.read()), dtype="uint8"), cv2.IMREAD_COLOR)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    return rgb_image.reshape(bgr_image.shape[0] * bgr_image.shape[1], 3)


def _get_dominant_color(colors, n_clusters):
    clf = KMeans(n_clusters=min(len(colors), n_clusters))
    counts = Counter(clf.fit_predict(colors))
    center_colors = clf.cluster_centers_
    best_color, best_score = None, 0

    for counter in range(center_colors.shape[0]):
        score = counts[counter]
        if score > best_score:
            best_color = center_colors[counter]
            best_score = score
    return [int(param) for param in best_color]


def get_color_from_album_url(album_url, n_clusters=4, color_min_diversity=100):
    colors = _get_colors_from_url(album_url)
    filtered_colors = _filter_colors_by_min_diversity(colors, color_min_diversity)
    if filtered_colors:
        return _get_dominant_color(filtered_colors, n_clusters)
    return []
