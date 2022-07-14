import mediapipe as mp
import time
from utils import *
import math

x_vid_0 = 500
y_vid_0 = 270

# ví dụ về lịch sử mua hàng có key là id khách hàng
customer_info = {
    '1': '10 eggs, 1 bottle of water',
    '2': '1 bottle of milk, 5 apples',    
    '3': 'pork, beef',
    '4': 'chicken, fish',
    '5': 'banh m
}


class FaceDetector:
    def __init__(self, minDetectionCon=0.5):
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(minDetectionCon)

    def findFaces(self, img, known_face_encodings, known_face_names):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        # print(self.results)
        bboxes = []
        face_names = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
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

                face_bbox = [(y // 4, math.ceil((x + w) / 4), math.ceil((y + h) / 4), x // 4)]
                label = get_face_label(known_face_encodings, known_face_names, face_bbox, img)
                face_names.append(label)
        return face_names, img, bboxes


def main():
    customers = []
    # lấy encoding feature của mặt cùng với id
    known_face_encodings, known_face_names = get_from_data("../checkout_images/raw/*/*.jpg")

    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('../test_videos/vid_2.mp4')
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
        x, y = 0, 0
        for bbox, name in zip(bboxes, face_names):
            cv2.putText(img, str(name), (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 255), 2)
            cv2.rectangle(img, bbox, (255, 0, 255), 2)
            if name not in customers and name != 'Unknown':
                print(f'Customer ID {name}:', customer_info[name])
                customers.append(name)

        try:
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
        except Exception as e:
            continue

        for name in customers:
            face = cv2.imread(f"../checkout_images/raw/{name}/1.jpg")
            face = cv2.resize(face, (224, 224))
            label = 'Id ' + str(name)
            if x > 1920:
                x += face.shape[1]
                y = 0
	    # show ảnh customer tìm được lên màn hình	
            cv2.imshow(label, face)
            cv2.moveWindow(label, x, y)
            y += face.shape[0] + 50

        window = 'Video'
        cv2.imshow(window, cv2.resize(img, (960, 540)))
        cv2.moveWindow(window, x_vid_0, 120)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
