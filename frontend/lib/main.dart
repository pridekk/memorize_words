import 'package:flutter/material.dart';
import 'package:frontend/screens/config_screen.dart';
import 'package:frontend/screens/memorize_screen.dart';
import 'package:frontend/screens/quiz_screen.dart';
import 'package:frontend/screens/search_screen.dart';
import 'package:frontend/widgets/bottom_navbar.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _selectedIndex = 0;
  String _title = "검색";

  Widget _selectedWidget = SearchScreen();

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;

      switch(index){
        case 0:
          _selectedWidget = SearchScreen();
          _title = "검색";
          break;
        case 1:
          _selectedWidget = MemorizeScreen();
          _title = "단어암기";
          break;
        case 2:
          _selectedWidget = QuizScreen();
          _title = "Quiz";
          break;
        case 3:
          _selectedWidget = ConfigScreen();
          _title = "설정";
          break;
      }
    });
  }
  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(_title),
      ),
      body: _selectedWidget,

      bottomNavigationBar: BottomNavBar(index:_selectedIndex));
  }
}
