from xml.dom import minidom
import xml.etree.ElementTree as ET

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


track_name = 'test'

gpx_ns = {'gpx_ns': 'http://www.topografix.com/GPX/1/1',
      'role': 'http://characters.example.com'}

###############################################################################
#  Namespace for tcx file

# <TrainingCenterDatabase
#   xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
#   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#   xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd">

NS = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
NS_XSL_LOC = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd"

ET.register_namespace("", NS)
qname1 = ET.QName(NS, "TrainingCenterDatabase")    # Element QName
qname2 = ET.QName(NS_XSI, "schemaLocation")    # Attribute QName
tcx_root = ET.Element(qname1, {qname2: NS_XSL_LOC})
#print (ET.tostring(tcx_root))

###############################################################################
# Parse GPX File
tree = ET.parse('test.gpx')
gpx_root = tree.getroot()
gpx_all = gpx_root.findall(".//*")

#for x in gpx_all:
#    print(x)

###############################################################################
#  Creating Header of tcx
tcx_folders = ET.SubElement(tcx_root, 'Folders')
tcx_folder_courses = ET.SubElement(tcx_folders, 'Courses')
tcx_coursefolder = ET.SubElement(tcx_folder_courses, 'CourseFolder')
tcx_coursefolder.set('name', 'jwnam_tcx')
tcx_CourseNameRef = ET.SubElement(tcx_coursefolder, 'CourseNameRef')
tcx_Id = ET.SubElement(tcx_CourseNameRef, 'Id')
tcx_Id.text = track_name

###############################################################################
# Add Name in Courses
tcx_Courses = ET.SubElement(tcx_root, 'Courses')
tcx_Course = ET.SubElement(tcx_Courses, 'Course')
tcx_Name = ET.SubElement(tcx_Course, 'Name')
tcx_Name.text = track_name

###############################################################################
# Add TrackPoint in Courses
tcx_Track = ET.SubElement(tcx_Course, 'Track')

for trkpt in gpx_root.iterfind('.//gpx_ns:trkpt', gpx_ns):
      lat = trkpt.get('lat')
      lon = trkpt.get('lon')
      ele = trkpt.find('gpx_ns:ele', gpx_ns)
      #print (lat, lon, ele.text)

      # add <TrackPoint>
      tcx_Trackpoint = ET.SubElement(tcx_Track, 'Trackpoint')
      tcx_Position = ET.SubElement(tcx_Trackpoint, 'Position')
      tcx_Latitude = ET.SubElement(tcx_Position, 'LatitudeDegrees')
      tcx_Longitude = ET.SubElement(tcx_Position, 'LongitudeDegrees')
      tcx_Altitude = ET.SubElement(tcx_Trackpoint, 'AltitudeMeters')
      tcx_Latitude.text = lat
      tcx_Longitude.text = lon
      tcx_Altitude.text = ele.text

###############################################################################
# Add CoursePoint in Courses
for wpt in gpx_root.iterfind('gpx_ns:wpt', gpx_ns):
      lat = wpt.get('lat')
      lon = wpt.get('lon')
      name = wpt.find('gpx_ns:name', gpx_ns)
      #print (lat, lon, name.text)

      # add <CoursePoint>
      tcx_CoursePoint = ET.SubElement(tcx_Course, 'CoursePoint')
      tcx_CPName = ET.SubElement(tcx_CoursePoint, 'Name')
      tcx_CPPosition = ET.SubElement(tcx_CoursePoint, 'Position')
      tcx_CPLatitude = ET.SubElement(tcx_CPPosition, 'LatitudeDegrees')
      tcx_CPLongitude = ET.SubElement(tcx_CPPosition, 'LongitudeDegrees')
      tcx_CPPointType = ET.SubElement(tcx_CoursePoint, 'PointType')
      tcx_CPName.text = name.text
      tcx_CPLatitude.text = lat
      tcx_CPLongitude.text = lon
      tcx_CPPointType.text = 'Generic'


      # Find waypoint & Change PointType for climbs
      upstart = False

      if upstart == True:
            tcx_CPPointType.text = 'Summit'
            upstart = False
      if (tcx_CPName.text.lower().find('st') != -1):
            tcx_CPPointType.text = 'Straight'
      if (tcx_CPName.text.lower().find('left') != -1):
            tcx_CPPointType.text = 'Left'
      if (tcx_CPName.text.lower().find('right') != -1):
            tcx_CPPointType.text = 'Right'
      if (tcx_CPName.text.lower().find('%') != -1 | (name.text.lower().find('ups') != -1)):
            tcx_CPPointType.text = 'Valley'
            upstart = True
      if (tcx_CPName.text.lower().find('top') != -1):
            tcx_CPPointType.text = 'Summit'
            upstart = False
      if (tcx_CPName.text.lower().find('lunch') != -1) :
            tcx_CPPointType.text = 'Food'
      if ((tcx_CPName.text.lower().find('hanaro') != -1) | (name.text.lower().find('mart') != -1) | (name.text.lower().find('cu') != -1) | (name.text.lower().find('feed') != -1)):
            tcx_CPPointType.text = 'Water'

tcx_file = ET.ElementTree()
tcx_file._setroot(tcx_root)
indent(tcx_root)

#ET.dump(tcx_root)      # Print in console
tcx_file.write('output.tcx', 'UTF-8', xml_declaration=True)

