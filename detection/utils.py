import os
import glob
import face_recognition
import cv2
import numpy as np


def get_face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    try:
        encoding = face_recognition.face_encodings(image)[0]
    except Exception as e:
        encoding = face_recognition.face_encodings(image)
    return encoding


def get_face_label(known_face_encodings, known_face_names, face_locations, frame, thres=0.45):
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # plt.imshow(rgb_small_frame)
    # plt.show()
    # cv2.imshow('Image', rgb_small_frame)

    # Find all the faces and face encodings in the current frame of video
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]

    name = 'Unknown'
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encodings)

    # # If a match was found in known_face_encodings, just use the first one.
    # if True in matches:
    #     first_match_index = matches.index(True)
    #     name = known_face_names[first_match_index]

    face_distances = face_recognition.face_distance(known_face_encodings, face_encodings)
    best_match_index = np.argmin(face_distances)
    dist = face_distances[best_match_index]
    if matches[best_match_index] and dist < thres:
        name = known_face_names[best_match_index]
    return name, dist


def get_from_data(format_path):
    known_face_encodings = []
    known_face_names = []

    image_paths = glob.glob(format_path)

    for path in image_paths:
        known_face_encodings.append(get_face_encoding(path))
        known_face_names.append(path.split(os.path.sep)[-2])

    return known_face_encodings, known_face_names
