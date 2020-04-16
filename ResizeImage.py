import cv2
import sys
import os
import json
from PIL import Image
#pip3 install opencv-python
#python3 ResizeImage.py img.png

dimArr = [[(20, 20), 2, 'iphone'],
          [(20, 20), 3, 'iphone'],
          [(29, 29), 1, 'iphone'],
          [(29, 29), 2, 'iphone'],
          [(29, 29), 3, 'iphone'],
          [(40, 40), 2, 'iphone'],
          [(40, 40), 3, 'iphone'],
          [(60, 60), 2, 'iphone'],
          [(60, 60), 3, 'iphone'],
          [(76, 76), 2, 'iphone'],
          [(20, 20), 1, 'ipad'],
          [(20, 20), 2, 'ipad'],
          [(29, 29), 1, 'ipad'],
          [(29, 29), 2, 'ipad'],
          [(40, 40), 1, 'ipad'],
          [(40, 40), 2, 'ipad'],
          [(76, 76), 1, 'ipad'],
          [(76, 76), 2, 'ipad'],
          [(83.5, 83.5), 2, 'ipad'],
          [(1024, 1024), 1, 'ios-marketing']
          ]
def addProfile(image, icc_profile):
    im = Image.open(image)
    im.save(image, "png", icc_profile=icc_profile)
    print('icc_profile', icc_profile)
def make_app_icon(img_path):
    cwd = os.getcwd()
    iconDir = cwd + '/AppIcon.appiconset'
    if not os.path.exists(iconDir):
        os.mkdir(iconDir)
        print('iconDir', iconDir)
    # addProfile(img_path)
    print('cwd', cwd)
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    im = Image.open(img_path)
    icc_profile = im.info.get("icc_profile")
    print('Original Dimensions : ', img.shape)
    jsonContent = {}
    images = []
    for image in dimArr:
        dim = (int(image[0][0] * image[1]), int(image[0][1] * image[1]))
        print('dim', dim)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        imgObj = {}
        size = str(image[0][0]) + 'x' + str(image[0][1])
        scale = str(image[1]) + 'x'
        filename = 'Icon-App-' + size + '@' + scale + '.png'
        imgObj['size'] = size
        imgObj['idiom'] = image[2]
        imgObj['scale'] = scale
        imgObj['filename'] = filename
        status = cv2.imwrite(iconDir + '/' + filename, resized)
        addProfile(iconDir + '/' + filename, icc_profile)
        print('Resized Dimensions : ', resized.shape)
        print('filename', filename)
        images.append(imgObj)
    jsonContent['images'] = images
    info = {}
    info['version'] = '1'
    info['author'] = 'xcode'
    jsonContent['info'] = info

    with open(iconDir + '/Contents.json', 'w') as f:
        json.dump(jsonContent, f, indent=4)
if __name__ == "__main__":
    make_app_icon(sys.argv[1])

