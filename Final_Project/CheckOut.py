from Detector import *

def main():
    detector = Detector(use_cuda=False)
    detector.checkOutVideo(0)

if __name__ == '__main__':
    main()