// 마커를 담을 배열입니다
var markers = [];

var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };  

// 지도를 생성합니다    
var map = new kakao.maps.Map(mapContainer, mapOption); 

// 장소 검색 객체를 생성합니다
var ps = new kakao.maps.services.Places();  

// 검색 결과 목록이나 마커를 클릭했을 때 장소명을 표출할 인포윈도우를 생성합니다
var infowindow = new kakao.maps.InfoWindow({zIndex:1});

// 키워드로 장소를 검색합니다
searchPlaces();

// 검색 시 나타낼 장소를 정해줌
var jongam = [
    [37.59236557, 127.0347952, "서울특별시 성북구 종암로 3길 29-17", "서울특별시 성북구 종암동 31-50"],
    [37.59203624, 127.0341879, "서울특별시 성북구 종암로 3길 37-22", "서울특별시 성북구 종암동31-37번지 "],
    [37.59197178, 127.0340189, "서울특별시 성북구 북악산로 27길 24", "서울특별시 성북구 종암동31-36번지 "],
    [37.59169622, 127.033377, "서울특별시 성북구 종암로 5길 96", "서울특별시 성북구 종암동31-61번지 "],
    [37.5927404, 127.0332503, "서울특별시 성북구 종암로 3길 53", "서울특별시 성북구 종암동32-4번지 "],
    [37.5927404, 127.0332503, "서울특별시 성북구 종암로 3길 53", "서울특별시 성북구 종암동32-4번지 "],
    [37.59276891, 127.0334311, "서울특별시 성북구 종암로 3길 47", "서울특별시 성북구 종암동32-8번지 "],
    [37.5931279, 127.0332566, "서울특별시 성북구 종암로 3길 50", "서울특별시 성북구 종암동34-9번지 한일주택 "],
    [37.593616, 127.0323444, "서울특별시 성북구 종암로 9다길 40-25", "서울특별시 성북구 종암동54-442번지 "],
    [37.59370406, 127.0320942, "서울특별시 성북구 종암로 9다길 40-21", "서울특별시 성북구 종암동54-327번지 "],
    [37.59407864, 127.0327235, "서울특별시 성북구 종암로 9다길 37", "서울특별시 성북구 종암동54-311번지 "],
    [37.59649567, 127.032998, "서울특별시 성북구 종암로 13가길 1", "서울특별시 성북구 종암동45-181번지 휴먼팰리스 "],
    [37.59191787, 127.0198086, "서울특별시 성북구 종암로 21다길 14-20", "서울특별시 성북구 "],
    [37.59839761, 127.0319882, "서울특별시 성북구 종암로 19가길 44", "서울특별시 성북구 종암동62-4번지 "],
    [37.5984723, 127.0312058, "서울특별시 성북구 종암로 19가길 32", "서울특별시 성북구 종암동62-15번지 노블레스타운 "],
    [37.59850211, 127.0304467, "서울특별시 성북구 종암로 19가길 10", "서울특별시 성북구 종암동62-29번지 "],
    [37.5977117, 127.0296529, "서울특별시 성북구 종암로 19길 93", "서울특별시 성북구 종암동57-39번지 "],
    [37.59850099, 127.0292123, "서울특별시 성북구 종암로 19길 109", "서울특별시 성북구 종암동125-85번지 "],
    [37.5990212, 127.027824, "서울특별시 성북구 종암로 19다길 30", "서울특별시 성북구 종암동125-59번지 "],
    [37.59866722, 127.0275115, "서울특별시 성북구 종암로 19다길 38", "서울특별시 성북구 종암동125-62번지 "],
    [37.59783835, 127.0275223, "서울특별시 성북구 종암로 19다길 56", "서울특별시 성북구 종암동57-159번지 "],
    [37.59856535, 127.0282716, "서울특별시 성북구 종암로 19라길 26", "서울특별시 성북구 종암동125-32번지 성도아트빌 "],
    [37.5986665, 127.0285194, "서울특별시 성북구 종암로 19라길 14", "서울특별시 성북구 종암동125-35번지 유민아트빌 "],
    [37.59917929, 127.0284221, "서울특별시 성북구 종암로 19라길 5", "서울특별시 성북구 종암동125-20번지 성도아트빌 "],
    [37.59951925, 127.0292218, "서울특별시 성북구 종암로 19다길 1", "서울특별시 성북구 종암동78-80번지 "],
    [37.60045818, 127.0316444, "서울특별시 성북구 종암로 25길 24", "서울특별시 성북구 종암동79-179번지 "],
    [37.60097274, 127.0317623, "서울특별시 성북구 종암로 25길 22-14", "서울특별시 성북구 종암동82-9번지 "],
    [37.60142358, 127.0318018, "서울특별시 성북구 종암로 25길 22-24", "서울특별시 성북구 종암동79-530번지 "],
    [37.60057913, 127.039842, "서울특별시 성북구 월곡로 13길 7", "서울특별시 성북구 종암동112-4번지 "],
    [37.59797676, 127.0389355, "서울특별시 성북구 월곡로 7길 7", "서울특별시 성북구 종암동3-1048번지 "],
    [37.59833952, 127.0381154, "서울특별시 성북구 월곡로 7길 25", "서울특별시 성북구 종암동3-337번지 "],
    [37.59891683, 127.0370888, "서울특별시 성북구 월곡로 7길 45", "서울특별시 성북구 종암동3-301번지 해가온팰리스아파트 "],
    [37.59989877, 127.0370648, "서울특별시 성북구 종암로 24가길 50", "서울특별시 성북구 종암동127번지 SK아파트 "],
    [37.5982374, 127.0399626, "서울특별시 성북구 월곡로 10길 42", "서울특별시 성북구 종암동1-10번지 종암힐스톤 "],
    [37.59649168, 127.0402455, "서울특별시 성북구 월곡로 10길 80", "서울특별시 성북구 종암동3-612번지 "],
    [37.59243149, 127.0373534, "서울특별시 성북구 회기로 3길 24", "서울특별시 성북구 종암동27-2번지 "],
    [37.59246202, 127.0377833, "서울특별시 성북구 회기로 3가길 1-24", "서울특별시 성북구 종암동28-387번지 "],
];

