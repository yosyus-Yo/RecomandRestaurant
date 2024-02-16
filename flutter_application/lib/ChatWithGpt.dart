import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:developer';

Future<String> ChatWithGpt(String input) async {
  final uri = Uri.parse('http://192.168.219.105:8000/main_handler/'); // Django 서버의 URL로 수정
  final headers = {'Content-Type': 'application/json'};
  final body = json.encode({
    'action': 'send_message',
    'message' : input,
  });
  log('body: $body');
  try {
    final response = await http.post(uri, headers: headers, body: body);
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      // Django 서버로부터 받은 데이터를 처리하는 코드
      // 예: showDialog()를 사용하여 화면에 데이터 표시
      log('Server response: $data');
      return data['response'];
    } else {
      // 서버 응답 오류 처리
      log('Server error: ${response.body}');
      return "server error";
    }
  } catch (e) {
    // HTTP 요청 실패 처리
    log('HTTP request failed: $e');
    return "server error";
  }
}