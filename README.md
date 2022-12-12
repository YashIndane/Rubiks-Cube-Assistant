# Rubiks-Cube-Assistant
![](https://img.shields.io/badge/python-3.8.2-yellowgreen)
![](https://img.shields.io/badge/contributers-1-yellow)
![](https://img.shields.io/badge/license-MIT-red)

A assistant to help you solve a standard Rubik's cube

## Description

### Getting the roi
1.The dataset consists of pixel values in the format of BGR format for each of the colours. The features are B,G,R and the target value is the colour label. For each label 625 rows of data is available.The model is trained on SVM classifier with the linear kernel.

2. The 9 colours on each face of cube is grabbed after filtering the countours by area and shape.

![sample_image1](https://user-images.githubusercontent.com/53041219/207012283-6c607f97-876b-4069-855d-29061870c522.png)

3. After the colours are grabbed , the middle pixel in them is used to predict the colour of whole ROI. This predicted colour values are stored in an array serially for further solving the cube.

### Solving the cube

To see demo click here -> [demo](https://www.linkedin.com/posts/yash-indane-aa6534179_python3-machinelearning-opencv-activity-6700111067638468608-nDUc)

The instructions for solving the cube have been webscrapped from https://ruwix.com/online-rubiks-cube-solver-program/

Installation

`$ pip install selenium`

For doing headless scrapping - 

```py
chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument('--headless')
driver = webdriver.Chrome("<CHROME-DRIVER-PATH>", chrome_options=chrome_opt)
```
