class Bucket:

    #public variables
    bucket_x = 0
    bucket_y = 0
    bucket_num = 0
    bucket_color_code = 0
    bucket_color_name = ""
    bucket_rgb_matrix = [0,0,0]
    bucket_rgb = ()
    bucket_hex_color = ""
    bucket_total_beads = 0
    bucket_available = 1
    def __init__(self,bucket_x,bucket_y,bucket_num,bucket_color_code,bucket_color_name,r,g,b,bucket_available):
        self.bucket_x = bucket_x
        self.bucket_y = bucket_y
        self.bucket_num = bucket_num
        self.bucket_color_code = bucket_color_code
        self.bucket_color_name = bucket_color_name
        self.bucket_rgb_matrix = [r,g,b]
        self.bucket_rgb = (r,g,b)
        self.bucket_hex_color = '#%02x%02x%02x' % self.bucket_rgb
        self.bucket_available = bucket_available