var ha = [
    [37.6037413, 127.0442296, "서울특별시 성북구 월곡로 18가길 57", "서울특별시 성북구 하월곡동13-9번지 "],
    [37.60051465, 127.0430024, "서울특별시 성북구 월곡로 14길 43-2", "서울특별시 성북구 하월곡동40-120번지 "],
    [37.6004186, 127.0422676, "서울특별시 성북구 월곡로 14길 33", "서울특별시 성북구 하월곡동41-31번지 "],
    [37.60092544, 127.0414344, "서울특별시 성북구 월곡로 14길 3", "서울특별시 성북구 하월곡동34-57번지 "],
    [37.60220254, 127.0433659, "서울특별시 성북구 화랑로 14길 64", "서울특별시 성북구 하월곡동38-49번지 "],
    [37.60119101, 127.0430731, "서울특별시 성북구 화랑로 14길 88", "서울특별시 성북구 하월곡동40-6번지 터틀하우스 "],
    [37.60548175, 127.0399603, "서울특별시 성북구 화랑로 5길 69", "서울특별시 성북구 하월곡동222-2번지 "],
    [37.60507881, 127.0402712, "서울특별시 성북구 화랑로 5길 64", "서울특별시 성북구 하월곡동53-12번지 "],
    [37.60471466, 127.0398116, "서울특별시 성북구 화랑로 5길 54", "서울특별시 성북구 하월곡동52-8번지 "],
    [37.60504517, 127.0361379, "서울특별시 성북구 오패산로 3길 36-4", "서울특별시 성북구 하월곡동71-2번지 "],
    [37.60465932, 127.0341269, "서울특별시 성북구 오패산로 3가길 34", "서울특별시 성북구 하월곡동90-1614번지 "],
    [37.60379013, 127.0347157, "서울특별시 성북구 오패산로 1길 39", "서울특별시 성북구 하월곡동90-1838번지 "],
];

var sang = [
    [37.60559367, 127.0493477, "서울특별시 성북구 화랑로 18가길 11-8", "서울특별시 성북구 상월곡동24-191번지 "],
    [37.60441989, 127.0501668, "서울특별시 성북구 화랑로 18가길 51", "서울특별시 성북구 상월곡동24-51번지 한솔아파트 "],
    [37.60564828, 127.0505362, "서울특별시 성북구 화랑로 18길 51", "서울특별시 성북구 상월곡동24-200번지 "],
    [37.60750677, 127.0485872, "서울특별시 성북구 화랑로 19길 7 ", "서울특별시 성북구 상월곡동28-7번지 우남빌라 "],
    [37.60578003, 127.047873, "서울특별시 성북구 화랑로 152 ", "서울특별시 성북구 상월곡동97-22번지 "],
    [37.60554188, 127.0451579, "서울특별시 성북구 화랑로 15길 1", "서울특별시 성북구 "],
    [37.60743948, 127.0469458, "서울특별시 성북구 장월로 1길 9", "서울특별시 성북구 상월곡동46번지 "],
    [37.60615663, 127.0454106, "서울특별시 성북구 장월로 1길 49", "서울특별시 성북구 상월곡동57-1번지 "],
    [37.60877129, 127.0456151, "서울특별시 성북구 장월로1길 28", "서울특별시 성북구 상월곡동101번지 동아에코빌아파트 "],
    [37.60652517, 127.0430728, "서울특별시 성북구 장월로 1마길 46-1", "서울특별시 성북구 상월곡동85-27번지 "],
    [37.60601144, 127.0430567, "서울특별시 성북구 장월로 1마길 40", "서울특별시 성북구 상월곡동78-5번지 "],
];
    
var donam = [
    [37.60071256, 127.0253219, "서울특별시 성북구 정릉로 46길 31", "서울특별시 성북구 "],
    [37.60138076, 127.0254944, "서울특별시 성북구 정릉로 46길 17", "서울특별시 성북구 돈암동625-5번지 "],
    [37.60111491, 127.0249429, "서울특별시 성북구 정릉로 44길 19", "서울특별시 성북구 돈암동627-3번지 구현대3차아파트 "],
    [37.60053877, 127.025007, "서울특별시 성북구 정릉로 44길 37", "서울특별시 성북구 돈암동628번지 "],
    [37.59977765, 127.0212232, "서울특별시 성북구 동소문로 35가길 29", "서울특별시 성북구 돈암동38-19번지 "],
    [37.59913367, 127.0207107, "서울특별시 성북구 동소문로 35가길 47", "서울특별시 성북구 돈암동48-30번지 "],
];

var gileum = [
    [37.61032671, 127.0231465, "서울특별시 성북구 숭인로 2길 28", "서울특별시 성북구 길음동1118-2번지 "],
    [37.61083706, 127.0227548, "서울특별시 성북구 숭인로 2길 14", "서울특별시 성북구 길음동1125-1번지 스위트휴 "],
    [37.60572414, 127.0255397, "서울특별시 성북구 삼양로 2길 22", "서울특별시 성북구 길음동1069번지 "],
    [37.60566411, 127.0248157, "서울특별시 성북구 삼양로 2길 19-5", "서울특별시 성북구 길음동1083번지 대원연립 "],
    [37.60603218, 127.0246523, "서울특별시 성북구 삼양로 4길 11", "서울특별시 성북구 길음동1086-1번지 "],
    [37.60688565, 127.0243467, "서울특별시 성북구 삼양로 4길 33", "서울특별시 성북구 길음동1089번지 "],
    [37.60784713, 127.0240284, "서울특별시 성북구 숭인로 2길 84", "서울특별시 성북구 길음동1094번지 "],
    [37.60896102, 127.0236174, "서울특별시 성북구 숭인로 2길 60", "서울특별시 성북구 길음동1104번지 "],
    [37.60681072, 127.027281, "서울특별시 성북구 삼양로 2길 70", "서울특별시 성북구 길음동1064-1번지 "],
];

