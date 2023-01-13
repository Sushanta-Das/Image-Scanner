import cv2
import numpy as np
from PIL import Image
kernel=np.ones((5,5),np.uint8)



######## Functions #############################

def wrap(arr):
    pt1=np.float32(arr)
    pt2=np.float32([[0,0],[width,0],[0,height],[width,height]])
    print(pt1)
    matrix=cv2.getPerspectiveTransform(pt1,pt2)
    imgout=cv2.warpPerspective(grey,matrix,(width,height))
    return imgout


def getmaxContour(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    maxarea=0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if(area>55):
            peri=cv2.arcLength(cnt,True)
            if(area>maxarea):
                maxarea=area
                approx=cv2.approxPolyDP(cnt,0.01*peri,True)
          
    pts=np.squeeze(approx)
    print("approx")
    cv2.drawContours(imgcontor,approx,-1,(240, 255, 60),20)
    print("points",pts)
    add=np.sum(pts,axis=1)
    diff=np.diff(pts,1,1)
    arr=np.array([pts[np.argmin(add)],pts[np.argmin(diff)],pts[np.argmax(diff)],pts[np.argmax(add)]])
    return arr



#######################  Main ##########################

img=cv2.imread("questionpaper.jpg")
l=(img.shape)
img=cv2.resize(img,(l[1]//3,l[0]//3))
l=(img.shape)
width=l[1];height=l[0]


grey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
bilateralblur=cv2.medianBlur(grey,5)
imgcontor=grey.copy()
canny=cv2.Canny(bilateralblur,100,150,1)
imgDilation=cv2.dilate(canny,kernel,iterations=1)
arr=getmaxContour(imgDilation)
print("arr")
print(arr)
imgout=wrap(arr)
cv2.imshow("TEST",imgDilation)

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",500,800)
def empty(a):
    pass
cv2.createTrackbar("BOX Size","Trackbars",31,179,empty)
cv2.createTrackbar("C","Trackbars",1,179,empty)
while True:
    box=cv2.getTrackbarPos("BOX Size","Trackbars")
    if box % 2==0:
        box+=1
    if box==1:box=3    
    C=cv2.getTrackbarPos("C","Trackbars")
    thres=cv2.adaptiveThreshold(imgout,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,box,C)
    cv2.imshow("Output",thres)
    cv2.imshow("Corners",imgcontor)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
###################### after running when image windows shows , press q to save result image as pdf 
##################### Also change the value of Box size and C in trackbar fit get perfect clear image
cv2.imwrite("result.jpg",thres)
path='./result.jpg'
pdf=Image.open(path)
pdf.save('./resultpdf.pdf')


