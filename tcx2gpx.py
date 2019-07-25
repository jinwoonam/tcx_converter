#-*- coding:utf-8 -*-
"""Simple converter from TCX file to GPX format

Usage:   python tcx2gpx.py   foo.tcx  > foo.gpx

Streaming implementation works for large files.


Open Source: MIT Licencse.
This is or was <http://www.w3.org/2009/09/geo/tcx2gpx.py>
Author: http://www.w3.org/People/Berners-Lee/card#i
Written: 2009-10-30
Last change: $Date: 2009/10/28 13:44:33 $

source : https://www.w3.org/2009/09/geo/tcx2gpx.py
"""
import urllib
from xml import sax
from xml.sax import saxutils
import sys, os

w = sys.stdout.write

TCX_NS = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"


class MyHandler(sax.handler.ContentHandler):
    def __init__(self):
        self.time = ""
        self.lat = ""
        self.lon = ""
        self.alt = ""
        self.content = ""
        self.name = ""
        self.desc = ""

    def startDocument(self):
        w("""<gpx xmlns="http://www.topografix.com/GPX/1/1"
        creator="http://www.w3.org/2009/09/geo/tcx2gpx.py"
        version="1.1"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
        """)

    def endDocument(self):
        w('</gpx>\n')

    def startElement(self, name, attrs):
        self.content = ""
        if name == 'Track':
            w(' <trk>\n')
        elif name == 'CoursePoint':
            w(' <wpt lat="%s" long="%s">\n' % (self.lat, self.lon))

    def characters(self, content):
        self.content = self.content + saxutils.escape(content)

    #    def endElementNS(fname, qname, attrs):
    #        (ns, name) = fname

    def endElement(self, name):
        if name == 'Track':
            w(' </trk>\n')
        elif name == 'Trackpoint':
            w('  <trkpt lat="%s" lon="%s">\n' % (self.lat, self.lon))
            if (self.alt): w('   <ele>%s</ele>\n' % self.alt)
            if (self.time): w('   <time>%s</time>\n' % self.time)
            w('  </trkpt>\n')
            sys.stdout.flush()
        elif name == 'LatitudeDegrees':
            self.lat = self.content
        elif name == 'LongitudeDegrees':
            self.lon = self.content
        elif name == 'AltitudeMeters':
            self.alt = self.content
        elif name == 'Time':
            self.time = self.content
        elif name == 'CoursePoint':
            w(' </wpt>\n')
        elif name == 'Name':
            self.name = self.content
            w('  <name>%s</name>\n' % (self.name))
        elif name == 'Notes':
            self.desc = self.content
            w('  <desc>%s</desc>\n' % (self.desc))


handler = MyHandler()


def read_TCX(uri):
    sax.parse(uri, handler)


read_TCX(sys.argv[1])

# ends
