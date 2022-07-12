from Detector import *

detector = Detector(use_cuda=True)

detector.processVideo('../test_videos/vid_2.mp4')
