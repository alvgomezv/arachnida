# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alvgomez <alvgomez@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 13:50:20 by alvgomez          #+#    #+#              #
#    Updated: 2023/04/14 16:58:36 by alvgomez         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests
from bs4 import BeautifulSoup
import shutil
import os
import sys

all_images = []
all_links = []
pictures = []

def get_img_urls(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    images = []
    for img in soup.findAll('img'):
        try:
            if img.get('src')[0] == '/':
                if ('https:'+ img.get('src')) not in all_images:
                    images.append('https:'+ img.get('src'))
                    all_images.append('https:'+ img.get('src'))
            else:
                if (img.get('src')) not in all_images:
                    images.append(img.get('src'))
                    all_images.append(img.get('src'))
        except:
            pass
    return images

def picture_format(img):
    format = None
    if img[-4:] == ".jpg":
        format = ".jpg"
    elif img[-5:] == ".jpeg":
        format = ".jpeg"
    elif img[-4:] == ".png":
        format = ".png"
    elif img[-4:] == ".gif":
        format = ".gif"
    elif img[-4:] == ".bmp":
        format = ".bmp"
    return format
        
def get_img_into_folder(images, file="./data", round=0):
    if not os.path.exists(file):
        os.makedirs(file)
    i = 0
    for img in images:
        try:
            req = requests.get(img, stream = True)
            if req.status_code == 200:
                format = picture_format(img)
                if format:
                    for item in pictures:
                        if f"pic_{i}" in item:
                            i += 1
                    src = os.path.join(file, (f"pic_{i}" + format))
                    with open(src, 'wb') as f:
                        shutil.copyfileobj(req.raw, f)
                        pictures.append(src)
        except:
            pass
    
def get_links(url, first_url, n_links=None):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = []
    i = 0
    for link in soup.findAll('a', href=True):
        if n_links != None:
            if i >= n_links:
                return links
        try:
            if first_url in link.get('href'):
                links.append(link.get('href'))
                i += 1
        except:
            pass
    return links
    
def recursive_download(link=None, first_url=None, n_links=None, depth=5, round=0, file="./data"):
    if round >= depth:
        pass
    else: 
        all_links.append(link)
        images = get_img_urls(link)
        get_img_into_folder(images, file, round)
        links = get_links(link, first_url, n_links)
        round += 1
        for url in links:
            if url not in all_links:
                recursive_download(url, first_url, n_links, depth, round, file)  
     
if __name__ == "__main__":
    #number of links
    l = None
    
    if len(sys.argv) == 1:
        print("No url provided")
    elif len(sys.argv) == 2:
        url = sys.argv[1]
        images = get_img_urls(url)
        get_img_into_folder(images)
    elif len(sys.argv) > 5:
        print("To many arguments")
    else:
        if sys.argv[2] == "-r" and len(sys.argv) == 3:
            recursive_download(link=sys.argv[1], first_url=sys.argv[1], n_links=l)
        elif sys.argv[2] == "-p":
            if len(sys.argv) != 4:
                print("No path provided")
            else:
                recursive_download(link=sys.argv[1], first_url=sys.argv[1], n_links=l, file=sys.argv[3])
        elif sys.argv[2] == "-r" and sys.argv[3] == "-l":
            if len(sys.argv) != 5:
                print("Maximum depth needed")
            else:
                d = int(sys.argv[4])
                recursive_download(link=sys.argv[1], first_url=sys.argv[1], n_links=l, depth=d)
    


    