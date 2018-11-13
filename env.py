#! /usr/bin/env python

from Adafruit_CCS811 import Adafruit_CCS811
import epd2in9
import time
import Image
import ImageDraw
import ImageFont

ccs =  Adafruit_CCS811()
while not ccs.available():
	pass

def main():
	epd = epd2in9.EPD()
	epd.init(epd.lut_full_update)

	image = Image.new('1', (epd2in9.EPD_WIDTH, epd2in9.EPD_HEIGHT), 255)  # 255: clear the frame
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype('/home/pi/demo/raspberrypi/python/open-sans.ttf', 16)
	draw.rectangle((0, 10, 128, 34), fill = 0)
	draw.text((8, 12), 'Air Quality Tracker', font = font, fill = 255)
	draw.text((8, 36), 'loading...', font = font, fill = 0)
	
	#draw.line((16, 60, 56, 60), fill = 0)
	#draw.line((56, 60, 56, 110), fill = 0)
	#draw.line((16, 110, 56, 110), fill = 0)
	#draw.line((16, 110, 16, 60), fill = 0)
	#draw.line((16, 60, 56, 110), fill = 0)
	#draw.line((56, 60, 16, 110), fill = 0)
	#draw.arc((60, 90, 120, 150), 0, 360, fill = 0)
	#draw.rectangle((16, 130, 56, 180), fill = 0)
	#draw.chord((60, 160, 120, 220), 0, 360, fill = 0)

	epd.clear_frame_memory(0xFF)
	epd.set_frame_memory(image, 0, 0)
	epd.display_frame()

	epd.delay_ms(1000)

	##
	# there are 2 memory areas embedded in the e-paper display
	# and once the display is refreshed, the memory area will be auto-toggled,
	# i.e. the next action of SetFrameMemory will set the other memory area
	# therefore you have to set the frame memory twice.
	##
	epd.clear_frame_memory(0xFF)
	epd.display_frame()
	epd.clear_frame_memory(0xFF)
	epd.display_frame()

	# for partial update
	epd.init(epd.lut_partial_update)
	##
	# there are 2 memory areas embedded in the e-paper display
	# and once the display is refreshed, the memory area will be auto-toggled,
	# i.e. the next action of SetFrameMemory will set the other memory area
	# therefore you have to set the frame memory twice.
	##
	epd.set_frame_memory(image, 0, 0)
	epd.display_frame()
	epd.set_frame_memory(image, 0, 0)
	epd.display_frame()

	time_image = Image.new('1', (epd2in9.EPD_WIDTH, epd2in9.EPD_HEIGHT), 255)  # 255: clear the frame
	draw = ImageDraw.Draw(time_image)
	font = ImageFont.truetype('/home/pi/demo/raspberrypi/python/open-sans.ttf', 12)
	image_width, image_height = time_image.size
	while (True):
		
		if ccs.available():
			temp = ccs.calculateTemperature()
			if not ccs.readData():
				print "CO2: ", ccs.geteCO2(), "ppm, TVOC: ", ccs.getTVOC(), " temp: ", temp
				draw.rectangle((0, 0, image_width, image_height), fill = 0)
				draw.text((5, 0), time.strftime('Time: %H:%M:%S'), font = font, fill = 255)
				draw.text((5, 20), 'CO2: %sppm'%(ccs.geteCO2()), font = font, fill = 255)
				draw.text((5, 40), 'Gas/Particulate: %s'%(ccs.getTVOC()), font = font, fill = 255)
				draw.text((5, 60), 'Temperature: %s'%(temp), font = font, fill = 255)
				epd.set_frame_memory(time_image, 0, 10)
				epd.display_frame()
			else:
				print "ERROR!"
				while(1):
					pass
					sleep(2)

	



   

if __name__ == '__main__':
    main()
