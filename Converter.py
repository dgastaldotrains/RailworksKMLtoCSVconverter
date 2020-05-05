import xml.etree.ElementTree as ET
import glob
import os

def add_named_coordinate(marker_name,marker_coordinate, marker_list):
    longitude, latitude, height = tuple(marker_coordinate.split(','))
    marker_list += ['{0},{1},"{2}"'.format(longitude,latitude,marker_name)]
    
def add_series_coordinate(marker_coordinate, marker_list):
    longitude, latitude, height = tuple(marker_coordinate.split(','))
    marker_list += ["{0},{1}".format(longitude,latitude)]
    
def add_newlines(markers_list):
    for i in range(len(markers_list)):
        if i == (len(markers_list) - 1):
            continue
        else:
            markers_list[i] += "\n"

def write_series_file(name,coordinates_list,kml_filename,destination_path):
    series_markers_list = []
    for coordinate in coordinates_list:
        add_series_coordinate(coordinate,series_markers_list)
    add_newlines(series_markers_list)
    filename = kml_filename + " - " + name + ".csv"
    with open(os.path.join(destination_path,filename),'w') as file:
        file.writelines(series_markers_list)

#The only required datas are the kml container folder and the destination path folder.
#If the user wants them to reside in the radix of the kml folder you could use 
kml_folder = "C:\\Users\\dinig\\OneDrive\\PROGETTO NODO DI TORINO\\KML"
kml_list = glob.glob(os.path.join(kml_folder,"*.kml"))
destination_folder = os.path.join(os.path.dirname(kml_folder),"CSV per blueprints")
if not(os.path.isdir(destination_folder)):
    print("Creating destination directory.")
    os.makedirs(destination_folder)
else:
    print("Destination directory already exists. Checking the presence of old files.")
    if not(len(glob.glob(os.path.join(destination_folder,"*.csv"))) == 0):
        print("Removing old files.")
        for file in os.listdir(destination_folder):
            os.remove(os.path.join(destination_folder, file))
    else:
        print("No file to remove.")
for kml_file in kml_list:
    kml_filename = os.path.basename(kml_file)[:-4]
    print("Working on " + kml_filename + " kml file")
    named_markers_list = []
    tree = ET.parse(kml_file)
    root = tree.getroot()
    document = root.find('{http://www.opengis.net/kml/2.2}Document')
    for placemark in document.iter('{http://www.opengis.net/kml/2.2}Placemark'):
        name = placemark.find('{http://www.opengis.net/kml/2.2}name').text
        if not(placemark.find('{http://www.opengis.net/kml/2.2}Point') == None):
            print('\tWorking on point marker "{0}".'.format(name))
            point = placemark.find('{http://www.opengis.net/kml/2.2}Point')
            coordinates = point.find('{http://www.opengis.net/kml/2.2}coordinates').text.strip().replace('\n','').replace('\t','')
            add_named_coordinate(name,coordinates,named_markers_list)
        elif not(placemark.find('{http://www.opengis.net/kml/2.2}LineString') == None):
            print('\tWorking on series marker "{0}".'.format(name))
            series = placemark.find('{http://www.opengis.net/kml/2.2}LineString')
            coordinates = series.find('{http://www.opengis.net/kml/2.2}coordinates').text.strip().replace('\n','').replace('\t','').split(' ')
            write_series_file(name,coordinates,kml_filename,destination_folder)
        elif not(placemark.find('{http://www.opengis.net/kml/2.2}Polygon') == None):
            print('\tWorking on polygon marker "{0}".'.format(name))
            polygon = placemark.find('{http://www.opengis.net/kml/2.2}Polygon')
            coordinates = polygon.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs').find('{http://www.opengis.net/kml/2.2}LinearRing').find('{http://www.opengis.net/kml/2.2}coordinates').text.strip().replace('\n','').replace('\t','').split(' ')
            write_series_file(name,coordinates,kml_filename,destination_folder)
    add_newlines(named_markers_list)
    if len(glob.glob(os.path.join(destination_folder,"*.csv"))) == 0:
        filename = kml_filename + ".csv"
    else:
        filename = kml_filename + " - Named markers.csv"
    with open(os.path.join(destination_folder,filename),'w') as file:
        file.writelines(named_markers_list)
