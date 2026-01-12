import 'package:http/http.dart' as http;

Future<(bool, String)> fetchUrl(String url) async {
  try {
    var response = await http.get(Uri.parse(url));
    return (true, response.body);
  } catch (e) {
    return (false, e.toString());
  }
}
