#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""GPX Course Profile Plotter -- main
    Python Version  : 3.5.5 in windows
    Created date    : 2017-04-04
"""

import save2tcx
import gpxpy.gpx    as gpx
import gpxpy.parser as parser
from geopy.distance import distance
from geopy.distance import great_circle
import ntpath
import time

__author__ = 'Seijung Park'
__license__ = 'GPLv2'
__version__ = '0.1.2'
__date__ = '2018-04-11'

"""
def get_nearest( points, wpt):
    near = []
    for i in range(len(points)):
        dist = vincenty( (points[i].latitude, points[i].longitude), (wpt.latitude, wpt.longitude)).meters
        if (dist < 20):
            print( "Found pos:%4d, dist:%3dm" %  (i, dist))
            near.append( points[i] )
            print( points[i] )
            return i
        #print( p, dist)
    return 0
"""


class my_wpt(gpx.GPXTrackPoint):
    def __init__(self):
        self.name = []
        self.pos = 0  # x, y array position
        self.latitude = 0
        self.longitude = 0
        self.km = 0
        self.dkm = 0
        self.ascen = 0
        self.dascen = 0
        self.kind = ''

    def __str__(self):
        return '[my_wpt{%s}:%s,%s %s: %s,%s]' % (self.name, self.pos, self.km, self.dkm, self.ascen, self.dascen)

    def __lt__(self, other):
        return self.pos < other.pos

    def get_nearest(self, points, wpt):
        near = []
        min_dist = 200;
        for i in range(len(points)):
            dist = distance((points[i].latitude, points[i].longitude), (wpt.latitude, wpt.longitude)).meters
            if (dist < min_dist):
                min_dist = dist
                #print( "Found pos:%4d, dist:%3dm (%s)" %  (i, dist, wpt.name))
                self.name = wpt.name
                self.pos = i
                self.latitude = wpt.latitude
                self.longitude = wpt.longitude
                print(points[i])
                if (min_dist < 20):
                    return i
        return -1

    def set_last(self, points):
        self.name = '완주'
        self.pos = len(points) - 1
        return

    def strip_name(self, clist, mlist):
        a = self.name

        if a[0] == 's':
            a = a[1:]

        elif a[0] == 'c':
            if a[1] in clist:
                a = a[2:]
            else:
                a = a[1:]
        elif a[0] == 'm':
            if a[1] in mlist:
                a = a[2:]
            else:
                a = a[1:]

        if len(a) > 3 and a[-3] == '_':
            a = a[:-3]
        elif len(a) > 2 and a[-2] == '_':
            a = a[:-2]
        elif len(a) > 1 and a[-1] == '_':
            a = a[:-1]

        self.name = a
        return self.name

    def get_km(self, prev, x):
        self.km = x[self.pos]
        if prev is None:
            self.dkm = self.km
        else:
            self.dkm = self.km - prev.km
        return

    def set_kind(self):
        kindlist = ["Generic", "Summit", "Valley", "Water", "Food", "Danger", "Left", "Right", "Straight", "First Aid",
                    "4th Category", "3rd Category", "2nd Category", "1st Category", "Hors Category", "Sprint"]

        print("name = {}".format(self.name))
        self.kind = kindlist[0]  # Generic
        if self.name[0] == 's':
            self.kind = kindlist[1]  # Summit

        elif self.name[0] == 'c':
            if self.name[1] == '1':
                self.kind = kindlist[13]  # 1st Category
            elif self.name[1] == '2':
                self.kind = kindlist[12]  # 2nd Category
            elif self.name[1] == '3':
                self.kind = kindlist[11]  # 3rd Category
            elif self.name[1] == '4':
                self.kind = kindlist[10]  # 4th Category
            elif self.name[1] == 'H':
                self.kind = kindlist[14]  # Hors Category
            elif self.name[1] == 'S':
                self.kind = kindlist[15]  # Sprint

        elif self.name[0] == 'm':
            if self.name[1] == 'G':
                self.kind = kindlist[0]  # Generic
            elif self.name[1] == 'S':
                self.kind = kindlist[1]  # Summit
            elif self.name[1] == 'V':
                self.kind = kindlist[2]  # Valley
            elif self.name[1] == 'W':
                self.kind = kindlist[3]  # Water
            elif self.name[1] == 'F':
                self.kind = kindlist[4]  # Food
            elif self.name[1] == 'D':
                self.kind = kindlist[5]  # Danger
            elif self.name[1] == 'L':
                self.kind = kindlist[6]  # Left
            elif self.name[1] == 'R':
                self.kind = kindlist[7]  # Right
            elif self.name[1] == 'C':
                self.kind = kindlist[8]  # Straght
            elif self.name[1] == 'A':
                self.kind = kindlist[9]  # First Aid

        return self.kind

    def get_ascen(self, prev, y):
        self.ascen = y[self.pos]
        if prev is None:
            self.dascen = self.ascen
        else:
            self.dascen = self.ascen - prev.ascen
        return


def calc_dist(points):
    x = []
    y = []
    ascen = []

    lenth = 0
    upelev = 0
    print("\n")
    lenth = len(points)
    point0 = points[0]
    point1 = points[1]

    sum1 = 0
    sum2 = 0
    x.append(0)
    y.append(0)
    ascen.append(0)

    for i in range(1, lenth):
        lat0 = points[i - 1].latitude
        lon0 = points[i - 1].longitude
        lat1 = points[i].latitude
        lon1 = points[i].longitude

        dist1 = distance((lat0, lon0), (lat1, lon1)).meters
        sum1 += dist1
        sum2 = sum1 / 1000

        elev = points[i].elevation
        delev = (elev - points[i - 1].elevation)

        # factor(4.0) is calibrated. do not modify
        # ignore single up point
        # el0 =
        # el1
        # el2
        if delev > 4.0:
            upelev += delev
        if (dist1 == 0):
            dist1 = 1
        grad = delev / dist1 * 100
        # print( "%7.1f, %8.3f %5.1f %4.1f" % (dist1, sum2, elev, grad))
        x.append(sum1)
        y.append(elev)
        ascen.append(upelev)
    print("Total up elevation: %f\n" % (upelev))
    return x, y, ascen


def do_job(f_name, speed=20):
    clist = '1234hs'
    mlist = 'GSVWFDLRCA'

    gpx_file = open(f_name, 'r', encoding='UTF8')
    wpt_list = []
    s_list = []

    gpx_parser = parser.GPXParser(gpx_file)
    gpx_parser.parse()

    gpx_file.close()

    gpx = gpx_parser.parse()
    x, y, ascen = calc_dist(gpx.tracks[0].segments[0].points)

    mypoints = gpx.tracks[0].segments[0].points
    # mypoints.append( gpx.tracks[0].segments[0].points)

    bound = gpx.get_bounds()
    print(bound.max_latitude, bound.max_longitude, bound.min_latitude, bound.min_longitude)
    # save2tcx.print_point( mypoints[0], mypoints[-1] )
    # print(save2tcx.lapinfo( bound, [100, 90], 5000, 300000))

    for waypoint in gpx.waypoints:
        # print ('waypoint {0} -> ({1},{2})'.format( waypoint.name, waypoint.latitude, waypoint.longitude ))
        print(waypoint)
        # pos = get_nearest( gpx.tracks[0].segments[0].points, waypoint)
        w = my_wpt()
        pos = w.get_nearest(gpx.tracks[0].segments[0].points, waypoint)

        # throw if wp is not matched
        if pos == -1:
            continue
        w.set_kind()
        if pos != 0:
            if len(wpt_list) == 0:
                w.get_km(None, x)
                w.get_ascen(None, ascen)
            else:
                w.get_km(wpt_list[-1], x)
                w.get_ascen(wpt_list[-1], ascen)

            if (w.name[0] in mlist) or (w.name[0] in clist) or w.name[0] == 's':
                w.strip_name(clist, mlist)
                s_list.append(w)
            else:
                w.strip_name(clist, mlist)
                wpt_list.append(w)
            # wpt.append(pos)
            # wpt_name.append(waypoint.name)

    w = my_wpt()
    w.set_last(gpx.tracks[0].segments[0].points)
    if len(wpt_list) == 0:
        w.get_km(None, x)
        w.get_ascen(None, ascen)
    else:
        print(len(x), len(ascen))
        w.get_km(wpt_list[-1], x)
        w.get_ascen(wpt_list[-1], ascen)
    wpt_list.append(w)

    # for w in wpt_list:
    #    print(w)

    name = ntpath.basename(f_name)
    # speed = 20
    """
    #for i in range(len(mypoints)):
    for i in range(100):
        x[i] = x[i] * 1000
        print(x[i])
        tstr = save2tcx.time2str(x[i] / (speed * 1000 / 3600))
        s = save2tcx.trackpoint( mypoints[i], x[i], tstr)
        print(s)
     """
    save2tcx.save(mypoints, x, speed, wpt_list, s_list, name)

    # print(help(gpx))
    # print(dir(gpx))
    # print(help(gpx.tracks[0].segments[0].points[0]))
    # print(dir(gpx.tracks[0].segments[0].points[0]))

    return


def main():
    # print(help(gpx))
    # do_job('D:/SRC/python/GPX2TCX/sample.gpx', 20)
    do_job('D:/workspace/strava/gpx2tcx/test.gpx', 20)


if __name__ == '__main__':
    main()

# class GPXTrackPoint:
