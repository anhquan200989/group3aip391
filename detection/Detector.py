from imutils.video import FPS
from utils import *
import math

enlarge = 40

class Detector:
    def __init__(self, use_cuda=False):
        # read model
        self.faceModel = cv2.dnn.readNetFromCaffe('models/res10_300x300_ssd_iter_140000.prototxt',
                                                  caffeModel='models/res10_300x300_ssd_iter_140000.caffemodel')
        if use_cuda:
            self.faceModel.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.faceModel.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def processImage(self, imgName):
        self.img = cv2.imread(imgName)
        (self.height, self.width) = self.img.shape[:2]
        self.processFrame()
        cv2.imshow('Output', self.img)
        cv2.waitKey(0)

    def processFrame(self, known_face_encodings, known_face_names):
        bboxes = []
        face_names = []
        distances = []
        blob = cv2.dnn.blobFromImage(self.img, 1.0, (300, 300), (104.0, 107.0, 123.0), swapRB=False, crop=False)
        self.faceModel.setInput(blob)
        predictions = self.faceModel.forward()

        for i in range(0, predictions.shape[2]):
            if predictions[0, 0, i, 2] > 0.5:
                bbox = predictions[0, 0, i, 3:7] * np.array([self.width, self.height, self.width, self.height])
                (xmin, ymin, xmax, ymax) = bbox.astype('int')
                xmin, ymin, xmax, ymax = xmin-enlarge, ymin-enlarge, xmax+enlarge, ymax
                bboxes.append((xmin, ymin, xmax - xmin, ymax - ymin))
                # face_bbox = [(ymin, xmax, ymax, xmin)]
                face_bbox = [(ymin // 4, math.ceil(xmax / 4), math.ceil(ymax / 4), xmin // 4)]
                label, dist = get_face_label(known_face_encodings, known_face_names, face_bbox, self.img)
                face_names.append(label)
                distances.append(dist)
                # cv2.rectangle(self.img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)

        return face_names, bboxes, distances

    def processVideo(self, videoName):
        known_face_encodings, known_face_names = get_from_data("../checkout_images/raw/*/*.jpg")
        process_this_frame = True

        cap = cv2.VideoCapture(videoName)
        if not cap.isOpened():
            print('False to open video')
            return
        while cap.isOpened():
            ret, self.img = cap.read()
            self.height, self.width = self.img.shape[:2]

            fps = FPS().start()

            while ret:
                if process_this_frame:
                    face_names, bboxes, distances = self.processFrame(known_face_encodings, known_face_names)

                process_this_frame = not process_this_frame
                for bbox, name, dist in zip(bboxes, face_names, distances):
                    cv2.putText(self.img, str(name), (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
                    cv2.putText(self.img, str(dist), (bbox[0], bbox[1]+bbox[3]+20), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
                    cv2.rectangle(self.img, bbox, (255, 0, 255), 2)

                cv2.imshow('Output', self.img)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break

                fps.update()
                ret, self.img = cap.read()

            fps.stop()
            print(f'Elapsed time: {fps.elapsed():.2f}')
            print(f'FPS: {fps.fps():.2f}')

            cap.release()
            cv2.destroyAllWindows()
