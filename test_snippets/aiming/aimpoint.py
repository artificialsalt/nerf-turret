from matplotlib import pyplot 
from time import time
from array import array

# Open csv file
pixel_data = open('test_image_16ft.csv' ,'r')
#pixel_data = open('test_image_medium.csv','r')

# Everything before this line is opening csv, which is not required for onboard processing
# ----------------------------------------------------------

mask_threshold = 75
width = 32
length = 24
pixels = []

# Iterate through pixel rows
# Everything between the below two lines involves csv, which is not required for onboard processing
# The real iteration would take place in a for loop (for line in camera.get_csv....)
# ----------------------------------------------------------

while True:

    # Read the next row of pixels
    pixel_row = pixel_data.readline()

    # Exit while loop if end of file reached
    if pixel_row == "":
        break
# ----------------------------------------------------------
    # Eliminate newlines
    pixel_row = pixel_row.rstrip('\n')
    # Append into list of rows
    pixels.append(pixel_row)

start_time = time()

# Convert array of strings into one long list of integers
pixels = ','.join(pixels)
pixels = pixels.split(',')
pixels = [int(val) for val in pixels]
pixels_original = [val for val in pixels]



# Mask the pixels, discard the edges which are susceptible to noise
for pixel in range(length*width):
    if pixels[pixel] > mask_threshold and pixel % width > 5 and pixel % width < 26:
        pixels[pixel] = 1
    else:
        pixels[pixel] = 0


discard_outliers = True
if discard_outliers:
    # Discard outlier pixels
    for pixel in range(length*width):
        if pixels[pixel] == 1:
            neighbors = []
            try:
                nb1 = pixels[pixel-width-1]
                neighbors.append(nb1)
            except IndexError:
                pass
            try:
                nb2 = pixels[pixel-width]
                neighbors.append(nb2)
            except IndexError:
                pass
            try:
                nb3 = pixels[pixel-width+1]
                neighbors.append(nb3)
            except IndexError:
                pass
            try:
                nb4 = pixels[pixel-1]
                neighbors.append(nb4)
            except IndexError:
                pass
            try:
                nb6 = pixels[pixel+1]
                neighbors.append(nb6)
            except IndexError:
                pass
            try:
                nb7 = pixels[pixel+width-1]
                neighbors.append(nb7)
            except IndexError:
                pass
            try:
                nb8 = pixels[pixel+width]
                neighbors.append(nb8)
            except IndexError:
                pass
            try:
                nb9 = pixels[pixel+width+1]
                neighbors.append(nb9)
            except IndexError:
                pass
            if 1 not in neighbors:
                pixels[pixel] = 0

# Compute center of mass (aimpoint)
# Y coordinate
mask_sum_y = 0
wtd_sum_y = 0
for row in range(length):
    mask_sum = sum(pixels[row*width : (row+1)*width-1])
    mask_sum_y += mask_sum
    wtd_sum_y += mask_sum * (row + 0.5)
try:
    com_y = wtd_sum_y / mask_sum_y
except ZeroDivisionError:
    exit

# X coordinate
mask_sum_x = 0
wtd_sum_x = 0
for col in range(width):
    mask_sum = 0
    for row in range(length):
        mask_sum += pixels[row * width + col]
    mask_sum_x += mask_sum 
    wtd_sum_x += mask_sum * (col + 0.5)
try:
    com_x = wtd_sum_x / mask_sum_x
except ZeroDivisionError:
    exit


# Insert coordinates->degree->setpoint conversion here

# Everything after this line is to demonstrate what the image would look like and where the turret would target
# ---------------------------------------------------------------------
try:
    print(f'COM: {com_x}, {com_y}')
    # Camera FOV characteristics
    x_fov = 55
    y_fov = 35

    # Defining the range of degrees from center
    x_min = -(x_fov/2)
    x_max = (x_fov/2)
    y_min = -(y_fov/2)
    y_max = (y_fov/2)

    # Mapping the COM to the FOV
    x_adj = (com_x) * (x_max - x_min) / (width) + x_min
    y_adj = (com_y) * (y_max - y_min) / (length) + y_min
    print(f'Turret adjustent: x: {x_adj} degrees, y: {y_adj} degrees')
except:
    pass
#print(f'Evaluation time: {end_time - start_time} seconds')

# Everything between these two lines is matlab plotting, not necessary for targeting
# -------------------------------------------------------------
pixels_org2d = []
for row in range(length):
    pixels_org2d.append(pixels_original[row*width : (row+1) * width-1])
pixels_2d = []
for row in range(length):
    pixels_2d.append(pixels[row*width : (row+1) * width-1])

fig, plts = pyplot.subplots(2)
plts[0] = pyplot.pcolor(pixels_org2d, cmap='Greys_r')
plts[1] = pyplot.pcolor(pixels_2d, cmap='Greys_r')
#pyplot.plot(com_x, com_y, 'or')
pyplot.show()
# -------------------------------------------------------------