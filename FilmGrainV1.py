# encoding:utf-8
import math 
import cv2
import numpy as np
import random

def gasuss_noise_rgb(h, w, c, mean=0.25, var=0.1):
    ''' 
        添加高斯噪声
        mean : 均值 
        var : 方差
    '''
    noise = np.random.normal(mean, var ** 0.5, [h,w,c])
    out = noise

    return out
    

def SampleGrain(h, w, c, noiseImg, grainSizeX, grainSizeY):
    out = np.zeros((h,w,c), np.float)
    
    #scale into noise texture image space 
    max_x_off = noiseImg.shape[1] - w / grainSizeX
    max_y_off = noiseImg.shape[0] - h / grainSizeY
    
    max_x_off = int(max_x_off)
    max_y_off = int(max_y_off)
    
    #generate random offset 
    x_off = np.random.randint(0, max_x_off)
    y_off = np.random.randint(0, max_y_off)
    
    for i in range(h):
        for j in range(w):
            #Bilear 
           
            pos_x = x_off + j/grainSizeX
            pos_y = y_off + i/grainSizeY
            
            h_coff = math.modf(pos_x)[0]
            v_coff = math.modf(pos_y)[0]
            
            x0 = int(pos_x)
            x1 = x0 + 1
            y0 = int(pos_y)
            y1 = y0 +1 
            
            out[i,j] = (noiseImg[x0,y0] * h_coff + (1-h_coff) * noiseImg[x1,y0]) * v_coff + (1-v_coff)*(noiseImg[x0,y1] * h_coff + (1-h_coff) * noiseImg[x1,y1])
    return out

def FilmGrain(srcImg, noiseImg, grainSizeX, grainSizeY):
    h = srcImg.shape[0]
    w = srcImg.shape[1]
    
    #Sample 
    noises = SampleGrain(srcImg.shape[0],srcImg.shape[1], srcImg.shape[2], noiseImg, grainSizeX, grainSizeY)
    return (noises + srcImg)

    
noise_img = gasuss_noise_rgb(1024,1024,3)
cv2.imwrite("noise.png", noise_img* 255)

srcImg = cv2.imread("test.jpg").astype(float)/255.0

filmgrain =FilmGrain(srcImg, noise_img, 32, 512)

cv2.imwrite("FilmGrain.jpg", filmgrain*255)

