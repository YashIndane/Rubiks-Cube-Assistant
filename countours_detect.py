import cv2
import numpy as np
import math


cap = cv2.VideoCapture(0)

def check_if_square(P1 , P2) -> bool : 
   
   d1 = math.dist(P1[0] , P2[1])
   d2 = math.dist(P1[1] , P2[0])

   return abs(d1 - d2)  < 2


tile_coordinates = []
while True : 
    success, img_org = cap.read()

    gray = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 20, 40)

    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations = 1)

    (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)





    tile_counter = 0
    countours_counter = 0
    font = cv2.FONT_HERSHEY_COMPLEX 


    for cnt in contours : 

         area = cv2.contourArea(cnt) 
         coordinates = []
         
    
            # Capturing grid squares by area 
         if area < 3000 and area > 1000 :  
                approx = cv2.approxPolyDP(cnt,   0.03 * cv2.arcLength(cnt, True), True) 
    
                # Only grabbing 4 sided polygons
                if(len(approx) == 4):  
                     
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

                      if check_if_square(P1 , P2) : 

                        cv2.drawContours(img_org, [approx], 0, (20, 255 , 57), 2)

                        if all([abs(P1[0][0] - x) > 50 or abs(P1[0][1] - y) > 50 for x , y in tile_coordinates]) : 

                              tile_coordinates.append(P1[0])

                              if len(tile_coordinates) == 9 : 

                                 print(tile_coordinates)
                                 tile_coordinates = []

                                  
                              
                        

    cv2.imshow('Screen' , img_org)



    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
