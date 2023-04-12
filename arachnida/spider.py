# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alvgomez <alvgomez@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 13:50:20 by alvgomez          #+#    #+#              #
#    Updated: 2023/04/12 17:25:10 by alvgomez         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests
from bs4 import BeautifulSoup
import shutil
import os
import sys

def get_img_urls(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        images = []
        for img in soup.findAll('img'):
            try:
                if img.get('src')[0] == '/' and img.get('src')[1] == '/':
                    images.append('https:'+ img.get('src'))
                else:
                    images.append(img.get('src'))
            except:
                pass
        return images
    except:
         pass

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
        
def get_img_into_folder(images, file="./data", pics=0, round=0):
    if not os.path.exists(file):
        os.makedirs(file)
    i = 0
    try:
        for img in images:
            if pics != 0:
                if i >= pics:
                    return
            try:
                req = requests.get(img, stream = True)
                if req.status_code == 200:
                    format = picture_format(img)
                    src = os.path.join(file, (f"pic_{i}_{round}" + format))
                    with open(src, 'wb') as f:
                        shutil.copyfileobj(req.raw, f)
                    i += 1
            except:
                pass
    except:
        pass
    
def get_links(url, n_links=None):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        links = []
        i = 0
        for link in soup.findAll('a', href=True):
            if n_links != None:
                if i >= n_links:
                    return links
            links.append(link.get('href'))
            i += 1
        return links
    except:
         pass
    
def recursive_download(all_images, all_links, link=None, pics=0, n_links=None, i=0, depth=5, round=0, name="./data"):
    if round >= depth:
        pass
    else:
        all_links.append(link)
        images = get_img_urls(link)
        temp = []
        for img in images:
            if img not in all_images:
                temp.append(img)
        images = temp
        all_images += images
        while os.path.exists(name + f"{round}_{i}"):
            i += 1
        file = name + f"{round}_{i}"
        get_img_into_folder(images, file, pics, round)
        links = get_links(link, n_links)
        round += 1
        i = 0
        try:
            for url in links:
                if url not in all_links:
                    recursive_download(all_images, all_links, url, pics, n_links, i, depth, round, name)
                    i += 1
        except:
            pass
     
if __name__ == "__main__":
    #number of links
    l = None
    #number of pictures to download
    p = 0
    
    all_links = []
    all_images = []
    if len(sys.argv) == 1:
        print("No url provided")
    elif len(sys.argv) == 2:
        url = sys.argv[1]
        images = get_img_urls(url)
        get_img_into_folder(images, pics=p)
    elif len(sys.argv) > 5:
        print("To many arguments")
    else:
        if sys.argv[2] == "-r" and len(sys.argv) == 3:
            recursive_download(all_images,all_links, link=sys.argv[1], pics=p, n_links=l, round=0)
        elif sys.argv[2] == "-p":
            if len(sys.argv) != 4:
                print("No path provided")
            else:
                recursive_download(all_images, all_links, link=sys.argv[1], pics=p, n_links=l, round=0, name=sys.argv[3])
        elif sys.argv[2] == "-r" and sys.argv[3] == "-l":
            if len(sys.argv) != 5:
                print("Maximum depth needed")
            else:
                d = int(sys.argv[4])
                recursive_download(all_images,all_links, link=sys.argv[1], pics=p, n_links=l, depth=d, round=0)

    


    