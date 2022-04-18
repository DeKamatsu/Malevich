import cv2

im = cv2.imread("input_images/olen.jpeg")
grey_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey_im)
blur = cv2.GaussianBlur(invert, (21, 21), 0)
inverted_blur = cv2.bitwise_not(blur)
sketch = cv2.divide(grey_im, inverted_blur, scale=256.0)

cv2.imwrite("output files/sketch_olen.png", sketch)
