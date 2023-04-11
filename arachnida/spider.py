# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alvgomez <alvgomez@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 13:50:20 by alvgomez          #+#    #+#              #
#    Updated: 2023/04/11 18:39:58 by alvgomez         ###   ########.fr        #
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
        for img in soup.findAll('img', src=True):
            try:
                if img.get('src')[0] == '/' and img.get('src')[1] == '/':
                    images.append('https:'+ img.get('src'))
            except:
                 pass
            else:
                 images.append(img.get('src'))
        return images
    except:
         pass


def get_img_into_folder(images, file="./data", pics=0, round=0):
    if not os.path.exists(file):
        os.makedirs(file)
    i = 0
    for img in images:
        if pics != 0:
            if i >= pics:
                return
        try:
            req = requests.get(img, stream = True)
            if req.status_code == 200:
                src = os.path.join(file, f"pic_{i}_{round}")
                with open(src, 'wb') as f:
                    shutil.copyfileobj(req.raw, f)
                i += 1
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
    
def recursive_download(link, pics, n_links, i=0, depth=5, round=0):
    print(round, depth)
    if round >= (depth):
        print("finished")
    else:
        images = get_img_urls(link)
        file= f"./data{round}_{i}"
        get_img_into_folder(images, file, pics, round)
        print(file)
        links = get_links(link, n_links)
        round += 1
        i = 0
        for link in links:
            recursive_download(link, pics, n_links, i, depth, round)
            i += 1
     
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No url provided")
    if len(sys.argv) == 2:
        url = sys.argv[1]
        images = get_img_urls(url)
        get_img_into_folder(images, pics=2)
    if len(sys.argv) == 3:
        if sys.argv[2] == "-r":
            recursive_download(link=sys.argv[1], pics=2, n_links=2, depth=3, round=0)

    


    