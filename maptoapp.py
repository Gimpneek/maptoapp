#!/usr/bin/env python
#Use a KML document to create a iOS friendly map

#IMPORTS
import os
import subprocess
from pykml import parser
from pykml.parser import Schema
from pykml.factory import nsmap
from lxml import etree
import imghdr
import stat
import sys
from PIL import Image


#SETUP

#VARIABLES
#schema variables for validating KML against
gxns = '{' + nsmap['gx'] + '}'
kmlns = '{'+nsmap[None]+ '}'
schema_ogc = Schema("ogckml22.xsd")
schema_gx = Schema("kml22gx.xsd")
kmlFile = ""
imageFile = ""
outputDir = ""
imageWidth = 0
imageHeight = 0

#FUNCTIONS
#checks to see if the user can write to the directory they wish to write the output file to
def isWritable(directory):
    try:
        tmp_prefix = "write_tester";
        count = 0
        filename = os.path.join(directory, tmp_prefix)
        while(os.path.exists(filename)):
            filename = "{}.{}".format(os.path.join(directory, tmp_prefix),count)
            count = count + 1
        f = open(filename,"w")
        f.close()
        os.remove(filename)
        return True
    except Exception as e:
        #print "{}".format(e)
        return False

#check if the KML is a valid document
def checkKML(filename):
	with open(filename) as f:
		doc = parser.parse(f)
		if schema_ogc.validate(doc) or schema_gx.validate(doc):
			return True
		else:
			return False

#check if the image is in PNG format
def checkImage(filename):
	if imghdr.what(filename) == "png":
		return True
	else:
		return False

def getKMLCoords(filename):
	with open(filename) as f:
		doc = parser.parse(f).getroot()
		gll = doc.GroundOverlay[gxns+"LatLonQuad"][kmlns+'coordinates']
		coordText = gll.text
		lonLats = {}
		coordSets = coordText.split(" ")
		for i in range(4):
			coordValues = coordSets[i].strip().split(',')
			coordVals = {}
			for x in range(len(coordValues)):
				if x == 0:
					coordVals['longitude'] = coordValues[x]
				if x == 1:
					coordVals['latitude'] = coordValues[x]
			lonLats[i] = coordVals
		return lonLats

def getImageCoords(filename):
	im = Image.open(filename)
	return im.size

#MAIN SCRIPT
#ask the input KML document
kmlFile = (raw_input("Please drag the KML file into terminal and press enter: ")).strip()

#verify input
if checkKML(kmlFile):

	#ask for the image file to apply to this
	imageFile = (raw_input("Please drag the image file (png) into terminal and press enter: ")).strip()

	#verify image
	if checkImage(imageFile):

		#ask for the output directory
		outputDir = (raw_input("Where should the output go (drag folder into terminal): ")).strip()
		if os.path.exists(outputDir):
			if isWritable(outputDir):
				print "Would go and do the business"
			else:
				print "Your account doesn't have the correct privelages to create a file here"
				sys.exit()
		else:
			print "Would create folder and go and do the business"
			try:
				os.makedirs(outputDir)
			except:
				print "Your account doesn't have the correct privelages to create the directory you specified"
				sys.exit()

		#use pykml to get the coordinates
		KMLCoords = getKMLCoords(kmlFile)
		
		#use image library to get the height and width of the image
		imageCoords = getImageCoords(imageFile)

		#Use GDAL to convert the image into a vrt file with latlonquad values embedded
		command = "-of VRT -a_srs EPSG:4326 -gcp 0 0 "+KMLCoords[0]['latitude']+" "+KMLCoords[0]['longitude']+" -gcp "+str(imageCoords[0])+" 0 "+KMLCoords[1]['latitude']+" "+KMLCoords[1]['longitude']+" -gcp 0 "+str(imageCoords[1])+" "+KMLCoords[3]['latitude']+" "+KMLCoords[3]['longitude']+" -gcp "+str(imageCoords[0])+" "+str(imageCoords[1])+" "+KMLCoords[2]['latitude']+" "+KMLCoords[2]['longitude']
		vrtCmd = ' '.join(["gdal_translate", command, imageFile, outputDir+"/map.vrt"])
		subprocess.call(vrtCmd, shell=True)

		print "Successfully generated the VRT file"

		Zoomlevel = (raw_input("What zoom levels would you like to generate the tiles for (the higher the level the more zoomed in you can go, use - for ranges e.g. 1-10)")).strip()
		#Use GDAL again to convert the vrt file into a series of tiles that can be dropped into the project
		tilesCmd = ' '.join(['python gdal2tiles.py', '-p mercator -z '+Zoomlevel+' -r bilinear', outputDir+'/map.vrt '+outputDir+'/map'])
		subprocess.call(tilesCmd, shell=True)
		#generate any other files for iOS
	else:
		print "There was an error with your image file"

else:
	print "There was an error with your KML file"