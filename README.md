maptoapp
========

A simple python script to convert KML into map tiles ready for iOS projects. Currently only tested in Mac OS X.


Setup
-----
1. Install the **GDAL Complete** framework from www.kyngchaos.com/software/frameworks
2. Setup GDAL in your path (copy and paste into Terminal)

    echo 'export PATH=/Library/Frameworks/GDAL.framework/Programs:$PATH' >> ~/.bash_profile
    source ~/.bash_profile

3. Verify that GDAL is set up by typing `gdal_translate` into a terminal window. If it spits out a load of stuff then it's setup

Usage
-----
Currently the script walks to you through the steps needed to generate the tiles. Basically you just drag and drop your files in (doesn't currently support paths with spaces). Here's the workflow it's based around:

1. Using Google Earth you've created an overlay of the image you wish to add to the tiles and exported this to a KML file
2. You have a high resolution version of the image used in the overlay available in PNG format (Google Earth has issues with big images)
3. You navigate to the maptoapp directory and type `python maptoapp.py` which starts the process
4. You'll be asked to supply the KML file, drag and drop your KML into the Terminal window
5. You'll then be asked to supply the image in PNG format, again just drag and drop into the Terminal window
6. You'll then be asked to supply the output folder, drag and drop this folder into the Terminal window too
7. The script will then process a vrt file based on your input and then prompt you for the zoom levels to generate.
8. For the zoom levels you can enter a single number or a range (using a hypen to seperate the range) between 1 and 20
9. The script then processes the tiles for you based on the details supplied and outputs them in the folder specified
10. The output folder will have a number of folders in it corresponding to the zoom levels you specified. You can drag and drop these into your project (example: http://www.shawngrimes.me/2010/12/mapkit-overlays-session-1-overlay-map/ )

Todo
----
- [ ] Setup script that creates correct environment for script
- [ ] Create a web version where files and images can be uploaded and an archive of the tiles returned