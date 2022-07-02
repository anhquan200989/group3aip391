import face_recognition
import cv2
import os

# num_know_faces = len(os.listdir("../checkout_images/raw")) - 3
num_know_faces = 0

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []

while True:
    idx = num_know_faces + 1
    count = 1

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face detection processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(small_frame, model="cnn")

    # Display the results
    for top, right, bottom, left in face_locations:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Extract the region of the image that contains the face
        face_image = frame[top:bottom, left:right]

        # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)

        if cv2.waitKey(1) & 0xFF == ord('a'):
            idx += 1
            count = 1
            print(f'Move to person {idx}')

        if cv2.waitKey(1) & 0xFF == ord('s'):
            if not os.path.exists(f"../checkout_images/raw/{idx}"):
                os.makedirs(f"../checkout_images/raw/{idx}")

            cv2.imwrite(f"../checkout_images/raw/{idx}/{count}.jpg", face_image)
            cv2.rectangle(frame, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX,
                        2, (0, 0, 255), 2)
            count += 1

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
