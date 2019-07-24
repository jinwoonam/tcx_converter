import requests
import sys
import datetime
import webbrowser

# https://www.strava.com/settings/api
#strava_token = "Bearer 01af046cabff7462c5512440394dbff40bf570a8"
token_file = "strava_token.txt"

# Token writing
if (3 == len(sys.argv) and 'token' == sys.argv[1]):
    file = open(token_file, "w")
    file.write(sys.argv[2])
    file.close()
    print("Strava token is written to file.")
    exit(0)

# read token
try:
    file = open(token_file,"r")
    strava_token = file.readline()
    #print(strava_token)
    file.close()
except OSError as err:
    print("OS error: {0}".format(err))
    print("Strava token file ({token_file}) is not exist".format(token_file=token_file))
    print("Usage : {py} token <access_toekn>".format(py=sys.argv[0]))
    webbrowser.open('https://www.strava.com/settings/api')
    exit(0)

headers = {
    'Authorization': "Bearer " + strava_token,
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

if (2 == len(sys.argv)):
    seg_no = sys.argv[1]
else:
    r = requests.request("GET", "https://www.strava.com/api/v3/athlete", headers=headers)
    #print(r.status_code)

    if (200 != r.status_code):
        print("Error: Strava Token Auth")
        webbrowser.open('https://www.strava.com/settings/api')
        exit(0)
    else :
        print("Usage : {py} segment_number".format(py=sys.argv[0]))
        exit(0)

url = "https://www.strava.com/api/v3/segments/" + seg_no

r = requests.request("GET", url, headers=headers).json()
#print(r.text)

''' Sample 
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

# URL & Information
gpx_wpt = ('<!--https://www.strava.com/segments/{seg_no} -->\n'.format(seg_no=seg_no))
gpx_wpt += ('<!--{name} (Cat:{cat}, Dist:{dist:.1f}km, Grade:{grade}%)\n'
            .format(name=r["name"], cat=5-r["climb_category"], dist=r["distance"]/1000, grade=r["average_grade"]))

# Start Position
gpx_wpt += ('  <wpt lat="{latt}" lon="{long}">\n'
	.format(latt=r["start_latitude"], long=r["start_longitude"]))
gpx_wpt += ('    <name>{cat}_{dist:.1f}_{grade}%</name>\n'
	.format(cat=5-r["climb_category"], dist=r["distance"]/1000, grade=r["average_grade"]))
gpx_wpt += ('    <desc>{name}</desc>\n'.format(name=r["name"]))
gpx_wpt += ('  </wpt>\n')

#end Position
gpx_wpt += ('  <wpt lat="{latt}" lon="{long}">\n'
	.format(latt=r["end_latitude"], long=r["end_longitude"]))
gpx_wpt += ('    <name>{name}</name>\n'.format(name=r["name"]))
gpx_wpt += ('    <desc>{name}</desc>\n'.format(name=r["name"]))
gpx_wpt += ('  </wpt>\n')

print(gpx_wpt)


# apend to file
# file name : segement_190712.gpx
now = datetime.datetime.now()
filename = now.strftime('segment_%y%m%d.gpx')
#print(filename)

f = open(filename, 'a')
f.write(gpx_wpt)
print("\n --> Written to " + filename)
f.close()
