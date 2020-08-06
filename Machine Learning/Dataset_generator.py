import cv2
import csv



with open('Colours_Dataset_25.csv' ,  'w' , newline = '') as f :

 for x in range (6) : 

   address = str(x) + '.png'  

   img = cv2.imread(address)
   rows , cols , _ = img.shape

  
   for i in range(rows) : 
      for j in range(cols) : 

          data_row = []
          for pixel_value in img[i][j] : data_row.append(pixel_value)

          data_row.append(x + 1)

          writer = csv.writer(f)
          writer.writerow(data_row) 

          cv2.waitKey()

f.close()
         

