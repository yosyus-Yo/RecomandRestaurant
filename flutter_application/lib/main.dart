import 'dart:async';
import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:flutter_naver_map/flutter_naver_map.dart';

import 'setOnTapListener .dart';
import 'ChatWithGpt.dart';

void main() async {
  await _initialize();
  runApp(const MyApp()); // NaverMapApp 대신 MyApp을 사용
}

// 지도 초기화하기
Future<void> _initialize() async {
  WidgetsFlutterBinding.ensureInitialized();
  await NaverMapSdk.instance.initialize(
    clientId: '2xj7pkji00', // 클라이언트 ID 설정
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
  final TextEditingController _chatController = TextEditingController();
  final List<String> _messages = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
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
              // minZoom: 10, // default is 0
              // maxZoom: 16, // default is 21
              // maxTilt: 30,
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
              marker.setOnTapListener((NMarker marker) async{
                onMarkerInfoWindow.close();
                log("마커 클릭됨", name: "NaverMap");
              });
            },
            onMapReady: (controller) {
              _controller.complete(controller);
              log("Naver Map Ready", name: "NaverMap");
            },
          ),
          Positioned(
            top: 50.0,
            right: 20.0,
            left: 20.0, // 검색 창을 화면 상단 가로 전체에 걸쳐 배치
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
                  // 여기에 검색 기능 구현
                },
              ),
            ),
          ),

          // 채팅 아이콘
          Positioned(
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
          ),

          // 채팅 창
          if (_showChat)
            Positioned(
              bottom: 80.0,
              right: 20.0,
              child: Container(
                width: 300,
                height: 400,
                padding: EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(8),
                  boxShadow: [
                    BoxShadow(
                      blurRadius: 8,
                      color: Colors.black26,
                      spreadRadius: 2,
                    ),
                  ],
                ),
                child: Column(
                  children: [
                    Expanded(
                      child: ListView.builder(
                        itemCount: _messages.length,
                        itemBuilder: (context, index) => ListTile(
                          title: Text(_messages[index]),
                        ),
                      ),
                    ),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: _chatController,
                            decoration: InputDecoration(
                              hintText: '메시지 입력...',
                              border: OutlineInputBorder(),
                            ),
                          ),
                        ),
                        IconButton(
                          icon: Icon(Icons.send),
                          onPressed: () async {// 비동기 함수로 변경
                            String userMessage = "";
                            setState(() {
                              if (_chatController.text.isNotEmpty) {
                                // 사용자 메시지 추가
                                String userMessage = _chatController.text;
                                _messages.add("User: $userMessage");
                                _chatController.clear();
                              }
                            });
                            // 서버로부터 답변 받아오기
                            if (userMessage.isNotEmpty) {
                              String gptResponse = await ChatWithGpt(userMessage); // ChatWithGpt 함수 호출
                              setState(() {
                                // GPT 응답을 채팅 목록에 추가
                                _messages.add("GPT: $gptResponse");
                              });
                            }
                          },
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}