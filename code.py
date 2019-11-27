from adafruit_pybadger import PyBadger
import time
#from machine import I2C, Pin
import board
#import busio
import displayio
import terminalio
from adafruit_display_text import label
from scd30 import SCD30
import audioio
import adafruit_bme280

def plot_data(data):
    # Set up plotting window
    bottom_margin = 15 #pixels on the bottom edge
    top_margin = 15 #pixels on the top edge
    y_height = display.height-bottom_margin-top_margin

    data_max = max(data)
    data_min = min(data)
    if ((data_max-data_min)==0):
        data_max = data_max+1
    # Create a bitmap with two colors
    bitmap = displayio.Bitmap(display.width, display.height, 2)

    # Create a two color palette
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xffffff

    # Create a TileGrid using the Bitmap and Palette
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

    # Create a Group
    group = displayio.Group()

    # Add the TileGrid to the Group
    group.append(tile_grid)

    # Add the Group to the Display
    display.show(group)

    for i in range(0, len(data)):
        y = y_height-round((data[i]-data_min)/(data_max-data_min) * y_height)
        #print("max: {} min: {} y: {}".format(data_max, data_min, y))
        bitmap[i,y+top_margin] = 1

    # Set text, font, and color
    font = terminalio.FONT

    # Create the tet label
    current_val_text = label.Label(font, text="{} ppmCO2".format(round(data[-1])), color=0x00FF00)

    # Set the location
    (_, _, width, height) = current_val_text.bounding_box
    current_val_text.x = display.width - width
    current_val_text.y = height//2

    min_val_text = label.Label(font, text="{} ppmCO2".format(round(data_min)), color=0xFFFFFF)
    (_, _, width, height) = min_val_text.bounding_box
    min_val_text.x = 0
    min_val_text.y = display.height-(height//2)

    max_val_text = label.Label(font, text="{} ppmCO2".format(round(data_max)), color=0xFFFFFF)
    (_, _, width, height) = max_val_text.bounding_box
    max_val_text.x = 0
    max_val_text.y = height//2

    # Show it
    #display.show(text_area)
    group.append(current_val_text)
    group.append(min_val_text)
    group.append(max_val_text)

pybadger = PyBadger()
display = pybadger.display

pybadger.auto_dim_display(delay=10, movement_threshold=20)

i2c = board.I2C()
scd30 = SCD30(i2c, 0x61)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

state = 3
state_changed = True

# Accumulate data from sensor
data = []

while True:
    if pybadger.button.start:
        state = 0
        state_changed = True
    elif pybadger.button.a:
        state = 1
        state_changed = True
    elif pybadger.button.b:
        state = 2
        state_changed = True
    elif pybadger.button.down:
        state = 3
        state_changed = True

    if (state==0 and state_changed):
        # Wait for sensor data to be ready to read (by default every 2 seconds)
        try:
            while scd30.get_status_ready() != 1:
                time.sleep(0.200)
        except SCD30.CRCException:
            print("CRC Exception in get_status_ready")
        print("getting measurement")
        #print(scd30.get_firmware_version())
        try:
            co2, temp, relh = scd30.read_measurement()
        except SCD30.CRCException:
            print("CRCException")
        print("({}, {}, {})".format(co2, temp, relh))
        pybadger.show_badge(name_string="{:.0f} ppmCO2".format(co2), hello_scale=2, my_name_is_scale=2, name_scale=2)
    elif (state==1 and state_changed):
        state_changed = False
        pybadger.show_business_card(image_name="supercon.bmp", name_string="Changeme in code.py", name_scale=1,
                                    email_string_one="alex@alexw.io",
                                    email_string_two="https://alexwhittemore.com/")
    elif (state==2 and state_changed):
        state_changed = False
        pybadger.show_qr_code(data="https://alexwhittemore.com/")
        pybadger.play_file("square_root_2_20k.wav")
    elif (state==3 and state_changed):
        # pybadger.display.height is 128
        # pybadger.display.width is 160
        #state_changed = False

        try:
            # Starts a continuous measurement with the (integer) ambient pressure in milibar as an argument for correction.
            scd30.start_continous_measurement(round(bme280.pressure))
            #scd30.start_continous_measurement()
            while scd30.get_status_ready() != 1:
                time.sleep(0.200)
        except SCD30.CRCException:
            print("CRC Exception in get_status_ready")
        try:
            co2, temp, relh = scd30.read_measurement()
        except SCD30.CRCException:
            print("CRCException")

        if len(data)==display.width:
            data.pop(0)

        try:
            data.append(round(co2))
            plot_data(data)
        except ValueError:
            pass