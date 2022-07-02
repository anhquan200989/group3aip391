import cv2
import mediapipe as mp
import time
import glob
import os
# from recognition.recognition import label_realtime, deepface_recognition
# from recognition.arcface_torch.backbones import get_model
# import onnxruntime
from dlib_face_recognition import get_face_label, get_face_encoding
import math

class FaceDetector:
    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(0.75)

    def findFaces(self, img, known_face_encodings, known_face_names):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        # print(self.results)
        bboxes = []
        face_names = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                # print(detection.location_data.relative_bounding_box)
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                bboxes.append(bbox)
                x, y, w, h = bbox

                # img_roi = img[y:y + h, x:x + w]
                # if session:
                #     label_realtime('../checkout_images/embs', img_roi, session)
                # else:
                #     label = deepface_recognition(img_roi)
                #     cv2.putText(img, f'{label}', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                #                 2, (255, 0, 255), 2)

                face_bbox = [(y//4, math.ceil((x+w)/4), math.ceil((y+h)/4), x//4)]
                label = get_face_label(known_face_encodings, known_face_names, face_bbox, img)
                face_names.append(label)
                # cv2.putText(img, str(label), (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                #             2, (255, 0, 255), 2)
                # cv2.rectangle(img, bbox, (255, 0, 255), 2)
                # cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0],bbox[1]-20), cv2.FONT_HERSHEY_PLAIN,
                # 2, (255,0,255), 2)
        return face_names, img, bboxes


def main():
    known_face_encodings = []
    known_face_names = []

    image_paths = glob.glob("../checkout_images/raw/*/*.jpg")

    for path in image_paths:
        known_face_encodings.append(get_face_encoding(path))
        known_face_names.append(path.split(os.path.sep)[-2])

    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture('../test_videos/vid_1.mp4')
    pTime = 0
    detector = FaceDetector()

    # model = '../weights/model.onnx'
    # session = onnxruntime.InferenceSession(model, providers=['CUDAExecutionProvider'])

    # net = get_model('r100', fp16=False).to('cuda')
    # net.load_state_dict(torch.load('../weights/backbone.pth'))
    # net.eval()
    bboxes = []
    face_names = []
    process_this_frame = True
    while True:
        _, img = cap.read()
        if process_this_frame:
            face_names, img, bboxes = detector.findFaces(img, known_face_encodings, known_face_names)

        process_this_frame = not process_this_frame

        for bbox, name in zip(bboxes, face_names):
            cv2.putText(img, str(name), (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 255), 2)
            cv2.rectangle(img, bbox, (255, 0, 255), 2)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
        cv2.imshow('Image', img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
