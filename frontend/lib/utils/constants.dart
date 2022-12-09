import 'package:dio/dio.dart';

final String BASE_URL = "http://192.168.40.204:8000";

var options = BaseOptions(
  baseUrl: BASE_URL,
  headers: {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InByaWRla2siLCJ1c2VyX2lkIjoxLCJleHAiOjE2NzA3MDM2NTB9.q5Rk2tjx2DD1j9FCOfujN44loB5tY7nLAB83sfC2yo4111'}
);

Dio dio = Dio(options);

