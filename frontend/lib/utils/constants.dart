import 'package:dio/dio.dart';

final String BASE_URL = "http://localhost:8000";

var options = BaseOptions(
  baseUrl: BASE_URL,
);

Dio dio = Dio(options);

