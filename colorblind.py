#!/usr/bin/python
import numpy as np
from SimpleCV import *
import sys, getopt

#NO OP
NOFX = np.array([[100, 0, 0,      0  ],
                 [0, 100, 0,      0  ], 
                 [0,      0, 100, 0  ], 
                 [0,      0,      0,      100]])


# THESE ARE ALL PURLOINED FROM HERE-- not my doing
# https://github.com/emarc/Chrometric/blob/master/src/com/enably/chrometric/client/Filters.java 
#
# TODO:
# Get rid of scaling and homogenous coordinates
# switch over to HSV... should get rid of saturation
#
# "Protanopia","Present in <b>1% of males</b>.
# A form of dichromatism in which red appears dark."
PROTANOPIA = np.array([[56.667, 43.333, 0,      0  ],
                       [55.833, 44.167, 0,      0  ], 
                       [0,      24.167, 75.833, 0  ], 
                       [0,      0,      0,      100]])

# "Protanomaly","Present in <b>1% of males, 0.01% of females</b>.
# Poor red-green hue discrimination."
PROTANOMALY = np.array([[81.667, 18.333, 0, 0], # r
                        [33.333, 66.667, 0, 0], # g
                        [0, 12.5, 87.5,  0], # b
                        [0, 0, 0, 100        ]])

# "Deuteranopia","Present in <b>1% of males</b>. Moderately
# affects red-green hue discrimination."
DEUTERANOPIA = np.array([[62.5, 37.5, 0, 0], # r
                         [70, 30, 0, 0], # g
                         [0, 30, 70, 0], # b
                         [0, 0, 0, 100]])

# "Deuteranomaly" "Present in <b>6% of males, 0.4% of females</b>.
# By far the most common type, mildly affecting red-green hue discrimination."
DEUTERANOMALY = np.array([[80, 20, 0, 0],
                          [25.833, 74.167, 0, 0],
                          [0, 14.167, 85.833, 0],
                          [0, 0, 0, 100]])

# "Tritanopia","<b>Very rare</b> (less than 1% of males and females).
# Only two cone pigments present and a total absence of blue retinal receptors."
TRITANOPIA = np.array([[95, 5, 0, 0],
                       [0, 43.333, 56.667, 0],
                       [0, 47.5, 52.5, 0],
                       [0, 0, 0, 100]])

# "Tritanomaly","<b>Rare</b> (0.01% for both male and female).
# Affects blue-yellow hue discrimination. Unlike most other forms, it is not sex-linked."
TRITANOMALY = np.array([[96.667, 3.333, 0, 0],
                        [0, 73.333, 26.667, 0],
                        [0, 18.333, 81.667, 0],
                        [0, 0, 0, 100]])

# "Achromatopsia","<b>Exceedingly rare</b>.
# Inability to distinguish any colors."
ACHROMATOPSIA = np.array([[29.9, 58.7, 11.4, 0],
                          [29.9, 58.7, 11.4, 0],
                          [29.9, 58.7, 11.4, 0],
                          [0,0,0,100]])
# "Achromatomaly","<b>Exceedingly rare</b>.
# Lacking most color vision."
ACHROMATOMALY = np.array([[61.8, 32, 6.2, 0],
                          [16.3, 77.5, 6.2, 0],
                          [16.3, 32.0, 51.6, 0],
                          [0, 0, 0, 100]])
def doEffect(img,effect,name):
    # matrix had a bunch of
    # scaling and was homo... fix this
    effect = effect[0:3,0:3]
    effect = effect/100.0
    raw = img.getNumpy().reshape(-1,3)
    out = raw.dot(effect)
    out = out.reshape(img.width,img.height,3)
    out = Image(out)
    out.drawText(name.lower(),10,10,color=Color.RED,fontsize=32)
    return out

def main(argv):
    fx = [NOFX,ACHROMATOMALY,ACHROMATOPSIA,TRITANOMALY,TRITANOPIA,DEUTERANOMALY,PROTANOMALY,PROTANOPIA]
    names = ["No Effect","ACHROMATOMALY","ACHROMATOPSIA","TRITANOMALY","TRITANOPIA","DEUTERANOMALY","PROTANOMALY","PROTANOPIA"]
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
    except getopt.GetoptError:
        print 'colorblind.py -i <inputfile> '
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'colorblind.py -i <inputfile> '
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    print 'Input file is "', inputfile
    img = Image(inputfile)
    stem = inputfile.split('.')[0]
    for effect,name in  zip(fx,names):
        temp = doEffect(img,effect,name)
        fname = "{0}-{1}.png".format(stem,name.lower())
        print "Saving {0}".format(fname)
        temp.save(fname)
       
if __name__ == "__main__":
    main(sys.argv[1:])