var jungreung = [
    [37.61159888, 127.0146691, "서울특별시 성북구 길음로 15가길 29    ", "서울특별시 성북구 정릉동227-21번지 대림파크빌 "],
    [37.61247963, 127.0143969, "서울특별시 성북구 길음로 15가길 53    ", "서울특별시 성북구 정릉동227-185번지 그레이스빌 "],
    [37.60701418, 127.0159413, "서울특별시 성북구 서경로 6길  6    ", "서울특별시 성북구 정릉동192-57번지 쉐누빌 "],
    [37.61127435, 127.0146507, "서울특별시 성북구 서경로 18길 26    ", "서울특별시 성북구 정릉동227-26번지 이안휴빌 "],
    [37.61058308, 127.0149543, "서울특별시 성북구 서경로 18길 10    ", "서울특별시 성북구 정릉동227-160번지 "],
    [37.61090878, 127.0140325, "서울특별시 성북구 서경로 87   ", "서울특별시 성북구 정릉동227-154번지 "],
    [37.6088428, 127.01372, "서울특별시 성북구 서경로 9가길 10   ", "서울특별시 성북구 정릉동218-21번지 한아름빌2차 "],
    [37.6109245, 127.0148365, "서울특별시 성북구 서경로 18길 18   ", "서울특별시 성북구 정릉동227-30번지 "],
    [37.60935028, 127.0129884, "서울특별시 성북구 보국문로 8다길 38   ", "서울특별시 성북구 정릉동221-3번지 "],
    [37.60946674, 127.0129076, "서울특별시 성북구 보국문로 8다길 40  ", "서울특별시 성북구 정릉동226-56번지 "],
    [37.60940568, 127.0120703, "서울특별시 성북구 보국문로 8다길 67   ", "서울특별시 성북구 정릉동226-65번지 "],
    [37.60878401, 127.0131545, "서울특별시 성북구 보국문로 8다길 26   ", "서울특별시 성북구 정릉동206-179번지 온니원쉐르빌 "],
    [37.60196318, 127.0099262, "서울특별시 성북구 아리랑로 19길 70", "서울특별시 성북구 정릉동506번지 "],
    [37.59990088, 127.0111313, "서울특별시 성북구 아리랑로 5길 133", "서울특별시 성북구 정릉동561번지 "],
    [37.60170071, 127.0162604, "서울특별시 성북구 아리랑로 18길 45", "서울특별시 성북구 정릉동16-343번지 "],
    [37.60085635, 127.0111753, "서울특별시 성북구 아리랑로 5길 153", "서울특별시 성북구 정릉동547번지 "],
    [37.6016634, 127.0150264, "서울특별시 성북구 아리랑로 18길 23", "서울특별시 성북구 정릉동112-25번지 "],
    [37.60103118, 127.0202668, "서울특별시 성북구 정릉로 42길 22   ", "서울특별시 성북구 정릉동16-55번지 "],
    [37.60083147, 127.0200882, "서울특별시 성북구 정릉로 42길 28   ", "서울특별시 성북구 정릉동16-70번지 "],
    [37.60738926, 127.0133767, "서울특별시 성북구 정릉로 27길 85   ", "서울특별시 성북구 정릉동203-1번지 풍산그레이스 "],
    [37.60899284, 127.0133443, "서울특별시 성북구 정릉로 27다길 14   ", "서울특별시 성북구 정릉동218-39번지 "],
    [37.60072017, 127.0197047, "서울특별시 성북구 정릉로 42길 38   ", "서울특별시 성북구 정릉동16-411번지 "],
    [37.60069753, 127.0180629, "서울특별시 성북구 정릉로 34길 45   ", "서울특별시 성북구 정릉동16-505번지 삼성그린빌라 "],
    [37.60165937, 127.0177898, "서울특별시 성북구 정릉로 38다길 23   ", "서울특별시 성북구 "],
    [37.59902915, 127.0103274, "서울특별시 성북구 북악산로 3길 40   ", "서울특별시 성북구 "],
    [37.60034604, 127.016969, "서울특별시 성북구 북악산로 825-12   ", "서울특별시 성북구 정릉동968-1번지 "],
    [37.60122193, 127.0171953, "서울특별시 성북구 북악산로 825-44   ", "서울특별시 성북구 정릉동125-6번지 "],
    [37.61241329, 127.0054045, "서울특별시 성북구 솔샘로 17길 26", "서울특별시 성북구 정릉동712-13번지 "],
    [37.6099346, 126.9999669, "서울특별시 성북구 정릉로 9가길 14", "서울특별시 성북구 정릉동885-4번지 "],
    [37.61191683, 127.0020925, "서울특별시 성북구 솔샘로 15길 64-2", "서울특별시 성북구 정릉동727-13번지 영진연립 "],
    [37.61279195, 127.0032927, "서울특별시 성북구 솔샘로 15길 28", "서울특별시 성북구 정릉동735번지 "],
    [37.61054547, 127.0029489, "서울특별시 성북구 솔샘로 5길 52", "서울특별시 성북구 정릉동718-8번지 "],
    [37.6107296, 127.0023461, "서울특별시 성북구 솔샘로 5길 62", "서울특별시 성북구 정릉동727-19번지 "],
    [37.6113636, 127.0027341, "서울특별시 성북구 솔샘로 11길 43-3", "서울특별시 성북구 정릉동716-115번지 "],
    [37.61119558, 127.0031101, "서울특별시 성북구 솔샘로 11길 40", "서울특별시 성북구 정릉동716-116번지 "],
    [37.61003238, 127.004077, "서울특별시 성북구 솔샘로 15다길 49", "서울특별시 성북구 정릉동717-12번지 "],
    [37.61047985, 127.0047846, "서울특별시 성북구 솔샘로 9길 4-3", "서울특별시 성북구 정릉동716-205번지 서광빌라 "],
    [37.60974125, 127.0026765, "서울특별시 성북구 정릉로 15길 47", "서울특별시 성북구 정릉동665-7번지 "],
    [37.60708734, 127.0021003, "서울특별시 성북구 정릉로 12길 18", "서울특별시 성북구 정릉동647-6번지 "],
    [37.60713977, 127.001907, "서울특별시 성북구 정릉로 12길 22", "서울특별시 성북구 정릉동647-7번지 "],
    [37.60637954, 127.0015094, "서울특별시 성북구 정릉로 12길 52", "서울특별시 성북구 정릉동642-2번지 "],
    [37.60547361, 127.0019972, "서울특별시 성북구 정릉로 10가길 62", "서울특별시 성북구 정릉동640-19번지 "],
    [37.60586686, 127.0016182, "서울특별시 성북구 정릉로 10가길 48", "서울특별시 성북구 정릉동640-21번지 한본빌라 "],
    [37.60609652, 127.0000069, "서울특별시 성북구 정릉로 10라길 17", "서울특별시 성북구 정릉동905-8번지 "],
    [37.60460231, 127.0001854, "서울특별시 성북구 정릉로 10라길 50", "서울특별시 성북구 정릉동908번지 에덴빌라 "],
    [37.60634399, 126.9994373, "서울특별시 성북구 정릉로 10라길 5", "서울특별시 성북구 정릉동903-13번지 보광빌라 "],
    [37.60476351, 126.9979409, "서울특별시 성북구 정릉로 10길 120-5", "서울특별시 성북구 정릉동921-8번지 에버빌1차 "],
    [37.60641846, 126.9986549, "서울특별시 성북구 정릉로 10다길 10", "서울특별시 성북구 정릉동898-20번지 "],
    [37.60592675, 126.9969853, "서울특별시 성북구 정릉로 10다길 49", "서울특별시 성북구 정릉동927번지 한전주택 "],
    [37.60813071, 126.9986886, "서울특별시 성북구 정릉로 10길 46", "서울특별시 성북구 정릉동895번지 이화연립주택 "],
    [37.60710963, 126.9962219, "서울특별시 성북구 정릉로 8가길 51", "서울특별시 성북구 정릉동879번지 "],
    [37.60652722, 126.9944856, "서울특별시 성북구 정릉로 8가길 86-4", "서울특별시 성북구 정릉동941-5번지 "],
    [37.60948614, 126.9948988, "서울특별시 성북구 정릉로 6가길 20", "서울특별시 성북구 정릉동955-2번지 "],
    [37.6071059, 127.0032326, "서울특별시 성북구 정릉로 16길 14", "서울특별시 성북구 정릉동649-7번지 "],
    [37.60908723, 127.0106248, "서울특별시 성북구 보국문로 12길 15-6    ", "서울특별시 성북구 정릉동402-71번지 영강하이츠빌라 "],
    [37.6111698, 127.0129191, "서울특별시 성북구 보국문로 8길 109   ", "서울특별시 성북구 정릉동266-402번지 "],
    [37.61318839, 127.0118731, "서울특별시 성북구 보국문로 16다길 49    ", "서울특별시 성북구 정릉동266-35번지 서경하이츠빌라 "],
    [37.61119116, 127.0111632, "서울특별시 성북구 보국문로 18길 42    ", "서울특별시 성북구 정릉동266-172번지 진영빌라 "],
    [37.61123184, 127.0106417, "서울특별시 성북구 보국문로 18길 35    ", "서울특별시 성북구 정릉동266-368번지 "],
    [37.61296826, 127.0081835, "서울특별시 성북구 보국문로 24길 9    ", "서울특별시 성북구 정릉동290-44번지 다오아트빌 "],
    [37.6174428, 127.0056095, "서울특별시 성북구 보국문로 28길 32   ", "서울특별시 성북구 정릉동772-26번지 에덴빌라 "],
    [37.6188457, 126.9999497, "서울특별시 성북구 보국문로 36길 30   ", "서울특별시 성북구 정릉동815-13번지 충신빌라 "],
    [37.61820956, 127.0025069, "서울특별시 성북구 보국문로 32길 26   ", "서울특별시 성북구 정릉동966-24번지 "],
    [37.61621003, 127.0036663, "서울특별시 성북구 보국문로 29길 5  ", "서울특별시 성북구 정릉동770번지 산장연립 "],
    [37.61570642, 127.0016454, "서울특별시 성북구 보국문로 29길 49  ", "서울특별시 성북구 정릉동764-4번지 "],
    [37.61554106, 127.0055441, "서울특별시 성북구 보국문로 137  ", "서울특별시 성북구 정릉동771-59번지 영빈빌라 "],
    [37.61364909, 127.0087861, "서울특별시 성북구 솔샘로 20길 18  ", "서울특별시 성북구 정릉동252-129번지 "],
    [37.61337451, 127.007204, "서울특별시 성북구 솔샘로 73-7 ", "서울특별시 성북구 정릉동293-4번지 "],
    [37.60091619, 127.0107894, "서울특별시 성북구 북악산로 766", "서울특별시 성북구 정릉동545-1번지 "],
    [37.59765251, 127.0051931, "서울특별시 성북구 북악산로 1길 71", "서울특별시 성북구 정릉동508-171번지 "],
    [37.59883264, 127.0051661, "서울특별시 성북구 북악산로 1길 80", "서울특별시 성북구 "],
    [37.59853876, 127.0034373, "서울특별시 성북구 북악산로 1길 118", "서울특별시 성북구 정릉동508-150번지 "],
    [37.5991287, 127.0028746, "서울특별시 성북구 북악산로 1길 134", "서울특별시 성북구 정릉동508-155번지 "],
];

