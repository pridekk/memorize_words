import 'package:flutter/material.dart';

class BottomNavBar extends StatelessWidget {

  final int index;

  const BottomNavBar({super.key, required this.index});


  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.search),
            label: 'Search',
            backgroundColor: Colors.red,
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.checklist_rtl),
            label: 'Memorize',
            backgroundColor: Colors.green,
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.school),
            label: 'Quiz',
            backgroundColor: Colors.purple,
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.quiz),
            label: 'Settings',
            backgroundColor: Colors.pink,
          ),
        ],
        currentIndex: index,
        selectedItemColor: Colors.amber[800]
    );
  }
}


