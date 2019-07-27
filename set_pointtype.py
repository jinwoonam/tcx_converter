#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import wpttype
import xml.etree.ElementTree as ET
import sys

#parameter = sys.argv[0].split('.')
if len(sys.argv) == 1:          # 옵션 없으면 도움말 출력하고 종료
    print("use test.gpx")
    track_name = 'test'
else:
    sys.argv[1]
    track_name = sys.argv[1].split('.')[0]
    print("use", sys.argv[1])

ns = {'garmin_tc': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
      'role': 'http://characters.example.com'}

tree = ET.parse(track_name+'.tcx')
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
        pointtype.text = wpttype.get_wpt_type(name.text)
'''
        if upstart == True:
            pointtype.text = 'Summit'
            upstart = False
        if (name.text.lower().find('st') != -1):
            pointtype.text = 'Straight'
        if (name.text.lower().find('left') != -1):
            pointtype.text = 'Left'
        if (name.text.lower().find('right') != -1):
            pointtype.text = 'Right'
        if (name.text.lower().find('%') != -1 | (name.text.lower().find('ups') != -1)):
            pointtype.text = 'Valley'
            upstart = True
        if (name.text.lower().find('top') != -1):
            pointtype.text = 'Summit'
            upstart = False
        if (name.text.lower().find('lunch') != -1):
            pointtype.text = 'Food'
        if ((name.text.lower().find('hanaro') != -1) | (name.text.lower().find('mart') != -1) | (name.text.lower().find('cvs') != -1) | (name.text.lower().find('feed') != -1)):
            pointtype.text = 'Water'
        if (name.text.lower().find('open') != -1):
            pointtype.text = 'Sprint'
'''
tree.write(track_name+'_wp.tcx', 'UTF-8', True)