var jangwi = [
    [37.61533633, 127.0429487, "서울특별시 성북구 장위로 17길 16-18", "서울특별시 성북구 장위동229-10번지 중앙클래식하우스 "],
    [37.61527748, 127.0434705, "서울특별시 성북구 장위로 15길 34-24", "서울특별시 성북구 장위동230-64번지 토암트윈스빌 "],
    [37.61472745, 127.0434209, "서울특별시 성북구 장위로 21길 17-14", "서울특별시 성북구 장위동229-5번지 동방라온가 "],
    [37.61428394, 127.0442874, "서울특별시 성북구 장위로 21가길 9", "서울특별시 성북구 장위동225-91번지 성원그린빌 "],
    [37.61412708, 127.0449464, "서울특별시 성북구 장위로 21가길 22", "서울특별시 성북구 장위동225-81번지 "],
    [37.61454184, 127.0460964, "서울특별시 성북구 장위로 29길 11-16", "서울특별시 성북구 장위동225-20번지 "],
    [37.61448608, 127.0470033, "서울특별시 성북구 장위로 29길 14", "서울특별시 성북구 장위동232-13번지 해마루빌4차 "],
    [37.61500241, 127.0462265, "서울특별시 성북구 장위로 21길 60", "서울특별시 성북구 장위동225-13번지 인성하우징 "],
    [37.61640158, 127.0454271, "서울특별시 성북구 장위로 21나길 50", "서울특별시 성북구 장위동219-252번지 삼성쉐르빌 "],
    [37.6156457, 127.04555, "서울특별시 성북구 장위로 21라길 28", "서울특별시 성북구 장위동219-257번지 공간행복 "],
    [37.61569701, 127.0452095, "서울특별시 성북구 장위로 21다길 5-26", "서울특별시 성북구 장위동219-260번지 "],
    [37.61642645, 127.0440448, "서울특별시 성북구 장위로 15길 74-10", "서울특별시 성북구 장위동219-341번지 "],
    [37.61344611, 127.039858, "서울특별시 성북구 장위로 10길 13", "서울특별시 성북구 장위동231-309번지 "],
    [37.61224721, 127.0397941, "서울특별시 성북구 장위로 10길 35", "서울특별시 성북구 장위동231-318번지 도원맨션 "],
    [37.61197195, 127.039186, "서울특별시 성북구 장위로 10길 48", "서울특별시 성북구 장위동231-559번지 장계빌라 "],
    [37.61298038, 127.0413138, "서울특별시 성북구 장위로 16길 27", "서울특별시 성북구 장위동231-116번지 "],
    [37.61193629, 127.0414518, "서울특별시 성북구 장위로 4길 80", "서울특별시 성북구 장위동231-297번지 "],
    [37.61181787, 127.0424048, "서울특별시 성북구 장위로 16길 67", "서울특별시 성북구 장위동231-539번지 "],
    [37.61217096, 127.0437254, "서울특별시 성북구 장위로 22길 40", "서울특별시 성북구 장위동233-378번지 "],
    [37.61177433, 127.0448179, "서울특별시 성북구 장위로 24길 46", "서울특별시 성북구 장위동233-357번지 "],
    [37.6126032, 127.0448073, "서울특별시 성북구 장위로 24길 48", "서울특별시 성북구 장위동 233-167번지"],
    [37.61131919, 127.0464773, "서울특별시 성북구 장월로 9나길 11-14", "서울특별시 성북구 장위동246-398번지 "],
    [37.60866949, 127.0463979, "서울특별시 성북구 장월로 3길 22", "서울특별시 성북구 장위동246-268번지 "],
    [37.61179559, 127.0463353, "서울특별시 성북구 장월로 11길 65-13", "서울특별시 성북구 장위동233-512번지 "],
    [37.61198406, 127.0462423, "서울특별시 성북구 장월로 11길 39-14", "서울특별시 성북구 장위동233-145번지 "],
    [37.61219311, 127.0464662, "서울특별시 성북구 장월로 11길 39-8", "서울특별시 성북구 장위동233-519번지 "],
    [37.61237162, 127.0484914, "서울특별시 성북구 장월로 11길  9", "서울특별시 성북구 장위동233-41번지 "],
    [37.6126549, 127.0478648, "서울특별시 성북구 장위로 32길 24", "서울특별시 성북구 장위동233-76번지 "],
    [37.61274135, 127.0474106, "서울특별시 성북구 장위로 30길 24", "서울특별시 성북구 장위동233-86번지 대성아트빌 "],
    [37.61319233, 127.0463515, "서울특별시 성북구 장위로 26길 17-13", "서울특별시 성북구 장위동233-532번지 "],
    [37.61300569, 127.046671, "서울특별시 성북구 장위로 26길 17-23", "서울특별시 성북구 장위동233-99번지 "],
    [37.6113639, 127.0475528, "서울특별시 성북구 장월로 9길 13", "서울특별시 성북구 장위동246-303번지 장위아띠끄빌 "],
    [37.60987889, 127.0477642, "서울특별시 성북구 장월로 44", "서울특별시 성북구 장위동246-122번지 "],
    [37.59191787, 127.0198086, "서울특별시 성북구울 장월로 40", "서울특별시 성북구 장위동 246-15번지"],
    [37.60999081, 127.0471172, "서울특별시 성북구 장월로 5길 43", "서울특별시 성북구 장위동246-149번지 그린빌라 "],
    [37.61077258, 127.0490894, "서울특별시 성북구 장월로 56-23", "서울특별시 성북구 장위동68-1205번지 "],
    [37.59191787, 127.0198086, "서울특별시 성북구 장월로 49길 18", "서울특별시 성북구 장위동 246-118번지"],
    [37.59191787, 127.0198086, "서울특별시 성북구 장월로 49길 17", "서울특별시 성북구 장위동 장위동 246-118 번지"],
    [37.59191787, 127.0198086, "서울특별시 성북구 장월로 49길 16", "서울특별시 성북구 장위동 246-118번지"],
];
    
