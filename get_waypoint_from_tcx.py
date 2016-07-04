import xml.etree.ElementTree as ET

track_name = 'test'

ns = {'garmin_tc': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
      'role': 'http://characters.example.com'}

tree = ET.parse('Hs65_course.tcx')
root = tree.getroot()

# all = root.findall(".//*Time")
# all = root.findall(".//*[@name='Course']/CoursePoint")
#all = list(root.iter("Lap"))
all = root.findall(".//*")

gpx_file = open(track_name + ".gpx", 'wt')

# Write Header
gpx_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
gpx_file.write('<gpx xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1" creator="jinuz" xmlns="http://www.topografix.com/GPX/1/1">\n')
gpx_file.write('  <metadata>\n')
gpx_file.write('    <desc>Converted by jinuz</desc>\n')
gpx_file.write('    <link href="http://blog.naver.com/hl1sfz">\n')
gpx_file.write('      <text>Jinuz Blog</text>\n')
gpx_file.write('    </link>\n')
gpx_file.write('  </metadata>\n')

# Convert waypoint
for courses in root.findall('garmin_tc:Courses', ns):
    course = courses.find('garmin_tc:Course', ns)
    for cp in course.findall('garmin_tc:CoursePoint', ns):
        name = cp.find('garmin_tc:Name', ns)
        position = cp.find('garmin_tc:Position', ns)
        lat = position.find('garmin_tc:LatitudeDegrees', ns)
        lon = position.find('garmin_tc:LongitudeDegrees', ns)
        #print (name.text, lat.text, lon.text)
        gpx_file.write('  <wpt lat="%s" lon="%s">\n' % (lat.text, lon.text))
        gpx_file.write('    <name>%s</name>\n' % (name.text))
        gpx_file.write('  </wpt>\n')


# Convert TrackSegment
gpx_file.write('  <trk>\n')
gpx_file.write('    <trkseg>\n')

for courses in root.findall('garmin_tc:Courses', ns):
    course = courses.find('garmin_tc:Course', ns)
    track = course.find('garmin_tc:Track', ns)
    for tp in track.findall('garmin_tc:Trackpoint', ns):
        position = tp.find('garmin_tc:Position', ns)
        lat = position.find('garmin_tc:LatitudeDegrees', ns)
        lon = position.find('garmin_tc:LongitudeDegrees', ns)
        altitude = tp.find('garmin_tc:AltitudeMeters', ns)

        #print (name.text, lat.text, lon.text)
        gpx_file.write('      <trkpt lat="%s" lon="%s">\n' % (lat.text, lon.text))
        gpx_file.write('        <ele>%s</ele>\n' % (altitude.text))
        gpx_file.write('      </trkpt>\n')

gpx_file.write('    </trkseg>\n')
gpx_file.write('  </trk>\n')

# Write Footer
gpx_file.write('</gpx>\n')

gpx_file.close()
