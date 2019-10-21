import globals
import os
import numpy
import math

# generate g code for image panel at specific layer
# image panel is 29x29
from math import *
import random

def delay(milliseconds):
    if milliseconds >= 1000:
        new_line("G4 S" + str(milliseconds/1000))
    else:
        new_line("G4 P" + str(milliseconds))
def home_sorter():
    # home sorter
    #pull back pusher motor first

    home_pusher()
    delay(300)
    new_line("G205 P1 S0 E0 F550")
    delay(50)
    globals.motor_steps[1] = 0
def home_pusher():
    new_line("G205 P0 S0 E0 F" + str(globals.m1_SPEED))
    globals.motor_steps[0] = 0
#Move end effector to just above first bead pos and make that 0,0 position
def home_end_effector():
    #now at z=400 pos
    new_line("G90")
    new_line("G28 X Y Z")
    globals.end_effector_xyz = [0,0,400]
    new_line("G91") #now back to relative

def zero_end_effector():

    new_line("G227")


def push(speed):
    #new_line("; PUSH")

    move(0,globals.M0_PUSH_LENGTH,speed)
    #delay(50)

def pushback():
    #globals.pickups_since_homed_pusher += 1
    #if globals.pickups_since_homed_pusher >= globals.BEADPICKUPBEFOREHOME_PUSHER:
    #    home_pusher()
    #    globals.pickups_since_homed_pusher = 0
    move(0,180,900)

def vibrate_sorter(turnon):
    if (turnon):
        new_line("M106 P2 S90 I0") # to get around firmware going to 255 initially
    else:
        new_line("M106 P2 S0 I0")
def move(motor_num,step,speed = -999,temp_delay = 50):
    step_int = round(step)
    globals.motor_steps[motor_num] = step
    if speed != -999:
        new_line("G201 P" + str(motor_num) + " X" + str(step_int) + " F" + str(speed))
    else:
        new_line("G201 P" + str(motor_num) + " X" + str(step_int))
    if temp_delay > 0:
        delay(temp_delay)
def open_file(filename = "test"):
    if os.path.exists(globals.PERLER_PATH + "3. G-code Converter/" + str(filename) + ".nc"):
        os.remove(globals.PERLER_PATH + "3. G-code Converter/" + str(filename) + ".nc")
    globals.file = open(globals.PERLER_PATH + "3. G-code Converter/" + str(filename) + ".nc","w")


def disable():
    new_line("G204 P0 S0; disable")
    new_line("G204 P1 S0; disable")

def findColor(bucket):
    for i in range(len(globals.bucket_array)):
        if globals.bucket_array[i].bucket_num == bucket:
            return globals.bucket_array[i].bucket_color_name



def generate_g_code(filename,yoff,startX, startY,endX,endY):
    open_file(filename)

    home_sorter()
    home_end_effector()

    #to make all ranges inclusive to last value
    endX += 1
    endY += 1

    y_size = endY - startY
    x_size = endX - startX

    offset_y = int(y_size/2)
    offset_x = int(x_size/2)
    bucket_count = [0]*64
    #globals.end_effector_xyz = [globals.BEAD_SPACE*x_size/2,globals.BEAD_SPACE*y_size/2,globals.end_effector_xyz[2]]
    # for loop start here for each bead
    slow_start = False

    stop_height = globals.CORNER_BEAD_XYZ[2] + 10
    if globals.end_effector_xyz[2] > stop_height:
        #move_end_effector(-999, -999, stop_height, 4000)
        move_end_effector(110, -40, stop_height, 4000)
        delay(200)
    new_line("G223")
    new_line("G298")
    for y in range(startY+yoff,endY):

        #STORAGE MOVE SECTION
        buckets_in_row = 0
        first_x_index = -1
        for x in range(startX, endX): #figure out if you need to move storage at beginning
            bucket = globals.image_bucket_matrix[y][x]
            if bucket == globals.clear_bucket: #skip clear ones
                continue;
            if first_x_index == -1:
                first_x_index = x - startX
            buckets_in_row += 1
            bucket_count[bucket] += 1
        if first_x_index == -1: #no beads in this row
            continue
        for bucket_number in bucket_count:
            if bucket_number >= 14: #dropped X of the same bucket
                if buckets_in_row > 22:
                    shake_storage(1)
                    bucket_count = [0] * 64
                elif buckets_in_row > 8:
                    shake_storage(0)
                    bucket_count = [0] * 64

        # GET INTO CORRECT X,Y LOCATION

        # move to correct z spot first
        move_end_effector(-999, -999, globals.end_effector_xyz[2] + 3
                          , 4000)
        # move to correct x spot
        x_pos = globals.BEAD_SPACE*(first_x_index-offset_x)
        move_end_effector(x_pos, -999, -999, 4000)
        # move to correct y spot (for new row)
        y_pos = globals.BEAD_SPACE *(y-startY-offset_y)
        move_end_effector(-999, y_pos, -999, 4000)

        #finally zero it for each new row
        zero_end_effector()
        delay(200)
        distance_since_homed = 0
        # PICKUP SECTION
        for x in range(startX,endX):
            bucket = globals.image_bucket_matrix[y][x]
            if bucket == globals.clear_bucket: #skip clear ones
                continue;
            pickup(bucket)
        # PLACE SECTION
        for x in range(startX, endX):
            bucket = globals.image_bucket_matrix[y][x]
            if bucket == globals.clear_bucket: #skip clear ones
                continue;
            currentX = globals.end_effector_xyz[0]
            newX = globals.BEAD_SPACE*(x-startX-offset_x)

            distance_since_homed += math.fabs(newX - currentX)
            move_end_effector(-999, -999, globals.end_effector_xyz[2] + 4,3000)#.05*distance, 2000)
            move_end_effector(newX, -999, -999, 2000)
            if(distance_since_homed > 30):
                zero_end_effector()
                distance_since_homed = 0
            else:
                move_end_effector(-999, -999, globals.end_effector_xyz[2] - 4, 2000)  # .05*distance, 2000)




            # if distance_since_homed > 20:
            #     move_end_effector(-999,-999, globals.end_effector_xyz[2]+3, 2000)
            #     move_end_effector(newX,-999, -999, 2000)
            #     zero_end_effector()
            #     distance_since_homed = 0
            # else:
            #     move_end_effector(newX, -999, -999, 2000)
            place_and_push()
            if slow_start:
                new_line("; GO SLOW")
                delay(5000)

            slow_start = False
        #do a manuver to dump extra bead
        move_end_effector(-999, -999, globals.end_effector_xyz[2] + 3
                          , 4000)
        move_end_effector(globals.end_effector_xyz[0]+10, -999, -999, 2000)
        place_and_push()
    home_end_effector()
    fuse()
    globals.file.close()
    print("GCODE DONE!!!")
    return

