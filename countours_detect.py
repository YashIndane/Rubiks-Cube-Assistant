import cv2
import numpy as np
import math


cap = cv2.VideoCapture(0)

def check_if_square(P1 , P2) : 
   
   d1 = math.dist(P1[0] , P2[1])
   d2 = math.dist(P1[1] , P2[0])

   return abs(d1 - d2)  < 2


while True : 
    success, img_org = cap.read()

    gray = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 20, 40)

    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=2)

    (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)





   
    font = cv2.FONT_HERSHEY_COMPLEX 
    for cnt in contours : 
         area = cv2.contourArea(cnt) 
         coordinates = []
    
            # Capturing grid squares by area 
         if area < 3000 and area > 1000 :  
                approx = cv2.approxPolyDP(cnt,   0.03 * cv2.arcLength(cnt, True), True) 
    
                # Only grabbing 4 sided polygons
                if(len(approx) == 4):  
                      #cv2.drawContours(img_org, [approx], 0, (0, 0, 255), 2) 

                      n = approx.ravel()  
                      i = 0
                      
                      for j in n : 
                        if(i % 2 == 0): 
                           x_c = n[i] 
                           y_c = n[i + 1] 
                           coordinates.append([x_c , y_c])

                        i += 1   

                      coordinates = sorted(coordinates , key = lambda x : x[0])
                      P1 = coordinates[:2]
                      P2 = coordinates[2:]

                      P1 = sorted(P1 , key = lambda z : z[1])
                      P2 = sorted(P2 , key = lambda q : q[1])

                      if check_if_square(P1 , P2) : cv2.drawContours(img_org, [approx], 0, (20, 255 , 57), 2) 

  
                          


    cv2.imshow('Screen' , img_org)



    if cv2.waitKey(1) & 0xFF == ord('q'):
            break