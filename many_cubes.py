import cv2
import numpy as np
import math
import joblib
import solution_generator



cap = cv2.VideoCapture(0)

colours = ['orange' , 'red' , 'green' , 'blue' , 'yellow' , 'white']

s_scalar = joblib.load('Scalar1')
model = joblib.load('model_0.04')

colours_array = ['0' , '0' , '0' , '0' , '0' , '0' , '0' , '0' , '0']
colour_pallet = {'orange':(0,165,255) , 'red':(0,0,255) , 'green':(0,255,0) , 'blue':(255,0,0) , 'yellow':(0,255,255) , 'white':(255,255,255)}

def check_if_square(P1 , P2) -> bool : 
   
   d1 = math.dist(P1[0] , P2[1])
   d2 = math.dist(P1[1] , P2[0])
   return abs(d1 - d2)  < 2

def sketch_cube(ca) : 

    ranges = [(60 , 330) ,(100 , 330) ,(140 , 330) ,(20 , 330) ,(60 , 290) ,(60 , 370)]
    lo , la = 0 , 9

     
    for i in range (int(len(ca) / 9)) : 
        
        nine_chunk = ca[lo : la]
        _x_ , _y_ = ranges[i]
        c_x = _x_

        
        for w , c_ in enumerate(nine_chunk) : 

               if w not in [3 , 6] : 
                 cv2.rectangle(img_org , (_x_ , _y_) , (_x_ + 13 , _y_ + 13) , colour_pallet[c_] , -1)
                 _x_ += 13
               else : 
                 _y_ += 13
                 _x_ = c_x
                 cv2.rectangle(img_org , (_x_ , _y_) , (_x_ + 13 , _y_ + 13) , colour_pallet[c_] , -1)
                 _x_ += 13
     
        lo += 9
        la += 9  
     


def sort_array(TA) -> list : 

   global colours_array

   TA = sorted(TA ,  key = lambda x : x[1])

   Z1 , Z2 , Z3 = TA[0 : 3] , TA[3 : 6] , TA[6 : 9]
   Z1.sort()
   Z2.sort()
   Z3.sort()
   
   temp_array = []
   
   for  x , y in Z1 + Z2 + Z3 : 

      img = img_org[y + 10 : y + 35 , x + 10 : x + 35]
      
      arr = []

      for p in img[12][12] : arr.append(p)

      n_array = np.array([arr])
      arr = s_scalar.transform([arr])

      value = model.predict(arr)

      index = value[0] - 1

      temp_array.append(colours[index])
   
      
   sub_array = colours_array[len(colours_array) - 9 : ]  
  
   not_same = 0
   for h in range(9) : 
       if sub_array[h] != temp_array[h] : not_same += 1

   if not_same >= 4 : colours_array += temp_array
       
      
   if len(colours_array) ==  63 : 
      
       colours_array[58] = 'white'
       sketch_cube(colours_array[9 : ])
       cv2.imshow('Screen' , img_org)

       solution_generator.fill_solve(colours_array[9 : ])

   try : colours_array[58] = 'white'
   except : pass
   
   return colours_array[9 : ]   
  


cs , c = 0 , 0
tile_coordinates = []
face_counter = 0
text_shower = False
font = cv2.FONT_HERSHEY_COMPLEX 

while True : 

    success, img_org = cap.read()

    gray = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 20, 40)

    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations = 0)

    (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
    for cnt in contours : 

         area = cv2.contourArea(cnt) 
       
         if area < 3500 and area > 1500 : # Capturing grid squares by area  
               
                approx = cv2.approxPolyDP(cnt,   0.03 * cv2.arcLength(cnt, True), True) 
                coordinates = []
    
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
                        

                        if all([abs(P1[0][0] - x) > 20 or abs(P1[0][1] - y) > 20 for x , y in tile_coordinates]) :
                              
                              tile_coordinates.append(P1[0])
                              
                              if len(tile_coordinates) == 9 : 

                                 face_counter += 1
                                
                                 if face_counter % 15 == 0 :

                                      cs += 1 
                                      ca = sort_array(tile_coordinates)
                                      face_counter = 0
                                      text_shower = True
                                      c = 0
                                      
                                 tile_coordinates = []
                                 

                                 
    cv2.rectangle(img_org , (20 , 330) , (180 , 370) , (0 , 0 , 0) , -1)
    cv2.rectangle(img_org , (60 , 290) , (100 , 410) , (0 , 0 , 0) , -1)

    try : sketch_cube(ca) 
    except : pass  

    if all([text_shower , c < 5 , cs < 6]) : 
        cv2.putText(img_org , 'Show next face' , (20 , 40) , cv2.FONT_HERSHEY_SIMPLEX , 1 , (0 , 0 , 255) , 2 , cv2.LINE_AA)
        c += 1
    else : 
        text_shower , c = False , 0

    if cs == 6 : 
        cv2.putText(img_org , 'CUBE SOLVED!' , (20 , 40) , cv2.FONT_HERSHEY_SIMPLEX , 1 , (0 , 0 , 255) , 2 , cv2.LINE_AA)
        colours_array = ['0' , '0' , '0' , '0' , '0' , '0' , '0' , '0' , '0']
        cs , c = 0 , 0
        tile_coordinates = []
        face_counter = 0
        text_shower = False
        cv2.rectangle(img_org , (20 , 330) , (180 , 370) , (0 , 0 , 0) , -1)
        cv2.rectangle(img_org , (60 , 290) , (100 , 410) , (0 , 0 , 0) , -1)

    cv2.imshow('Screen' , img_org)

    if cv2.waitKey(1) & 0xFF == ord('q') : break
    
   



                