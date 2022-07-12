import numpy as np
import cv2
from imutils.video import FPS


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

    def processFrame(self):
        blob = cv2.dnn.blobFromImage(self.img, 1.0, (300, 300), (104.0, 107.0, 123.0), swapRB=False, crop=False)
        self.faceModel.setInput(blob)
        predictions = self.faceModel.forward()

        for i in range(0, predictions.shape[2]):
            if predictions[0, 0, i, 2] > 0.5:
                bbox = predictions[0, 0, i, 3:7] * np.array([self.width, self.height, self.width, self.height])
                (xmin, ymin, xmax, ymax) = bbox.astype('int')

                cv2.rectangle(self.img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)

    def processVideo(self, videoName):
        cap = cv2.VideoCapture(videoName)
        if not cap.isOpened():
            print('False to open video')
            return
        while cap.isOpened():
            ret, self.img = cap.read()
            self.height, self.width = self.img.shape[:2]

            fps = FPS().start()

            while ret:
                self.processFrame()
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
