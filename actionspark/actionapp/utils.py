from urllib import request
import re
import os
import tempfile
import ssl
import cv2
import numpy as np
import imageio
import tensorflow_hub as hub
import tensorflow as tf

UCF_ROOT = "https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101/"
_VIDEO_LIST = None
_CACHE_DIR = tempfile.mkdtemp()
unverified_context = ssl._create_unverified_context()

def list_ucf_videos():
    global _VIDEO_LIST
    if not _VIDEO_LIST:
        index = request.urlopen(UCF_ROOT, context=unverified_context).read().decode("utf-8")
        videos = re.findall("(v_[\w_]+\.avi)", index)
        _VIDEO_LIST = sorted(set(videos))
    return list(_VIDEO_LIST)

def fetch_ucf_video(video):
    cache_path = os.path.join(_CACHE_DIR, video)
    if not os.path.exists(cache_path):
        urlpath = request.urljoin(UCF_ROOT, video)
        print("Fetching %s => %s" % (urlpath, cache_path))
        data = request.urlopen(urlpath, context=unverified_context).read()
        open(cache_path, "wb").write(data)
    return cache_path

def crop_center_square(frame):
    y, x = frame.shape[0:2]
    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y:start_y+min_dim, start_x:start_x+min_dim]

import cv2
import numpy as np

def feature_extraction_external_video(video_path, max_frames=0, resize=(224, 224)):
    # Specify the backend API preference (e.g., cv2.CAP_FFMPEG)
    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)

    frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = crop_center_square(frame)
            frame = cv2.resize(frame, resize)
            frame = frame[:, :, [2, 1, 0]]
            frames.append(frame)

            if max_frames > 0 and len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames) / 255.0


def to_gif(images):
    converted_images = np.clip(images * 255, 0, 255).astype(np.uint8)
    imageio.mimsave('./animation.gif', converted_images, fps=25)
    return embed.embed_file('./animation.gif')

KINETICS_URL = "https://raw.githubusercontent.com/deepmind/kinetics-i3d/master/data/label_map.txt"
with request.urlopen(KINETICS_URL) as obj:
    labels = [line.decode("utf-8").strip() for line in obj.readlines()]
print("Found in total %d labels." % len(labels))

i3d = hub.load("https://tfhub.dev/deepmind/i3d-kinetics-400/1").signatures['default']

def predict(sample_video):
    # Add a batch axis to the sample video.
    model_input = tf.constant(sample_video, dtype=tf.float32)[tf.newaxis, ...]

    logits = i3d(model_input)['default'][0]
    probabilities = tf.nn.softmax(logits)

    top_actions = []
    for i in np.argsort(probabilities)[::-1][:1]:
        top_actions.append({'action': labels[i], 'probability': float(probabilities[i] * 100)})

    return top_actions