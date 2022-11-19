# ### Import Libraries

# In[47]:


# !pip install opencv-python
# !pip install extcolors
# !pip install colormap
# !pip install easydev

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as patches
import matplotlib.image as mpimg

from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2
import extcolors

from colormap import rgb2hex


# ### Convert RGB colors to HEX

# In[9]:


def color_to_df(input):
    colors_pre_list = str(input).replace('([(', '').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')', '') for i in colors_pre_list]

    # convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                           int(i.split(", ")[1]),
                           int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]

    df = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurence'])
    return df


# ### Create Donut Chart

# In[10]:


def donut_chart(list_precent, list_color, resize_name, ax1):
    text_c = [c + ' ' + str(round(p * 100 / sum(list_precent), 1)) + '%' for c, p in zip(list_color, list_precent)]
    wedges, text = ax1.pie(list_precent,
                           labels=text_c,
                           labeldistance=1.05,
                           colors=list_color,
                           textprops={'fontsize': 150, 'color': 'black'})
    plt.setp(wedges, width=0.3)

    img = mpimg.imread(resize_name)
    imagebox = OffsetImage(img, zoom=2.5)
    ab = AnnotationBbox(imagebox, (0, 0))
    ax1.add_artist(ab)


# ### Create Color Palette

# In[11]:


def color_palette(list_color, ax2):
    x_posi, y_posi, y_posi2 = 160, -170, -170
    for c in list_color:
        if list_color.index(c) <= 5:
            y_posi += 180
            rect = patches.Rectangle((x_posi, y_posi), 360, 160, facecolor=c)
            ax2.add_patch(rect)
            ax2.text(x=x_posi + 400, y=y_posi + 100, s=c, fontdict={'fontsize': 190})
        else:
            y_posi2 += 180
            rect = patches.Rectangle((x_posi + 1000, y_posi2), 360, 160, facecolor=c)
            ax2.add_artist(rect)
            ax2.text(x=x_posi + 1400, y=y_posi2 + 100, s=c, fontdict={'fontsize': 190})


# ### Extract Color

# In[33]:


def extract_color(input_image, resize, tolerance):
    bg = 'bg.png'
    fig, ax = plt.subplots(figsize=(192, 108), dpi=10)
    fig.set_facecolor('white')
    plt.savefig(bg)
    plt.close(fig)

    # resize
    output_width = resize
    img = Image.open(input_image)
    if img.size[0] >= resize:
        wpercent = (output_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((output_width, hsize), Image.ANTIALIAS)
        resize_name = 'resize_' + input_image
        img.save(resize_name)
    else:
        resize_name = input_image

    # crate dataframe
    img_url = resize_name
    colors_x = extcolors.extract_from_path(img_url, tolerance=tolerance, limit=13)
    df_color = color_to_df(colors_x)

    # annotate text
    list_color = list(df_color['c_code'])
    list_precent = [int(i) for i in list(df_color['occurence'])]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(160, 120), dpi=10)

    donut_chart(list_precent, list_color, resize_name, ax1)
    color_palette(list_color, ax2)

    fig.set_facecolor('white')
    ax2.axis('off')
    bg = plt.imread('bg.png')
    # plt.imshow(bg)
    plt.tight_layout()

    output_name = 'output_' + input_image
    plt.savefig(output_name)
    return output_name