var seokgwan = [
    [37.60604073, 127.0601807, "서울특별시 성북구 돌곶이로 9나길 12", "서울특별시 성북구 석관동332-155번지 "],
    [37.60939993, 127.0599686, "서울특별시 성북구 돌곶이로 22가길 5", "서울특별시 성북구 석관동"],
    [37.61142121, 127.0603396, "서울특별시 성북구 한천로 81길 23", "서울특별시 성북구 석관동192-37번지 "],
    [37.60824715, 127.0645814, "서울특별시 성북구 한천로 69길 10-2", "서울특별시 성북구 석관동65-76번지 "],
    [37.6115033, 127.0661491, "서울특별시 성북구 한천로 76다길 4-7", "서울특별시 성북구 석관동118-42번지 "],
    [37.61347164, 127.0655242, "서울특별시 성북구 한천로 66길 203", "서울특별시 성북구 석관동134-2번지 "],
    [37.61386658, 127.064194, "서울특별시 성북구 화랑로 42길 36", "서울특별시 성북구 석관동168-61번지 "],
];

var dongsomun = [
    [37.58811039, 127.0073241, "서울특별시 성북구 동소문로 2길 15", "서울특별시 성북구 동소문동2가76번지 "],
    [37.59067336, 127.0088753, "서울특별시 성북구 동소문로 7길 16", "서울특별시 성북구 동소문동4가97-1번지 "],
    [37.59097512, 127.0083278, "서울특별시 성북구 동소문로 3길 68", "서울특별시 성북구 동소문동1가129번지 삼선파크빌 "],
    [37.5909736, 127.0081467, "서울특별시 성북구 동소문로 25-30", "서울특별시 성북구 동소문동1가130번지 "],
    [37.59070985, 127.0078558, "서울특별시 성북구 동소문로 3길 54", "서울특별시 성북구 동소문동1가55-1번지 광국빌라 "],
    [37.58966569, 127.0069071, "서울특별시 성북구 동소문로 3길 26", "서울특별시 성북구 동소문동1가45-1번지 "],
];

