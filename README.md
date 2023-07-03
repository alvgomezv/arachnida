# Arachnida

### Web Scraping and Image Metadata Extraction

This repository contains two programs, `spider` and `scorpion`, that allow you to perform web scraping and extract image metadata. These programs are developed in Python and do not rely on external libraries like wget or scrapy.

## Spider

#### Program Description

The spider program extracts all images from a website recursively. It takes a URL as a parameter and provides various options for customizing the download process. Downloads images with the following extensions by default: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`.

#### Usage

`./spider [-rlp] URL`


#### Options:
- `-r`: Recursively downloads the images in the provided URL.
- `-r -l [N]`: Indicates the maximum depth level of the recursive download. If not specified, the default value is 5.
- `-p [PATH]`: Specifies the path where the downloaded files will be saved. If not specified, the default path is `./data/`.

## Scorpion

#### Program Description

The scorpion program parses image files for EXIF and other metadata, displaying them on the screen. It is compatible with the same image extensions handled by the spider program.

#### Usage

`./scorpion FILE1 [FILE2 ...]`


#### Arguments:
- `FILE1`, `FILE2`, ...: Image files to parse for metadata.

## Instructions

1. Clone this repository to your local machine.
2. Compile and run the `spider` program to extract images from a website and customize the download process using the available options.
3. Use the `scorpion` program to parse image files and display their metadata.

**Note:** Make sure you have Python and the required dependencies installed before running these programs.

Feel free to explore the code and modify it according to your needs. Happy web scraping and metadata extraction!

Please refer to the original source for any further updates or additional information.
