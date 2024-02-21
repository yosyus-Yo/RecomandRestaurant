import 'dart:async';
import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:flutter_naver_map/flutter_naver_map.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:geolocator/geolocator.dart';

import 'ChatWithGpt.dart';
import 'setOnTapListener .dart';
import 'FindPath.dart';

// 'setOnTapListener.dart'와 'ChatWithGpt.dart'는 사용자가 정의한 파일로 가정합니다.
// 필요한 로직을 해당 파일에 구현하세요.

void main() async {
  await _initialize();
  runApp(const MyApp());
}

Future<void> _initialize() async {
  WidgetsFlutterBinding.ensureInitialized();
  await NaverMapSdk.instance.initialize(
    clientId: '2xj7pkji00',
    onAuthFailed: (e) => log("네이버맵 인증오류 : $e", name: "onAuthFailed"),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MapScreen(),
    );
  }
}

class MapScreen extends StatefulWidget {
  @override
  _MapScreenState createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final Completer<NaverMapController> _controller = Completer();
  bool _showChat = false;
  bool _showRouteMode = false;
  final TextEditingController _startController = TextEditingController(); // 출발지 입력을 위한 컨트롤러
  final TextEditingController _endController = TextEditingController(); // 도착지 입력을 위한 컨트롤러
  final TextEditingController _chatController = TextEditingController();
  final List<String> _messages = [];
  late String _startPoint = "";
  late String _endPoint = "";
  late stt.SpeechToText _speech; // 음성 인식을 위한 객체
  bool _isListening = false; // 현재 음성 인식이 활성화되어 있는지 여부

  @override
  void initState() {
    super.initState();
    requestMicrophonePermission();
    _speech = stt.SpeechToText(); // SpeechToText 인스턴스 초기화
  }

  void requestMicrophonePermission() async {
  var status = await Permission.microphone.request();
  if (status.isGranted) {
    print('마이크 권한 허용됨');
  } else if (status.isDenied) {
    print('마이크 권한 거부됨');
  }
}
    void _startListening() async {
    bool available = await _speech.initialize(
      onStatus: (val) => print('onStatus: $val'),
      onError: (val) => print('onError: $val'),
    );
    if (available) {
      setState(() => _isListening = true);
      _speech.listen(
        onResult: (result) {
          setState(() {
            _chatController.text = result.recognizedWords; // 인식된 단어를 텍스트 필드에 설정
          });
        },
      );
    } else {
      setState(() => _isListening = false);
      _speech.stop();
    }
  }

