import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:frontend/utils/constants.dart';

class SearchScreen extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _SearchScreenState();

}

class _SearchScreenState extends State<SearchScreen> {

  bool _tapped = false;
  late TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();

  }

  @override
  void dispose() {
    _controller.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    var top = MediaQuery.of(context).size.height / 3;
    if(_tapped){
      top = 0;
    }

    return
      GestureDetector(
        onTap: (){
          FocusScope.of(context).unfocus();
          setState(() {
            _tapped = false;
          });
        },
        child: Scaffold(
          body: GestureDetector(
            onTap: (){
              FocusScope.of(context).unfocus();
              setState(() {
                _tapped = false;
              });
            },
            child: Stack(
                children: [
                  Positioned(
                    top:top,
                    left:0,
                    right: 0,
                    child: Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: TextField(
                        controller: _controller,
                        decoration: const InputDecoration(
                          prefixIcon: Icon(Icons.search),
                          hintText: 'Type word for searching',
                          labelText: 'Search',
                        ),
                        onTap: (){
                          setState(() {
                            _tapped = true;
                            getWords("r");
                          });
                        },
                      ),

                    ),
                  ),]
            ),
          ),
        ),
      );
  }

}

void getWords(String query) async {
  try {
    var resp = await dio.get("/api/v1/words/search?query=$query");

    print(resp.data);
  }catch(e){

    print(e);
  }


}