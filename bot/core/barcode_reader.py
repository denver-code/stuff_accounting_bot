import cv2

bd = cv2.barcode.BarcodeDetector('sr.prototxt', 'sr.caffemodel')

def retval_code(image):
    retval, decoded_info, decoded_type, points = bd.detectAndDecode(image)
    if not retval:
        return [400, "Looks like you have wrong image without proper barcode, please make sure on picture are only one proper barcode"]

    return [200, decoded_info[0]]
