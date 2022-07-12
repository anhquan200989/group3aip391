from facenet_pytorch import MTCNN
import math
from utils import *


def recognition(rects, known_face_encodings, known_face_names, frame, enlarge=40):
    bboxes = []
    face_names = []
    for bbox in rects:
        bbox = list(map(int, bbox.tolist()))
        x, y, x1, y1 = bbox
        bboxes.append((x, y, x1-x, y1-y))
        x, y, x1, y1 = x-enlarge, y-enlarge, x1+enlarge, y1+enlarge
        face_bbox = [(y // 4, math.ceil(x1 / 4), math.ceil(y1 / 4), x // 4)]
        # face_bbox = [(y // 4, math.ceil((x + w) / 4), math.ceil((y + h) / 4), x // 4)]
        label = get_face_label(known_face_encodings, known_face_names, face_bbox, frame)
        face_names.append(label)
    return bboxes, face_names


if __name__ == "__main__":
    cap = cv2.VideoCapture('../test_videos/vid_2.mp4')

    detector = MTCNN(device='cuda')
    cap.set(cv2.CAP_PROP_FPS, 60)
    bboxes = []
    face_names = []

    known_face_encodings, known_face_names = get_from_data("../checkout_images/raw/*/*.jpg")
    process_this_frame = True

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (900, 500))
        rects, _ = detector.detect(frame)

        if process_this_frame and rects is not None:
            if bboxes is not None:
                bboxes, face_names = recognition(rects, known_face_encodings,
                                                 known_face_names, frame)

        process_this_frame = not process_this_frame

        for bbox, name in zip(bboxes, face_names):
            cv2.putText(frame, str(name), (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 255), 2)
            cv2.rectangle(frame, bbox, (255, 0, 255), 2)

        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
