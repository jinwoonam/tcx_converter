import xml.etree.ElementTree as ET

track_name = 'test'

ns = {'garmin_tc': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
      'role': 'http://characters.example.com'}

tree = ET.parse('____139km(1).tcx')
root = tree.getroot()

ET.register_namespace('', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')

all = root.findall(".//*")

# Find waypoint & Change PointType for climbs
upstart = False

for courses in root.findall('garmin_tc:Courses', ns):
    course = courses.find('garmin_tc:Course', ns)
    for cp in course.findall('garmin_tc:CoursePoint', ns):
        name = cp.find('garmin_tc:Name', ns)
        pointtype = cp.find('garmin_tc:PointType', ns)
        #if name.text ==
        if upstart == True:
            pointtype.text = 'Summit'
            upstart = False
        if (name.text.lower().find('st') != -1):
            pointtype.text = 'Straight'
        if (name.text.lower().find('left') != -1):
            pointtype.text = 'Left'
        if (name.text.lower().find('right') != -1):
            pointtype.text = 'Right'
        if (name.text.lower().find('%') != -1):
            pointtype.text = 'Valley'
            upstart = True
        if (name.text.lower().find('top') != -1):
            pointtype.text = 'Summit'
            upstart = False
        if (name.text.lower().find('lunch') != -1) :
            pointtype.text = 'Food'
        if ((name.text.lower().find('hanaro') != -1) | (name.text.lower().find('mart') != -1) | (name.text.lower().find('cu') != -1) | (name.text.lower().find('feed') != -1)):
            pointtype.text = 'Water'

tree.write('output.tcx', 'UTF-8', True)