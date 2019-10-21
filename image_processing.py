from PIL import Image
import xml.etree.ElementTree as ET
import re
import globals
from math import *
import numpy
import operator

def convert_image(filename):
    formula = 1

    globals.image_total_beads = 0
    globals.image_total_colors = 0
    for i in range(globals.MAX_CONTAINERS):
        globals.bucket_array[i].bucket_total_beads = 0
    # copy rgb values and close image
    globals.perler_image = Image.open(filename)
    globals.perler_image = globals.perler_image.transpose(Image.FLIP_LEFT_RIGHT)
    print("unmodified size: " + str(globals.perler_image.size))
    #globals.perler_image = globals.perler_image.convert('RGB')
    # create perler images
    globals.perler_image_width = globals.perler_image.width
    globals.perler_image_height = globals.perler_image.height


    edges = tuple(add_bg_find_edges())
    globals.perler_image = globals.perler_image.crop(edges)
    globals.perler_image_height = int(globals.perler_image.height / globals.IMAGE_MULTIPLIER)
    globals.perler_image_width = int(globals.perler_image.width / globals.IMAGE_MULTIPLIER)


    #figure out how many panals
    globals.image_bucket_matrix = [[0 for i in range(globals.perler_image_width)] for j in range(globals.perler_image_height)]
    for y in range(globals.perler_image_height):
        for x in range(globals.perler_image_width):
            #temp_image_matrix[x][y] = '#%02x%02x%02x' % im.getpixel((globals.IMAGE_MULTIPLIER * x, globals.IMAGE_MULTIPLIER * y))
            curr = globals.perler_image.getpixel((x, y))
            if (curr == (0,255,0,255)):
                globals.image_bucket_matrix[y][x] = globals.clear_bucket
            else:
                deltas = []
                for color in range(len(globals.bucket_array)):
                    if globals.check_box_values[color].get() == 1:
                        continue #bucket not used
                    if globals.bucket_array[color].bucket_rgb_matrix == [0,255,0]:
                        continue
                    rr = globals.bucket_array[color].bucket_rgb_matrix[0] - curr[0]
                    rg = globals.bucket_array[color].bucket_rgb_matrix[1] - curr[1]
                    rb = globals.bucket_array[color].bucket_rgb_matrix[2] - curr[2]
                    rr_mean = (globals.bucket_array[color].bucket_rgb_matrix[0] + curr[0])/2
                    if formula == 0:
                        deltas.append((color,sqrt((rr ** 2) + (rg ** 2) + (rb ** 2))))
                    if formula == 1:
                        deltas.append((color,sqrt((2+(rr_mean/256)) * (rr ** 2) + 4 * (rg ** 2) + (2+(255-rr_mean)/256) * (rb ** 2))))
                deltas = sorted(deltas, key=operator.itemgetter(1))
                globals.image_bucket_matrix[y][x] = globals.bucket_array[deltas[0][0]].bucket_num
                #add to totals and counts
                if globals.image_bucket_matrix[y][x] != globals.clear_bucket:
                    globals.image_total_beads += 1
                    globals.bucket_array[deltas[0][0]].bucket_total_beads += 1
                globals.perler_image.putpixel((x, y), globals.bucket_array[deltas[0][0]].bucket_rgb)

    #get total colors
    for i in range(len(globals.bucket_array)):
        if globals.bucket_array[i].bucket_total_beads > 0:
            globals.image_total_colors += 1
    poop = globals.image_bucket_matrix
    numpy.set_printoptions(suppress=True)
    print("total beads : " + str(globals.image_total_beads))
    print("estimated time : " + str(int(globals.image_total_beads*5)/60) + " minutes")
    print("total colors : " + str(globals.image_total_colors))
    print("size: (" + str(globals.perler_image_width) + "," + str(globals.perler_image_height) + ")")
def add_bg_find_edges():
    x_edge = globals.perler_image_width
    y_edge = globals.perler_image_height
    test = globals.perler_image.getpixel((0, 0))

    if test == 0:
        t = 4
    else:
        t = len(test)
    clear_bucket_color = (0,255,0,255)
    edge_array = [0,0,x_edge,y_edge]
    temp_color_matrix = [[0 for i in range(y_edge)] for j in range(x_edge)]
    for x in range(x_edge):
        for y in range (y_edge):
            temp_color_matrix[x][y] = globals.perler_image.getpixel((x, y))
            if t == 3: #add on alpha
                temp_color_matrix[x][y] = temp_color_matrix[x][y] + (255,)
            else:
                if temp_color_matrix[x][y][3] == 0:
                    temp_color_matrix[x][y] = clear_bucket_color
                    globals.perler_image.putpixel((x,y),clear_bucket_color)
    # find start of x
    found = False
    for x in range(x_edge):
        if found:
            break
        for y in range(y_edge):
            if temp_color_matrix[x][y] != clear_bucket_color:
                edge_array[0] = x
                found = True
                break
    # find end of x
    found = False
    for x in range(x_edge-1,0,-1):
        if found:
            break
        for y in range(y_edge):
            if temp_color_matrix[x][y] != clear_bucket_color:
                test = temp_color_matrix[x][y]
                edge_array[2] = x+1
                found = True
                break
    # find start of y
    found = False
    for y in range(y_edge):
        if found:
            break
        for x in range(x_edge):
            if temp_color_matrix[x][y] != clear_bucket_color:
                edge_array[1] = y
                found = True
                break
    # find end of y
    found = False
    for y in range(y_edge-1,0,-1):
        if found:
            break
        for x in range(x_edge):
            if temp_color_matrix[x][y] != clear_bucket_color:
                edge_array[3] = y+1
                found = True
                break
    print("edge array = " + str(edge_array))
    return edge_array
def find_edges(startx,starty,endx,endy):
    # find start of x

    edge_array = [startx,starty,endx,endy]

    found = False
    for x in range(startx, endx):
        if found:
            break
        for y in range(starty,endy):
            if globals.image_bucket_matrix[y][x] != globals.clear_bucket:
                edge_array[0] = x
                found = True
                break

    # find end of x
    found = False
    for x in range(endx-1,startx,-1):
        if found:
            break
        for y in range(starty,endy):
            if globals.image_bucket_matrix[y][x] != globals.clear_bucket:
                edge_array[2] = x+1
                found = True
                break

    # find start of y
    found = False
    for y in range(starty, endy):
        if found:
            break
        for x in range(startx, endx):
            if globals.image_bucket_matrix[y][x] != globals.clear_bucket:
                edge_array[1] = y
                found = True
                break

    # find end of y
    found = False
    for y in range(endy - 1, starty, -1):
        if found:
            break
        for x in range(startx, endx):
            if globals.image_bucket_matrix[y][x] != globals.clear_bucket:
                edge_array[3] = y + 1
                found = True
                break

    return edge_array