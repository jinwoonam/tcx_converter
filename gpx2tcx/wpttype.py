#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""GPX Course Profile Plotter -- main
    Python Version  : 3.5.5 in windows
    Created date    : 2017-04-04
"""

__author__  = 'Jinwoo Nam'
__license__ = 'GPLv2'
__version__ = '0.1.1'
__date__    = '2019-07-26'

upstart = 0

def get_wpt_type(name):
    # Find waypoint & Change PointType for climbs
    # ["Generic", "Summit", "Valley", "Water", "Food", "Danger", "Left", "Right", "Straight", "First Aid",
    # "4th Category", "3rd Category", "2nd Category", "1st Category", "Hors Category", "Sprint"]
    ret_str = 'Generic'

    if get_wpt_type.upstart != -1:
        #ret_str = 'Summit'
        ret_str = {5: "Sprint", 4: "4th Category", 3: "3rd Category", 2: "2nd Category", 1: "1st Category", 0: "Hors Category"}.get(get_wpt_type.upstart, 'Summit')
        get_wpt_type.upstart = -1

    if (name.lower().find('st') != -1):
        ret_str = 'Straight'
    if (name.lower().find('left') != -1):
        ret_str = 'Left'
    if (name.lower().find('right') != -1):
        ret_str = 'Right'
    if (name.lower().find('%') != -1 | (name.lower().find('ups') != -1)):
        ret_str = 'Valley'
        get_wpt_type.upstart = int(name[0])
    if (name.lower().find('top') != -1):
        ret_str = 'Summit'
        get_wpt_type.upstart = -1
    if (name.lower().find('lunch') != -1):
        ret_str = 'Food'
    if (name.lower().find('!!') != -1):
        ret_str = 'Danger'
    if ((name.lower().find('hanaro') != -1) | (name.lower().find('mart') != -1) | (
            name.lower().find('cvs') != -1) | (name.lower().find('feed') != -1)):
        ret_str = 'Water'

    return ret_str
get_wpt_type.upstart = -1




def main():
    upstart = 0  # 0=HC, 1~4=Cat1~4, 5=TT, -1=not upstart

'''
    # Test code
    print(get_wpt_type('3_10.1_4%'))
    print(get_wpt_type.upstart)
    print(get_wpt_type('kom'))
'''

if __name__ == '__main__':
    main()
