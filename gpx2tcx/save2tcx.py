#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""GPX Course Profile Plotter -- main
    Python Version  : 3.5.5 in windows
    Created date    : 2017-04-04
"""

import gpxpy.parser as parser
from geopy.distance import vincenty
from geopy.distance import great_circle
import ntpath
from time import strftime, gmtime
import codecs

__author__  = 'Seijung Park'
__license__ = 'GPLv2'
__version__ = '0.1.3'
__date__    = '2018-04-11'



def time2str(t):
    # 2010-01-01T00:00:00Z
    ref_time = 1262304000
    return strftime( "%Y-%m-%dT%H:%M:%SZ", gmtime(ref_time+t))


def header1():
    hdr = """<?xml version="1.0" encoding="UTF-8"?>
<TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd">
"""
    return hdr


#print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))
 

def header2( name ):
    #if len(name) > 10:
    #    name = name[:10]
    hdr = """  <Folders>
    <Courses>
      <CourseFolder Name=\"{}\">
        <CourseNameRef>
          <Id>{}</Id>
        </CourseNameRef>
      </CourseFolder>
    </Courses>
  </Folders>
""".format(name,name)
    return hdr


def header3(  name ):
    if len(name) > 10:
        name = name[:10]
    hdr = """  <Courses>
    <Course>
      <Name>{}</Name>
""".format(name)
    return hdr


def footer_trackpoint():
    ftr = """      </Track>
"""
    return ftr


def footer():
    ftr = """    </Course>
  </Courses>
</TrainingCenterDatabase>

"""
    return ftr

    
def lapinfo( p, time, len):
    lap = """      <Lap>
        <TotalTimeSeconds>{}</TotalTimeSeconds>
        <DistanceMeters>{}</DistanceMeters>
        <BeginPosition>
          <LatitudeDegrees>{}</LatitudeDegrees>
          <LongitudeDegrees>{}</LongitudeDegrees>
        </BeginPosition>
        <EndPosition>
          <LatitudeDegrees>{}</LatitudeDegrees>
          <LongitudeDegrees>{}</LongitudeDegrees>
        </EndPosition>
        <Intensity>Active</Intensity>
      </Lap>
      <Track>
""".format(time, len, p[0].latitude, p[0].longitude, p[-1].latitude, p[-1].longitude)
    return lap

       
def trackpoint( pos, len, time):
    cpt = """        <Trackpoint>
          <Time>{}</Time>
          <Position>
            <LatitudeDegrees>{}</LatitudeDegrees>
            <LongitudeDegrees>{}</LongitudeDegrees>
          </Position>
          <AltitudeMeters>{}</AltitudeMeters>
          <DistanceMeters>{:.3f}</DistanceMeters>
        </Trackpoint>
""".format( time, pos.latitude, pos.longitude, pos.elevation, len)
    return cpt


def coursepoint(latitude, longitude, time, name, kind='Generic'):
    kindlist = ["Generic", "Summit", "Valley", "Water", "Food", "Danger", "Left", "Right", "Straight", "First Aid", "4th Category", "3rd Category", "2nd Category", "1st Category", "Hors Category", "Sprint" ]
    
    if kind == '':
        kind = 'Generic'
    #kind = 'Generic'
        
    if len(name) > 10:
        name = name[:10]
    name = name.replace("&", "&amp;", 3)

    cpt = """      <CoursePoint>
        <Name>{}</Name>
        <Time>{}</Time>
        <Position>
          <LatitudeDegrees>{}</LatitudeDegrees>
          <LongitudeDegrees>{}</LongitudeDegrees>
        </Position>
        <PointType>{}</PointType>
      </CoursePoint>
""".format( name, time, latitude, longitude, kind)
    return cpt


    
    
"""
순서
header1
header2
header3
lapinfo
trackpoint * n
footer_trackpoint
coursepoint * m
footer
"""
def save( points, x, speed, wpt_list, s_list, name):
    #name = name[:-4]
    name = name.split('.')[0]
    f = codecs.open(name+'.tcx', 'w', 'utf-8')
    
    h = header1()
    h = h + header2( name )
    h = h + header3( name )
    h = h + lapinfo( points, x[-1]/(speed * 1000 / 3600), x[-1])
    #print(h)
    f.write(h)
    
    s = ""
    for i in range(len(x)):
        #x[i] = x[i] * 1000
        #print(x[i])
        tstr = time2str(x[i] / (speed * 1000 / 3600))
        s = s + trackpoint( points[i], x[i], tstr)
    
    s = s + footer_trackpoint()
    #print(s)
    f.write(s)

    w_list = wpt_list + s_list
    #print( "len = ", len(w_list))
    if w_list is not None:
        w_list.sort()
        c = ""
        for wpt in w_list:
            #print(wpt)
            time = time2str(x[wpt.pos] / (speed * 1000 / 3600))
            #c = c + coursepoint( points[wpt.pos], time, wpt.name, wpt.kind)
            c = c + coursepoint(wpt.latitude, wpt.longitude, time, wpt.name, wpt.kind)
        #print(c)
        f.write(c)
        
    t = footer()
    #print(f)
    f.write(t)
    return


def print_point( p1, p2 ):
    print( p1.longitude, p1.latitude, p1.elevation, p1.time, p1.distance )
    print( p2.longitude, p2.latitude, p2.elevation, p2.time, p2.distance )
    return


def main():
    a = header1()
    a = a + header2( "test str" )
    a = a + header3( "test str" )
    
    time = 67966.0000000
    len = 188796.3125000

    bounds = p1_y = 37.5125859
    p1_x = 127.0020282
    ele1 = 9.8000000
    
    p2_y = 36.6073117
    p2_x = 126.7924189
    ele2 = 25.3000000
    
    a = a + lapinfo( [p1_y, p1_x, ele1], [ele1, ele2], time, len)
    print ( a )
	
	
if __name__ == '__main__':
	main()