var samsun = [
    [37.58697003, 127.01642, "서울특별시 성북구 보문로 29나길 1", "서울특별시 성북구 삼선동5가151-6번지 "],
    [37.58813688, 127.0147968, "서울특별시 성북구 보문로 31길 36", "서울특별시 성북구 삼선동5가66-11번지 "],
    [37.59094013, 127.0149185, "서울특별시 성북구 보문로 36길 12", "서울특별시 성북구 삼선동4가350-6번지 "],
    [37.58880944, 127.0122516, "서울특별시 성북구 삼선교로 18길 5", "서울특별시 성북구 삼선동3가6번지 "],
    [37.58763702, 127.0056772, "서울특별시 성북구 삼선교로 2길 15", "서울특별시 성북구 삼선동1가11-2번지 "],
    [37.58738508, 127.0067902, "서울특별시 성북구 삼선교로 4길 10", "서울특별시 성북구 삼선동1가16-7번지 "],
    [37.58565168, 127.0074586, "서울특별시 성북구 삼선교로 4길 47-1", "서울특별시 성북구 삼선동1가216-6번지 "],
    [37.58291339, 127.0075628, "서울특별시 성북구 삼선교로 4길 115", "서울특별시 성북구 삼선동1가290-28번지 "],
    [37.58251566, 127.0084852, "서울특별시 성북구 삼선교로 4길 133", "서울특별시 성북구 삼선동1가291-15번지 "],
    [37.58138684, 127.0092587, "서울특별시 성북구 삼선교로 4길 162", "서울특별시 성북구 삼선동1가302-7번지 "],
    [37.58536748, 127.0111761, "서울특별시 성북구 삼선교로 16길 67", "서울특별시 성북구 삼선동2가232번지 "],
    [37.58548612, 127.0102801, "서울특별시 성북구 삼선교로 14길 58", "서울특별시 성북구 삼선동2가203-1번지 타임아트빌 "],
    [37.58566915, 127.0084661, "서울특별시 성북구 삼선교로 10다길 28", "서울특별시 성북구 삼선동1가246번지 "],
    [37.58422272, 127.0089721, "서울특별시 성북구 삼선교로 10다길 59", "서울특별시 성북구 삼선동1가288번지 "],
    [37.58520169, 127.0075212, "서울특별시 성북구 삼선교로 8길 56", "서울특별시 성북구 삼선동1가224번지 "],
    [37.58763488, 127.0172718, "서울특별시 성북구 보문로 29길 10", "서울특별시 성북구 삼선동5가242번지 "],
];

