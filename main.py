import math
import socket,struct
import cv2
import numpy as np
from timeit import default_timer as timer



#setting up the connection
# TCP_IP = ''
# TCP_PORT =  12345
# BUFFER_SIZE = 1024
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.bind((TCP_IP,TCP_PORT))
# print("Waiting For Simulink To Start")
# s.listen(1)
# conn,addr = s.accept()
# print('Connection Address: ',addr)


def GetContours(image):
    contours,hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #area 9200
        if area >3200:

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
                    cv2.putText(img2,f"Angle={str(round(math.degrees(tetha),2))}",
                                (50, 50), cv2.FONT_HERSHEY_SIMPLEX,1,
                                (0, 255, 0), 2,
                                cv2.LINE_AA)



                    #if x_p2<140:
                       # tetha = tetha-3.141592
                    #if x_p2>215:
                        #tetha = tetha+3.141592



                    # command = round(math.degrees(tetha),2)
                    # msg = struct.pack('<d',command)
                    # conn.send(msg)
                    print('Tetha =',math.degrees(tetha))
                    x, y, w, h = cv2.boundingRect(approx)
                    ROI = img[y:y+h, x:x+w]
                    blur = cv2.GaussianBlur(ROI, (25, 25), 0)
                    img[y:y+h, x:x+w] = blur
                    cv2.imshow('blur',img)

            # Max_x = list1[0][0][0]
            # Min_y = list1[0][0][1]
            # for i in range(len(approx)):
            #         if list1[i][0][0] > Max_x:
            #             Max_x=list1[i][0][0]
            #
            # for j in range(len(approx)):
            #     if list1[j][0][1] < Min_y:
            #         Min_y = list1[j][0][1]
            # print(Min_y)
            # print(Max_x)

cap = cv2.VideoCapture(0)
cap.set(3,800)
cap.set(4,600)

labels_file = open('labeles.csv', 'w')
labels_file.write('filename,angle\n')
while True:
    start = timer()
    success,img1 =cap.read()
    img = img1
    img2 = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # sharpen = cv2.filter2D(img2, -1, sharpen_kernel)
    ret, thresh1 = cv2.threshold(imgGray, 70, 255, cv2.THRESH_BINARY)
    # ret, thresh2 = cv2.threshold(sharpen, 150, 255, cv2.THRESH_BINARY)
    # thresh3 = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    imgCanny = cv2.Canny(thresh1, 250, 250)
    GetContours(imgCanny)
    #print(cap.get(cv2.CAP_PROP_FPS))
    # cv2.imshow("Raw Image",img1)
    cv2.imshow("Final Image",img2)
    cv2.imshow('Binary Thresholding',thresh1)
    # cv2.imshow('Canny Edge Detection',imgCanny)
    elapsed_time = timer()-start
    # print(f"elapsed time = {elapsed_time}")
    # for count in range(0, 1000):
    #     image_name = 'Pic_' + str(count) + '.png'
    #     cv2.imwrite(image_name, img2)
    #     labels_file.write(image_name + ',' + str(angle) + '\n')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break