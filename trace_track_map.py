import cv2
import extcolors
import numpy as np
import PIL.Image as img
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from scipy import signal
from scipy import misc
from array import *
from colormap import rgb2hex

def color_to_df(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    return df

def exact_color(input_image, resize, tolerance, zoom):
    #background
    bg = 'bg.png'
    fig, ax = plt.subplots(figsize=(192,108),dpi=10)
    fig.set_facecolor('white')
    plt.savefig(bg)
    plt.close(fig)
    
    #resize
    output_width = resize
    img = Image.open(input_image)
    if img.size[0] >= resize:
        wpercent = (output_width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((output_width,hsize), Image.ANTIALIAS)
        resize_name = 'resize_'+ input_image
        img.save(resize_name)
    else:
        resize_name = input_image
    
    #crate dataframe
    img_url = resize_name
    colors_x = extcolors.extract_from_path(img_url, tolerance = tolerance, limit = 13)
    df_color = color_to_df(colors_x)
    
    #annotate text
    list_color = list(df_color['c_code'])
    list_precent = [int(i) for i in list(df_color['occurence'])]
    text_c = [c + ' ' + str(round(p*100/sum(list_precent),1)) +'%' for c, p in zip(list_color, list_precent)]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(160,120), dpi = 10)
    
    #donut plot
    wedges, text = ax1.pie(list_precent,
                           labels= text_c,
                           labeldistance= 1.05,
                           colors = list_color,
                           textprops={'fontsize': 150, 'color':'black'})
    plt.setp(wedges, width=0.3)

    #add image in the center of donut plot
    img = mpimg.imread(resize_name)
    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(imagebox, (0, 0))
    ax1.add_artist(ab)
    
    #color palette
    x_posi, y_posi, y_posi2 = 160, -170, -170
    for c in list_color:
        if list_color.index(c) <= 5:
            y_posi += 180
            rect = patches.Rectangle((x_posi, y_posi), 360, 160, facecolor = c)
            ax2.add_patch(rect)
            ax2.text(x = x_posi+400, y = y_posi+100, s = c, fontdict={'fontsize': 190})
        else:
            y_posi2 += 180
            rect = patches.Rectangle((x_posi + 1000, y_posi2), 360, 160, facecolor = c)
            ax2.add_artist(rect)
            ax2.text(x = x_posi+1400, y = y_posi2+100, s = c, fontdict={'fontsize': 190})

    fig.set_facecolor('white')
    ax2.axis('off')
    bg = plt.imread('bg.png')
    plt.imshow(bg)       
    plt.tight_layout()
    return plt.show()

def trace_track():
    ## Get colors specific to each line
    track = img.open('track layout.png')
    red = track.getpixel((227, 193))
    green = track.getpixel((256, 47))

    ## Declare arrays for red and green pixels
    red_pixels = []
    green_pixels = []

    ## Iterate through image
    width, height = track.size
    for i in range(width):
        j = 0
        for j in range(height):
            color = track.getpixel((i,j))
            if color == red:
                red_pixels.append((i,j))
            elif color == green:
                green_pixels.append((i,j))

    ## Plot tracks on empty image
    # Red line plot
    red_rows = len(red_pixels)
    for i in range(red_rows):
        plt.plot(red_pixels[i][0], red_pixels[i][1], 'r.')

    # Green line plot
    green_rows = len(green_pixels)
    for i in range(green_rows):
        plt.plot(green_pixels[i][0], green_pixels[i][1], 'g.')

def processImage(image): 
    image = cv2.imread(image) 
    image = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY) 
    return image

def convolve_track():
    #read image
    src = cv2.imread('D:/cv2-resize-image-original.png', cv2.IMREAD_UNCHANGED)
    print(src.shape)

    #extract red channel
    red_channel = src[:,:,2]

    #write red channel to greyscale image
    cv2.imwrite('D:/cv2-red-channel.png',red_channel)

exact_color('tracklayout.png', 900, 40, 2)