var seongbuk = [
    [37.60028779, 126.9950451, "서울특별시 성북구 선잠로 101", "서울특별시 성북구 성북동15-24번지 "],
    [37.59754182, 126.9974261, "서울특별시 성북구 선잠로 96-1", "서울특별시 성북구 성북동 "],
    [37.59977394, 126.9971357, "서울특별시 성북구 선잠로 84", "서울특별시 성북구 성북동15-68번지 "],
    [37.59818216, 126.9974968, "서울특별시 성북구 선잠로 66", "서울특별시 성북구 성북동9-11번지 "],
    [37.59754182, 126.9974261, "서울특별시 성북구 선잠로 76-1", "서울특별시 성북구 "],
    [37.60139091, 126.9965591, "서울특별시 성북구 대사관로 152", "서울특별시 성북구 성북동15-29번지 "],
    [37.59731332, 126.9885849, "서울특별시 성북구 대사관로 7길 31", "서울특별시 성북구 성북동330-379번지 "],
    [37.59818625, 126.989513, "서울특별시 성북구 대사관로 11길 31", "서울특별시 성북구 성북동330-255번지 "],
    [37.59876779, 126.9890295, "서울특별시 성북구 대사관로 13길 123", "서울특별시 성북구 성북동330-267번지 "],
    [37.59244244, 126.9911306, "서울특별시 성북구 성북로 23길 137", "서울특별시 성북구 성북동217-119번지 "],
    [37.59425274, 127.0016486, "서울특별시 성북구 성북로 14가길 5", "서울특별시 성북구 성북동145-177번지 "],
    [37.5944193, 127.0021673, "서울특별시 성북구 성북로 14가길 17", "서울특별시 성북구 성북동145-34번지 "],
    [37.59337947, 127.002804, "서울특별시 성북구 성북로 12길 11-14", "서울특별시 성북구 성북동164-1번지 팔복빌라 "],
    [37.59754182, 126.9974261, "서울특별시 성북구 선잠로 34-1", "서울특별시 성북구 "],
    [37.59509377, 126.9977533, "서울특별시 성북구 선잠로 27", "서울특별시 성북구 성북동75-17번지 "],
    [37.59533997, 126.9938546, "서울특별시 성북구 성북로 28길 14", "서울특별시 성북구 성북동253-2번지 "],
    [37.59595641, 126.9932348, "서울특별시 성북구 성북로 26길 43", "서울특별시 성북구 성북동300-3번지 "],
    [37.59661664, 126.9924672, "서울특별시 성북구 성북로 28길 50", "서울특별시 성북구 성북동300-5번지 "],
    [37.59576663, 126.9931694, "서울특별시 성북구 성북로 28길 27", "서울특별시 성북구 성북동260-65번지 "],
    [37.59460538, 126.9890744, "서울특별시 성북구 성북로 31길 48 (1)", "서울특별시 성북구 성북동349-1번지 사보이빌라 1호"],
];

var bomun = [
    [37.5861653, 127.0171666, "서울특별시 성북구 지봉로 21길 32", "서울특별시 성북구 보문동2가53번지 "],
    [37.58594468, 127.0177243, "서울특별시 성북구 보문로 25길 19", "서울특별시 성북구 보문동2가64-4번지 "],
    [37.58284235, 127.0184783, "서울특별시 성북구 보문로 21길 38", "서울특별시 성북구 보문동6가10번지 "],
    [37.58388227, 127.0178419, "서울특별시 성북구 보문사길 39", "서울특별시 성북구 보문동3가207-2번지 베쏘하우스 "],
];

var anam = [
    [37.58582419, 127.0216661, "서울특별시 성북구 고려대로 10길 3", "서울특별시 성북구 안암동2가141-12번지 "],
    [37.58446808, 127.0222046, "서울특별시 성북구 고려대로 10길 37", "서울특별시 성북구 안암동3가41-1번지 "],
    [37.58327017, 127.0233525, "서울특별시 성북구 고려대로 12길 69    ", "서울특별시 성북구 안암동3가133-4번지 "],
    [37.5845636, 127.0228601, "서울특별시 성북구 고려대로 14길 44    ", "서울특별시 성북구 안암동3가55-9번지 "],
    [37.58525188, 127.0287501, "서울특별시 성북구 고려대로 22길 41    ", "서울특별시 성북구 안암동"],
    [37.57958377, 127.0243063, "서울특별시 성북구 안암로 5길 8   ", "서울특별시 성북구 안암동4가41-39번지 "],
    [37.58181484, 127.023881, "서울특별시 성북구 안암로 9길 49  ", "서울특별시 성북구 안암동3가130-13번지 "],
    [37.5839954, 127.0304534, "서울특별시 성북구 안암로 89-3", "서울특별시 성북구 안암동5가104-17번지 "],
    [37.58265781, 127.028863, "서울특별시 성북구 안암로 69-1 ", "서울특별시 성북구 안암동5가134-35번지 "],
    [37.5808657, 127.0224215, "서울특별시 성북구 안암로 1길   ", "서울특별시 성북구 안암동 "],
    [37.59007233, 127.0298312, "서울특별시 성북구 개운사길 76-1 ", "서울특별시 성북구 안암동5가10-1번지 "]
    ];

// 키워드 검색을 요청하는 함수입니다
function searchPlaces() {

    var keyword = document.getElementById('keyword').value.trim();
// trim(): 문자열 양끝의 공백 제거하고 새로운 문자열 반환
    // 특정 키워드를 검색할 때 고정된 장소 정보를 표시합니다.
    if (keyword === '종암동'|| keyword === '종암') {
        displayFixedPlaces(jongam);
    }else if (keyword === '하월곡동' || keyword === '하월곡'){
        displayFixedPlaces(ha);
    }else if (keyword === '상월곡동' || keyword === '상월곡'){
        displayFixedPlaces(sang);
    }else if (keyword === '돈암동'|| keyword === '돈암'){
        displayFixedPlaces(donam);
    }else if (keyword === '길음동'|| keyword === '길음'){
        displayFixedPlaces(gileum);
    }else if (keyword === '정릉동'|| keyword === '정릉'){
        displayFixedPlaces(jungreung);
    }else if (keyword === '장위동'|| keyword === '장위'){
        displayFixedPlaces(jangwi);
    }else if (keyword === '석관동'|| keyword === '석관'){
        displayFixedPlaces(seokgwan);
    }else if (keyword === '동소문동'|| keyword === '동소문'){
        displayFixedPlaces(dongsomun);
    }else if (keyword === '삼선동'|| keyword === '삼선'){
        displayFixedPlaces(samsun);
    }else if (keyword === '성북동'){
        displayFixedPlaces(seongbuk);
    }else if (keyword === '보문동'|| keyword === '보문'){
        displayFixedPlaces(bomun);
    }else if (keyword === '안암동'|| keyword === '안암'){
        displayFixedPlaces(anam);
}
}

