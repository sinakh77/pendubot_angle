import cv2
import math
import numpy as np
import os
import random

def GetContours(image):
    contours,hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #area 9200
        if area >500:

            cv2.drawContours(img2, cnt, -1, (0, 255, 0), 2)
            peri = cv2.arcLength(cnt,True)

            approx  = cv2.approxPolyDP(cnt,0.0148*peri,True)
            list1 = approx.tolist()

            if len(approx) == 4:
                for num in range(len(approx)):
                    x_num = list1[num][0][0]
                    y_num = list1[num][0][1]
                    cv2.circle(img2, (x_num, y_num), 4, (0, 0, 255), 2)

                for j in range(len(approx)):
                    for i in range(len(approx)):
                        if i < len(approx) - 1:
                            if list1[i][0][1] > list1[i + 1][0][1]:
                                list1[i][0], list1[i + 1][0] = list1[i + 1][0], list1[i][0]
                Min_Distance = math.sqrt((list1[0][0][0]-list1[1][0][0])**2+(list1[0][0][1]-list1[1][0][1])**2)
                for n in (2,3):
                    distance = math.sqrt((list1[0][0][0] - list1[n][0][0])**2+(list1[0][0][1] - list1[n][0][1])**2)
                    if distance < Min_Distance:
                        list1[n][0], list1[1][0] = list1[1][0], list1[n][0]
                if len(approx) > 3:
                    x_p1 = (list1[0][0][0] + list1[1][0][0]) / 2
                    y_p1 = (list1[0][0][1] + list1[1][0][1]) / 2
                    x_p2 = (list1[2][0][0] + list1[3][0][0]) / 2
                    y_p2 = (list1[2][0][1] + list1[3][0][1]) / 2
                    cv2.line(img2, (int(x_p1), int(y_p1)), (int(x_p2), int(y_p2)), (0, 0, 255), 2)
                    a = (x_p1 - x_p2)
                    b = (y_p2 - y_p1)

                    try :
                        tetha = math.atan(a / b)
                    except ZeroDivisionError:
                            tetha = 1.57
                            print('Zero Divison Occured!')
                    # cv2.putText(img2,f"Angle={str(round(math.degrees(tetha),2))}",
                    #             (50, 50), cv2.FONT_HERSHEY_SIMPLEX,1,
                    #             (0, 255, 0), 2,
                    #             cv2.LINE_AA)
                    # print('Tetha =', math.degrees(tetha))
                    x, y, width, height = cv2.boundingRect(approx)
                    # adding random width and heigh to the ROI
                    random_width = random.randint(-20,0)
                    random_height = random.randint(-20,0)
                    # REGION OF INTEREST
                    ROI = img[y:y + (height + random_height), x:x + (width + random_width)]
                    blurred_ROI = blur(ROI)
                    img[y:y + (height + random_height), x:x + (width + random_width)] = blurred_ROI




def blur(image):
    # gaussian blur
    gaussian_img = cv2.GaussianBlur(image,(25,25),0)
    # median blur
    median_img = cv2.medianBlur(image,9)
    # bilateral blur
    bilateral_img = cv2.bilateralFilter(image,9,75,75)
    # 2D convolutional
    average = 1
    kernel = np.ones((average,average), np.float32) / (average ^ 2)
    filtered_img = cv2.filter2D(image,-1,kernel)

    return gaussian_img




path = r'C:\Users\Cna\Downloads\CV'
for filename in os.listdir(path):
    if filename.endswith(".png"):
        image_path = os.path.join(path, filename)
        img = cv2.imread(image_path)
        img2 = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # THRESHOLDING PARAMETER FOR A SPECIFIC DATASET
        thresh_parameter = 50

        ret, thresh1 = cv2.threshold(imgGray, thresh_parameter, 255, cv2.THRESH_BINARY)
        imgCanny = cv2.Canny(thresh1, 250, 250)
        # cv2.imshow('1', imgCanny)
        GetContours(imgCanny)
        # cv2.imshow('2',final_img)
        # final_img_gaussian, final_img_median, final_img_bilateral, final_img_convolutional = blur(img)
        # cv2.imshow('image', img)
        New_path = r'C:\Users\Cna\Downloads\CV\Blurred_images'
        Final_path = os.path.join(New_path, filename)
        cv2.imwrite(Final_path, img)
        continue
    else:
         continue

# cv2.imshow('Gaussian',final_img_gaussian)
# cv2.imshow('Median',final_img_median)
# cv2.imshow('Bilateral',final_img_bilateral)
# cv2.imshow('2D filter',final_img_convolutional)



cv2.waitKey(0)
cv2.destroyAllWindows()