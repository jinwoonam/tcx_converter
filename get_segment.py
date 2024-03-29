import requests
import sys
import datetime
import webbrowser

#strava_token = "Bearer 01af046cabff7462c5512440394dbff40bf570a8"
# https://www.strava.com/settings/api
token_file = "strava_token.txt"

# file name : segement_190712.gpx
seg_file = datetime.datetime.now().strftime('segment_%y%m%d.gpx')

postman_headers = {
    #'Authorization': "Bearer " + strava_token,
    'User-Agent': "PostmanRuntime/7.15.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "918a31ce-671f-4665-8487-d34cd41d202f,356930ab-1ac0-4478-80e0-150922f50d16",
    'Host': "www.strava.com",
    'cookie': "_strava4_session=a1kcv8lbe0i7rlukjdt9kvnfo0viif8d",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }


def write_strava_token():
    if (3 == len(sys.argv) and 'token' == sys.argv[1]):
        file = open(token_file, "w")
        file.write(sys.argv[2])
        file.close()
        print("Strava token is written to file.")
        return 1
    else:
        return 0


def read_strava_token():
    try:
        file = open(token_file, "r")
        token = file.readline()
        # print(token)
        file.close()
        return token
    except OSError as err:
        print("OS error: {0}".format(err))
        print("Strava token file ({token_file}) is not exist".format(token_file=token_file))
        print("Usage : {py} token <access_toekn>".format(py=sys.argv[0]))
        webbrowser.open('https://www.strava.com/settings/api')
        exit(0)
        return 0


def check_strava_token():
    r = requests.request("GET", "https://www.strava.com/api/v3/athlete", headers=postman_headers)

    if (200 == r.status_code):  # check OK
        return 1
    else:   # check Fail
        print("Error: Strava Token Auth (err:{code})".format(code=r.status_code))
        print("Usage : {py} token <access_toekn>".format(py=sys.argv[0]))
        webbrowser.open('https://www.strava.com/settings/api')
        exit(0)
        return 0


#######################################################################################################################
# Token writing to file
if (write_strava_token()):
    exit(0)

# read token
strava_token = read_strava_token()
if (strava_token):
    #print('Current Strava token is {token}\n'.format(token=strava_token))
    postman_headers['Authorization'] = "Bearer " + strava_token


# check strava token
if (1 == len(sys.argv)):
    r = requests.request("GET", "https://www.strava.com/api/v3/athlete", headers=postman_headers)

    if (check_strava_token()):
        print("Usage : {py} segment_number".format(py=sys.argv[0]))
    exit(0)

for seg_no in sys.argv:
    #print(seg_no)
    if (seg_no == sys.argv[0]):
        f = open(seg_file, 'a')
        f.write('<!--주요세그먼트 -->\n')
        f.close()
        continue;

    #TODO check error
    url = "https://www.strava.com/api/v3/segments/" + seg_no
    r = requests.request("GET", url, headers=postman_headers).json()
    #print(r.text)

    # URL & Information
    gpx_wpt = ('<!--https://www.strava.com/segments/{seg_no} -->\n'.format(seg_no=seg_no))
    gpx_wpt += ('<!--{name} (Cat:{cat}, Dist:{dist:.1f}km, Grade:{grade}%) -->\n'
                .format(name=r["name"], cat=5-r["climb_category"], dist=r["distance"]/1000, grade=r["average_grade"]))

    # Start Position
    gpx_wpt += ('  <wpt lat="{latt}" lon="{long}">\n'.format(latt=r["start_latlng"][0], long=r["start_latlng"][0]))
    gpx_wpt += ('    <name>{cat}_{dist:.1f}_{grade}%</name>\n'
        .format(cat=5-r["climb_category"], dist=r["distance"]/1000, grade=r["average_grade"]))
    gpx_wpt += ('    <desc>{name}</desc>\n'.format(name=r["name"]))
    gpx_wpt += ('  </wpt>\n')

    # End Position
    gpx_wpt += ('  <wpt lat="{latt}" lon="{long}">\n'.format(latt=r["end_latlng"][0], long=r["end_latlng"][1]))
    gpx_wpt += ('    <name>{name}</name>\n'.format(name=r["name"]))
    gpx_wpt += ('    <desc>{name}</desc>\n'.format(name=r["name"]))
    gpx_wpt += ('  </wpt>\n')

    print(gpx_wpt)


    # apend to file
    f = open(seg_file, 'a')
    f.write(gpx_wpt)
    print(" --> Written to {filename} \n ".format(filename=seg_file))
    f.close()

''' GPX waypoint Sample 
    {"id":8306671,"resource_state":3,"name":"계파로 오픈구간","activity_type":"Ride",
     "distance":12801.7,"average_grade":0.4,"maximum_grade":46.9,
     "elevation_high":316.5,"elevation_low":134.8,
     "start_latlng":[38.066698,127.657155],"end_latlng":[38.161143,127.639063],
     "start_latitude":38.066698,"start_longitude":127.657155,
     "end_latitude":38.161143,"end_longitude":127.639063,"climb_category":0,
     "city":"Hwacheon-gun","state":"Gangwon-do","country":"South Korea",
     "private":false,"hazardous":false,"starred":false,
     "created_at":"2014-10-09T12:50:11Z","updated_at":"2019-07-10T08:19:53Z",
     "total_elevation_gain":617.8,
     "map":{"id":"s8306671","polyline":"y{igFe`djW...B@uEC","resource_state":3},
     "effort_count":202,"athlete_count":134,"star_count":0,
     "athlete_segment_stats":{"pr_elapsed_time":1905,"pr_date":"2019-07-10","effort_count":1}}

      <wpt lat="37.54348845865" lon="127.106323242188">
        <name>출발 지점</name>
        <desc>설명추가</desc>
      </wpt>
'''