  void _stopListening() {
    _speech.stop(); // 음성 인식 중지
    setState(() => _isListening = false);
  }


  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        if (_showChat) {
          setState(() {
            _showChat = false; // 채팅창 밖을 탭하면 채팅창 숨김
          });
        }
      },
    child: Scaffold(
      resizeToAvoidBottomInset: false,
      body: Stack(
        children: [
          NaverMap(
            options: const NaverMapViewOptions(
              extent: NLatLngBounds(
                southWest: NLatLng(31.43, 122.37),
                northEast: NLatLng(44.35, 132.0),
              ),
              locale: Locale('ko'),
              indoorEnable: true,
              locationButtonEnable: true,
              consumeSymbolTapEvents: false,
            ),
            onMapTapped: (NPoint point, NLatLng latLng) async {
              final NaverMapController controller = await _controller.future;
              final cameraUpdate = NCameraUpdate.scrollAndZoomTo(
                target: latLng,
              );
              controller.updateCamera(cameraUpdate);
              final marker = NMarker(id: "test", position: latLng);
              final info = await sendCurrentLocationToServer(latLng.latitude, latLng.longitude);
              final onMarkerInfoWindow = NInfoWindow.onMarker(id: marker.info.id, text: info);
              controller.addOverlay(marker);
              marker.openInfoWindow(onMarkerInfoWindow);
              if(_showRouteMode == true)
              {
                _handleMapTap(latLng, info);
                if(_endPoint != "")
                {
                  final response = await FindPath(_startPoint, _endPoint);
                  List<dynamic> _response = response["response"];
                  List<NLatLng> coords = _response.map<NLatLng>((coords) {
                    return NLatLng(coords[1], coords[0]); // NLatLng(latitude, longitude)
                  }).toList();
                  final path = NMultipartPathOverlay(id: "path", paths: [
                      NMultipartPath(coords : coords)
                  ]);
                  controller.addOverlay(path);
                }
              }
              marker.setOnTapListener((NMarker marker) async{
                if(onMarkerInfoWindow.isVisible == true){
                  onMarkerInfoWindow.setIsVisible(false);
                }
                else{
                  onMarkerInfoWindow.setIsVisible(true);
                }
                log("마커 클릭됨", name: "NaverMap");
              });
            },
            onMapReady: (controller) {
              _controller.complete(controller);
              log("Naver Map Ready", name: "NaverMap");
            },
          ),
          _buildSearchBar(),
          if (_showRouteMode) _buildRouteSelection(),
          _buildChatIcon(),
          _buildRouteButton(),
          if (_showChat) _buildChatWindow(),
          _buildChatIcon(),
        ],
      ),
    ),
    );
  }
  // 길찾기 모드 활성화/비활성화를 토글하는 함수
  void _toggleRouteMode() {
    setState(() {
      _showRouteMode = !_showRouteMode;
      
    });
  }

  // 길찾기 버튼 위젯
  Widget _buildRouteButton() {
    return Positioned(
      bottom: 80.0,
      right: 20.0,
      child: FloatingActionButton(
        onPressed: _toggleRouteMode,
        child: Icon(Icons.map),
        backgroundColor: _showRouteMode ? Colors.red : Colors.blue, // 길찾기 모드 활성화 시 버튼 색상 변경
      ),
    );
  }

  // 출발지와 도착지 입력창 위젯
  Widget _buildRouteSelection() {
    return Positioned(
      top: 50.0,
      right: 20.0,
      left: 20.0,
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _startController,
              decoration: InputDecoration(
                hintText: '출발지',
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ),
          SizedBox(width: 10),
          Expanded(
            child: TextField(
              controller: _endController,
              decoration: InputDecoration(
                hintText: '도착지',
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
  void _handleMapTap(NLatLng latLng, String info) {
    if (_showRouteMode == true) { // If search bar is not showing, we're in route selection mode
      setState(() {
        if (_startPoint == "") {
          _startPoint = "${latLng.longitude}, ${latLng.latitude}";
          _startController.text = info;
          log("Start point: $_startPoint", name: "NaverMap");
        } else if (_endPoint == "") {
          _endPoint = "${latLng.longitude}, ${latLng.latitude}";
          _endController.text = info;
        } else {
          // Reset points if both are already set and map is tapped again
          _startPoint = "${latLng.longitude}, ${latLng.latitude}";
          _startController.text = info;
          _endPoint = "";
        }
      });
    }
  }
  Widget _buildSearchBar() {
    return Positioned(
      top: 50.0,
      right: 20.0,
      left: 20.0,
      child: Container(
        padding: EdgeInsets.symmetric(horizontal: 8),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(10),
          boxShadow: [
            BoxShadow(
              color: Colors.black26,
              blurRadius: 4,
              offset: Offset(0, 2),
            ),
          ],
        ),
        child: TextField(
          decoration: InputDecoration(
            icon: Icon(Icons.search),
            hintText: '검색',
            border: InputBorder.none,
          ),
          onSubmitted: (value) {
            // Search functionality here
          },
        ),
      ),
    );
  }

  Widget _buildChatIcon() {
    return Positioned(
      bottom: 20.0,
      right: 20.0,
      child: FloatingActionButton(
        onPressed: () {
          setState(() {
            _showChat = !_showChat;
          });
        },
        child: Icon(Icons.chat),
      ),
    );
  }

  Widget _buildChatWindow() {
  final screenHeight = MediaQuery.of(context).size.height;
  final keyboardHeight = MediaQuery.of(context).viewInsets.bottom;

  return Positioned(
    bottom: keyboardHeight != 0 ? keyboardHeight + 20.0 : 80.0,
    right: 20.0,
    left: 20.0,
    child: Container(
      width: double.infinity,
      height: _showChat ? screenHeight * 0.4 : 0,
      padding: EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(15),
        boxShadow: [
          BoxShadow(
            blurRadius: 8,
            color: Colors.black26,
            spreadRadius: 2,
          ),
        ],
      ),
      child: _showChat ? _chatContent() : Container(),
    ),
  );
}
Widget _chatContent() {
    return Column(
      children: [
        // 채팅 메시지를 보여주는 ListView.builder와 입력 필드 등을 포함하는 UI 구성
        Expanded(
          child: ListView.builder(
              reverse: true,
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                bool isUser = _messages[index].startsWith("User:");
                String messageText = _messages[index].substring(5).trim(); // "User: " 또는 "GPT: " 제거
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    margin: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.lightBlue[100] : Colors.grey[300],
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      messageText,
                      style: TextStyle(fontSize: 16),
                    ),
                  ),
                );
              },
            ),
        ),
        Row(
          children: [
            IconButton(
              icon: Icon(_isListening ? Icons.mic_off : Icons.mic),
              onPressed: _isListening ? _stopListening : _startListening, // 마이크 버튼 클릭 시 음성 인식 시작/중지
            ),
            Expanded(
              child: TextField(
                  controller: _chatController,
                  decoration: InputDecoration(
                    hintText: '메시지 입력...',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(25),
                    ),
                    filled: true,
                    fillColor: Colors.grey[200],
                  ),
                ),
            ),
            IconButton(
              icon: Icon(Icons.send, color: Colors.blue),
                onPressed: () async {
                  if (_chatController.text.isNotEmpty) {
                    String userMessage = _chatController.text.trim();
                    setState(() {
                      _messages.insert(0, "User: $userMessage");
                      _chatController.clear();
                    });
                    // 서버로부터 답변 받아오기
                    String gptResponse = await ChatWithGpt(userMessage); // ChatWithGpt 함수 호출
                    setState(() {
                      _messages.insert(0, "GPT: $gptResponse");
                    });
                  }
                },
            ),
          ],
        ),
      ],
    );
  }
}