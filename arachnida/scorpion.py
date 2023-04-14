# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alvgomez <alvgomez@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/14 19:24:36 by alvgomez          #+#    #+#              #
#    Updated: 2023/04/14 19:38:57 by alvgomez         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import exifread

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No file provided")
    elif len(sys.argv) > 1:
        with open(sys.argv[1], 'rb') as f:
            tags = exifread.process_file(f)
            print(tags)
            