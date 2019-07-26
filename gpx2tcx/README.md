# README #

GPX to TCX file converter
GPX 파일을 TCX 파일로 변환하는 프로그램

라이센스는 GPLv2 입니다.

직접 소스를 수정해서 gpx 파일 경로명을 지정하시고 실행하시면 됩니다.

버추얼 파트너의 속도 지정이 가능합니다.
do_job() 함수의 두 번째 인자로 속도를 지정하시면 됩니다.
기본 값은 20(km/hr)입니다.

waypoint에 아이콘을 지정할 수 있습니다.
아이콘은 다음 16가지 입니다.
["Generic", "Summit", "Valley", "Water", "Food", "Danger", "Left", "Right", "Straight", "First Aid", "4th Category", "3rd Category", "2nd Category", "1st Category", "Hors Category", "Sprint" ]

지정 방븝은 다음과 같습니다.
1. 2. 3. ... Generic
s벗고개, s선어치, s정령치... Summit
c1, c2, c3, c4, ch, cs : category 1, 2, 3, 4, hors, sprint
mG, mS, mV, mW, mF, mD : Generic, Summit, Valley, Water, Food, Danger
mL, mR, mC, mA : Left, Right, Straight, First Aid
앞에 위에 해당하는 첨자가 없음 : Generic

tcx 파일로 변환시 앞첨자는 모두 삭제후 해당 아이콘으로 대치됩니다.
또한 waypoint 명칭 뒤쪽에 _, _x, _xy 등의 첨자가 붙음 경우 역시 삭제후 표기됩니다.
(고도표 프로그램과의 호환을 위해서)

저장되는 파일명은 인자로 지정한 파일명에서 확장자만 .tcx로 바뀌어서 python이 실행되는 폴더로 저장됩니다.
ex) do_job('D:/SRC/python/GPX2TCX/sample.gpx', 25)
    일 경우
	sample.tcx
	로 저장됨
	
역시, 프로그램과 관련하여 궁금한 점이 있으시면 구글링을...

란도너스에 관련한 궁금증은
	http://www.korearandonneurs.kr/
	http://www.audax-club-parisien.com/EN/index.php
	https://rusa.org/
	https://www.audax-japan.org/en/audax-japan/
	http://app.audaxthailand.com/home
	 
	즐거운 라이딩 되세요 !!!