def place_and_push():
    delay(150)
    new_line("G226")
    delay(1500)

def fuse():
    fuse_temp = 145
    new_line("M190 S" + str(fuse_temp))
    new_line("M190 S0")
def shake_storage(mode):
    if mode == 0:
        new_line("G225")
    elif mode == 1:
        new_line("G224")
def pickup(bucket):
    #bucket starts at index 1, goes to 68

    globals.pickups_since_homed += 1
    if globals.pickups_since_homed > globals.BEADPICKUPBEFOREHOME:
        globals.pickups_since_homed = 0
        delay(100)
        home_sorter()
    offset = 0
    for i in range(len(globals.M1_BUCKET_OFFSET)):
        if bucket >= globals.M1_BUCKET_OFFSET[i][0] and bucket < globals.M1_BUCKET_OFFSET[i+1][0]:
            offset = globals.M1_BUCKET_OFFSET[i][1]
    m1_new_step = offset + bucket*5.294*globals.STEPS_PER_ANGLE
    move(1,m1_new_step,globals.m1_SPEED)
    delay(100)
    push(900)
    #move(0, globals.M0_PUSH_LENGTH-200, 900)
    new_line("G303")
    pushback()

def move_end_effector(x_pos, y_pos, z_pos, speed = 4000, record = True):
    move = [0,0,0]
    if x_pos != -999:
        move[0] = round(x_pos - globals.end_effector_xyz[0],3)
    if y_pos != -999:
        move[1] = round(y_pos - globals.end_effector_xyz[1],3)
    if z_pos != -999:
        move[2] = round(z_pos - globals.end_effector_xyz[2],3)
    abs_pos = [globals.end_effector_xyz[0]+move[0], globals.end_effector_xyz[1]+move[1], globals.end_effector_xyz[2]+move[2]]
    new_line("G1 X" + str(move[0]) + " Y" + str(move[1]) + " Z" + str(move[2]) + " F" + str(speed) + " ; ABSOLUTE = " + str(abs_pos))
    #delay(5*numpy.amax(numpy.absolute(move)))
    if record:
        globals.end_effector_xyz = [globals.end_effector_xyz[0]+move[0], globals.end_effector_xyz[1]+move[1], globals.end_effector_xyz[2]+move[2]]
    return

def generate_debug_patterns():


    open_file()


    NUM = 4
    for i in range(5):
        if i == 3:
            i=0;
    if NUM == 0:
        home_sorter()
        count = 0
        for i in range(3):
            for i in range(16,24):
                pickup(i)
            for i in range(16,24):
                pickup(i)
            for i in range(48,62):
                pickup(i)
        disable()

    if NUM == 1:
        home_sorter()
        pickup(10)

    if NUM == 2: #test all color drop
        home_sorter()
        home_end_effector()
        start_location = [-15,-15] #x,y
        bucket_index = 0
        grid_matrix = []
        count = 0
        pic_size = [20,20] #6 horizonal, 6 vertical
        for y in range(pic_size[1]):
            for x in range(pic_size[0]):
                count += 1
                if count == 4:
                    bucket_index += 1
                    count = 0
                if bucket_index == 64:
                    disable()
                    return
    if NUM == 3:
        home_end_effector()
        stop_height = globals.CORNER_BEAD_XYZ[2] + 6
        if globals.end_effector_xyz[2] > stop_height:
            move_end_effector(-999, -999, stop_height, 4000)
            zero_end_effector()
    if NUM == 4:

        home_sorter()
        for i in range(20):
            pickup(46)
    return
def new_line(line,addN = False):
    if addN:
        globals.N += 1
        line2 = "N" + str(globals.N) + " " + line + "\n"
    else:
        line2 = line + "\n"
    globals.file.write(line2)