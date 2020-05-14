import math 
import cv2
import numpy as np

img = np.zeros((1080,1920,3), dtype=np.int16)

def DrawBezier(pts, nPoints):
    for x in range(nPoints):
        t = (1.0 * x) /(nPoints * 1.0);
        k_1_minus_t = 1.0 - t
        k0 = k_1_minus_t * k_1_minus_t * k_1_minus_t
        k1 = 3 * k_1_minus_t * k_1_minus_t * t;
        k2 = 3 * k_1_minus_t * t * t;
        k3 = t * t * t; 
        
        point = k0 * pts[0] + k1 * pts[1] + k2 * pts[2] + k3 * pts[3]
        
        #pt = point
        xx = (int)(point[0]+0.500001)
        yy = (int)(point[1]+0.500001)
        
        img[yy,xx,0] = 0
        img[yy,xx,1] = 0
        img[yy,xx,2] = 0

def AntiAlias(pts, nPoints):
    for x in range(nPoints):
        t = (1.0 * x) /(nPoints * 1.0);
        k_1_minus_t = 1.0 - t
        k0 = k_1_minus_t * k_1_minus_t * k_1_minus_t
        k1 = 3 * k_1_minus_t * k_1_minus_t * t;
        k2 = 3 * k_1_minus_t * t * t;
        k3 = t * t * t; 
        
        point = k0 * pts[0] + k1 * pts[1] + k2 * pts[2] + k3 * pts[3]
        pt = point
        
        xx1 = int(point[0])
        yy1 = int(point[1])
        
        if 1: #2x2 anti alias
            for ii in range(2):
                for jj in range(2):
                    xx = xx1  + ii
                    yy = yy1  + jj
                    distance = (xx - point[0]) * (xx - point[0]) + (yy - point[1]) * (yy - point[1])
                    distance = math.sqrt(distance)           
                    
                    #Blender with original Color
                    img[yy,xx,0] = min(255,int(255 * distance)) * img[yy,xx,0] / 255  
                    img[yy,xx,1] = min(255,int(255 * distance)) * img[yy,xx,0] / 255
                    img[yy,xx,2] = min(255,int(255 * distance)) * img[yy,xx,0] / 255
                    #img[yy,xx,0] = min(min(255,int(255 * distance)) , img[yy,xx,0])
                    #img[yy,xx,1] = min(min(255,int(255 * distance)) , img[yy,xx,0])
                    #img[yy,xx,2] = min(min(255,int(255 * distance)) , img[yy,xx,0])
        
        if 0:
            xx = (int)(point[0]+0.500001)
            yy = (int)(point[1]+0.500001)
            
            img[yy,xx,0] = 0
            img[yy,xx,1] = 0
            img[yy,xx,2] = 0    


def DrawLine(pt1, pt2, color):
    distance = (pt1[0]  - pt2[0])*(pt1[0]  - pt2[0]) + (pt1[1]  - pt2[1])*(pt1[1]  - pt2[1])    
    distance = math.sqrt(distance)
    
    # to have safe points 
    nPoints = int(distance * 1.2)
    for x in range(nPoints):
        t = (1.0 * x) /(nPoints * 1.0);
        k = 1 - t
        point = k * pt1 + t * pt2
        
        xx = (int)(point[0]+0.500001)
        yy = (int)(point[1]+0.500001)
        
        img[yy,xx] = color    


for y in range(1080):              
    for x in range(1920):
        img[y,x,0]= 255
        img[y,x,1]= 255
        img[y,x,2]= 255



if 0:

            # B(t) = (1-t)^3*P0 + 3(1-t)^2*t*P1 + 3 (1-t)*t^2 * P3 + t^3 * P3
            #4 Control Points    

            #  [200, 50],  [200, 650] , [800, 650], [800,50]

            # 800 * 3.14 ~= 2500 Points, 2500 Points may have leaded Points

            #control_points 
            pts = np.zeros((4,2), dtype=np.int16)

            pts[0,0] = 200
            pts[0,1] = 50

            pts[1,0] = 200
            pts[1,1] = 850

            pts[2,0] = 1600
            pts[2,1] = 850

            pts[3,0] = 1600
            pts[3,1] = 50


            DrawBezier(pts, 2500)

            #Increasing Points to 3000
            pts[0,1] = pts[0,1] + 200
            pts[1,1] = pts[1,1] + 200
            pts[2,1] = pts[2,1] + 200
            pts[3,1] = pts[3,1] + 200
                
            DrawBezier(pts, 5000)


            pts[0,1] = pts[0,1] + 200
            pts[1,1] = pts[1,1] + 200
            pts[2,1] = pts[2,1] + 200
            pts[3,1] = pts[3,1] + 200

            AntiAlias(pts, 2500)

# 勾股定理, 1*1+1*1 = 2; 1*1 + sqrt(2) * sqrt(2) = 3; 1*1 + sqrt(3) * sqrt(3) = 4. ....

pts = np.zeros((3,2), dtype=np.int32)

color = np.zeros((3), dtype=np.int16)
red_color = np.zeros((3), dtype=np.int16)

pts[0,0] =  500
pts[0,1] =  600

pts[1,0] =  500
pts[1,1] =  800

color[0] = 0
color[1] = 0
color[2] = 0

red_color[0] = 0
red_color[1] = 0
red_color[2] = 255


DrawLine(pts[0], pts[1], color)

unit_1 = 200

for i in range(13): 
    # compute dx, dy 
    dx = pts[1,0] - pts[0,0]
    dy = pts[1,1] - pts[0,1]
    
    #Vertical switch dx, dy 
    t = dy 
    dy = dx * 1.0
    dx = t  * 1.0
    
    #normalize    
    distance = dx * dx  + dy * dy    
    print(i, dx, dy, distance)
    distance = math.sqrt(distance)
    dx = -dx / distance
    dy = dy / distance
    
    pts[2,0] = int(pts[1,0] + unit_1 * dx)
    pts[2,1] = int(pts[1,1] + unit_1 * dy)
    
    print(pts)
    
    #Draw Vertical Edge
    DrawLine(pts[1], pts[2], color)
    
    #bevel edge
    DrawLine(pts[0], pts[2], red_color)
    
    #Change Pts2 to pts1;
    
    pts[1] = pts[2]  
    
    


cv2.imwrite('sqrt_xx.jpg', img)
cv2.imshow('image',img)