function displayFixedPlaces(places) {
    var listEl = document.getElementById('placesList'),
        menuEl = document.getElementById('menu_wrap'),
        fragment = document.createDocumentFragment(),
        bounds = new kakao.maps.LatLngBounds();

    // 검색 결과 목록에 추가된 항목들을 제거합니다
    removeAllChildNods(listEl);

    // 지도에 표시되고 있는 마커를 제거합니다
    removeMarker();

    for (var i = 0; i < places.length; i++) {
        var placePosition = new kakao.maps.LatLng(places[i][0], places[i][1]),
            marker = addMarker(placePosition, i),
            itemEl = getFixedListItem(i, places[i]);

        bounds.extend(placePosition);

        (function(marker, title) {
            kakao.maps.event.addListener(marker, 'mouseover', function() {
                displayInfowindow(marker, title);
            });

            kakao.maps.event.addListener(marker, 'mouseout', function() {
                infowindow.close();
            });

            itemEl.onmouseover = function() {
                displayInfowindow(marker, title);
            };

            itemEl.onmouseout = function() {
                infowindow.close();
            };
        })(marker, places[i][2]);

        fragment.appendChild(itemEl);
    }

    // 검색결과 항목들을 검색결과 목록 Element에 추가합니다
    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;

    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.setBounds(bounds);
}

// 검색결과 항목을 Element로 반환하는 함수입니다 (고정된 장소용)
function getFixedListItem(index, place) {
    var el = document.createElement('li'),
    markerIndex = (index % 15) + 1,
        itemStr = '<span class="markerbg marker_' + (index + 1) + '"></span>' +
                  '<div class="info">' +
            '   <h5>' + place[2] + '</h5>' +
            '   <span>' + place[3] + '</span>' +
            '</div>';

    el.innerHTML = itemStr;
    el.className = 'item';

    // 클릭 이벤트 리스너 추가
    el.onclick = function() {
        var marker = markers[index];
        var position = new kakao.maps.LatLng(place[0], place[1]);
        map.setCenter(position);
        displayInfowindow(marker, place[2]);
    };

    return el;
}
// 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {

        // 정상적으로 검색이 완료됐으면
        // 검색 목록과 마커를 표출합니다
        displayPlaces(data);

        // 페이지 번호를 표출합니다
        displayPagination(pagination);

    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

        alert('검색 결과가 존재하지 않습니다.');
        return;

    } else if (status === kakao.maps.services.Status.ERROR) {

        alert('검색 결과 중 오류가 발생했습니다.');
        return;

    }
}

// 검색 결과 목록과 마커를 표출하는 함수입니다
function displayPlaces(places) {

    var listEl = document.getElementById('placesList'), 
    menuEl = document.getElementById('menu_wrap'),
    fragment = document.createDocumentFragment(), 
    bounds = new kakao.maps.LatLngBounds(), 
    listStr = '';
    
    // 검색 결과 목록에 추가된 항목들을 제거합니다
    removeAllChildNods(listEl);

    // 지도에 표시되고 있는 마커를 제거합니다
    removeMarker();
    
    for ( var i=0; i<places.length; i++ ) {

        // 마커를 생성하고 지도에 표시합니다
        var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
            marker = addMarker(placePosition, i), 
            itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        bounds.extend(placePosition);

        // 마커와 검색결과 항목에 mouseover 했을때
        // 해당 장소에 인포윈도우에 장소명을 표시합니다
        // mouseout 했을 때는 인포윈도우를 닫습니다
        (function(marker, title) {
            kakao.maps.event.addListener(marker, 'mouseover', function() {
                displayInfowindow(marker, title);
            });

            kakao.maps.event.addListener(marker, 'mouseout', function() {
                infowindow.close();
            });

            itemEl.onmouseover =  function () {
                displayInfowindow(marker, title);
            };

            itemEl.onmouseout =  function () {
                infowindow.close();
            };
        })(marker, places[i].place_name);

        fragment.appendChild(itemEl);
    }

    // 검색결과 항목들을 검색결과 목록 Element에 추가합니다
    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;

    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.setBounds(bounds);
}

// 검색결과 항목을 Element로 반환하는 함수입니다
function getListItem(index, places) {

    var el = document.createElement('li'),
    itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                '<div class="info">' +
                '   <h5>' + places.place_name + '</h5>';

    if (places.road_address_name) {
        itemStr += '    <span>' + places.road_address_name + '</span>' +
                    '   <span class="jibun gray">' +  places.address_name  + '</span>';
    } else {
        itemStr += '    <span>' +  places.address_name  + '</span>'; 
    }
                 
      itemStr += '  <span class="tel">' + places.phone  + '</span>' +
                '</div>';           

    el.innerHTML = itemStr;
    el.className = 'item';

    return el;
}

function addMarker(position, title) {
    // 마커 이미지의 이미지 소스 URL
    var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";
    
    // 마커 이미지의 이미지 크기
    var imageSize = new kakao.maps.Size(24, 35); 
    
    // 마커 이미지를 생성
    var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
    
    // 마커를 생성
    var marker = new kakao.maps.Marker({
        position: position, 
        image: markerImage, 
        title: title
    });

    // 마커를 지도에 표시
    marker.setMap(map); 
    markers.push(marker);  

    return marker;
}


// 지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeMarker() {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    markers = [];
}

// 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
function displayPagination(pagination) {
    var paginationEl = document.getElementById('pagination'),
        fragment = document.createDocumentFragment(),
        i; 

    // 기존에 추가된 페이지번호를 삭제합니다
    while (paginationEl.hasChildNodes()) {
        paginationEl.removeChild (paginationEl.lastChild);
    }

    for (i=1; i<=pagination.last; i++) {
        var el = document.createElement('a');
        el.href = "#";
        el.innerHTML = i;

        if (i===pagination.current) {
            el.className = 'on';
        } else {
            el.onclick = (function(i) {
                return function() {
                    pagination.gotoPage(i);
                }
            })(i);
        }

        fragment.appendChild(el);
    }
    paginationEl.appendChild(fragment);
}

// 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
// 인포윈도우에 장소명을 표시합니다
function displayInfowindow(marker, title) {
    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    infowindow.setContent(content);
    infowindow.open(map, marker);
}

 // 검색결과 목록의 자식 Element를 제거하는 함수입니다
function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}