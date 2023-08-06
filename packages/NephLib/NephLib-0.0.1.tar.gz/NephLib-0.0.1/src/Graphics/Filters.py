import cv2

def High_Pass_Filter(input_image:str):
    source_image = cv2.imread(input_image)
    filtered_image = source_image - cv2.GaussianBlur(source_image, (21, 21), 3) + 127
    return filtered_image

if __name__ == '__main__':
    from sys import argv
    image_in = cv2.imread(argv[1])
    image_out = High_Pass_Filter(argv[1])
    cv2.imshow("Original", image_in)
    cv2.imshow("High Pass Filter", image_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit()