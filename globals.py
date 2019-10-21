

DEBUG = 0
#array of bead_class
beads = []

check_box_values = [0]*64
bucket_array = []
clear_bucket = 21
big_perler_image = []
perler_image = []
perler_image_width = 0
perler_image_height = 0

image_bucket_matrix = []
image_total_beads = 0
image_total_colors = 0

MAX_PANAL_SIZE = 43

IMAGE_MULTIPLIER = 1
MAX_CONTAINERS = 64
MAX_BEADS_PER_CONTAINER = 1000

PERLER_PATH = "C:/Users/kevin/Dropbox/BeadSpriteMachine/"
#PERLER_PATH = "F:/Dropbox/BeadSpriteMachine/"

#realtime angles of M0 and M1
motor_steps = [0, 0]
end_effector_xyz = [0,0,0]
homed = False

STEPS_PER_ANGLE = 1/.45


additional = 0


#offset from 0 degrees to endstop pos (higher is more cc)
M1_BUCKET_OFFSET = [[0,0],[7,0],[24,2],[41,1],[65,0]] #ex. 23 > buckets >= 0 offset = 1
M0_PUSH_LENGTH = 425


AUTOZERO_FREQUENCY = 5



pickups_since_homed = 0
BEADPICKUPBEFOREHOME = 25
pickups_since_homed_pusher = 0
BEADPICKUPBEFOREHOME_PUSHER = 9999
m1_SPEED = 600
#offset from last bead
offset_place_y = 1.5
offset_place_x = 1.5
#offset between tube and aligner piece
offset_machine_y = 10
offset_machine_x = 6.5

#used to move printer from home to directly on first bead
CORNER_BEAD_XYZ = (-150, -150, 83.5)

#POSTIVE = MORE RIGHT AND UP
BEADS_PER_SKEW = 2
SKEW_X = -.1
SKEW_Y = .05

SKEW_X2 = -.3

BEAD_SPACE = 5.05
N = 0
file = 0
