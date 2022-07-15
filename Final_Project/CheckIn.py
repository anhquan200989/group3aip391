from Detector import *


def main():
    add_Item_from_file()
    add_Bill_from_file()
    detector = Detector(use_cuda=False)
    detector.checkInVideo(0)
# if customer moves into camera zone, show face picture
# if customer moves out of camera zone, stop display face picture

if __name__ == '__main__':

    main()
