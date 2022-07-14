import cv2
import mediapipe as mp
import time
import os

# num_know_faces = len(os.listdir("../checkout_images/raw"))
num_know_faces = 0
enlarge = 40


class FaceDetector:
    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(0.75)

    def findFaces(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        # print(self.results)
        bboxs = []
        if self.results.detections:
            detection = self.results.detections[0]
            # print(detection.location_data.relative_bounding_box)
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            bboxs.append([bbox, detection.score])
            # cv2.rectangle(img, bbox, (255, 0, 255), 2)
            # cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0],bbox[1]-20), cv2.FONT_HERSHEY_PLAIN,
            # 2, (255,0,255), 2)
        return img, bboxs


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceDetector()
    idx = num_know_faces + 1
    count = 1

    while True:
        _, img = cap.read()
        img, bboxs = detector.findFaces(img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        if len(bboxs) != 0:
            x, y, w, h = bboxs[0][0]
            imgRoi = img[y-enlarge:y+h+enlarge, x-enlarge:x+w+enlarge]
            if imgRoi.shape[0] * imgRoi.shape[1] > 0:
                cv2.imshow('ROI', imgRoi)

            # Press 'a' to take picture of new person
            if cv2.waitKey(1) & 0xFF == ord('a'):
                idx += 1
                count = 1
                print(f'Move to person {idx}')

            # Press 's' to save face of the person
            if cv2.waitKey(1) & 0xFF == ord('s'):
                if not os.path.exists(f"../checkout_images/raw/{idx}"):
                    os.makedirs(f"../checkout_images/raw/{idx}")

                cv2.imwrite(f"../checkout_images/raw/{idx}/{count}.jpg", imgRoi)
                cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX,
                            2, (0, 0, 255), 2)
                count += 1
                addAgain = input("Add another picture? ")
                if addAgain == 'y':
                    continue
                else:
                    add_Bill()  # string
                   
                    
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
        cv2.imshow('Face', img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
