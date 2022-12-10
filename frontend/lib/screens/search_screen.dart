import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:frontend/models/search_word.dart';
import 'package:frontend/utils/constants.dart';

import '../models/word_meaning.dart';

class SearchScreen extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _SearchScreenState();

}

class _SearchScreenState extends State<SearchScreen> {

  bool _tapped = false;
  bool _meaning = false;
  late TextEditingController _controller;
  late ScrollController _scrollController;
  late List<SearchWord> items;
  var searchText = '';
  late List<WordMeaning> meanings;
  var currentPage = 1;
  var moreData = true;
  var size = 10;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _scrollController = ScrollController();
    _scrollController.addListener(onScroll);

    items = [];
    meanings = [];

  }

  void onScroll() async {
    if(_scrollController.position.pixels == _scrollController.position.maxScrollExtent){
      if(moreData){
        var data = await getWords(searchText, ++currentPage, size);

        if(data.isNotEmpty){
          setState(() {
            items += data;
          });
          print("items: ${items.length}");

        } else {
          setState((){
            moreData = false;
          });
        }

      }
    }
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
            searchText = '';
          });
        },
        child: Scaffold(
          body: GestureDetector(
            onTap: (){
              FocusScope.of(context).unfocus();
              setState(() {
                _tapped = false;
                items = [];
              });
            },

            child:

              Container(

              alignment: Alignment.center,
              child:

              Column(
                  mainAxisAlignment:  MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _controller,

                        decoration: const InputDecoration(
                          prefixIcon: Icon(Icons.search),
                          hintText: 'Type word for searching',

                        ),
                        onTap: (){
                          setState(() {
                            _tapped = true;
                          });
                        },
                        onChanged: (text) async {
                          List<SearchWord> words = [];
                          if(text.isNotEmpty){
                            words = await getWords(text, 1, size);
                          }
                          setState(() {
                            searchText = text;
                            items = words;
                            currentPage = 1;
                            if(items.isNotEmpty){
                              moreData = true;
                            }
                          });
                        },
                      ),
                    ),
                    if(items.isNotEmpty && _tapped == true && _meaning == false)
                    Expanded(
                      flex: 9,
                      child: RefreshIndicator(
                        onRefresh: () async {

                          var addedWords = await getWords(searchText, ++currentPage, size);

                          if(addedWords.isNotEmpty){
                            setState(() {
                              items += addedWords;
                            });
                          }
                        },
                        child: ListView.builder(
                          controller: _scrollController,
                          scrollDirection: Axis.vertical,
                          shrinkWrap: true,
                          itemCount: items.length,
                          itemBuilder: (context, index){
                            return ListTile(
                              title: GestureDetector(
                                  onTap: () async {
                                    var meanings = await getMeaning(items[index].id, 1, size);
                                    setState(() {
                                      _meaning = true;
                                    });
                                  },
                                  child: Text(items[index].id)
                              )
                            );
                          },
                        ),
                      ),
                    ),
                  ]
              ),
            ),
          ),
        ),
      );
  }

  Future<List<SearchWord>> getWords(String query, int page, int size) async {

      var resp = await dio.get("/api/v1/words?query=$query&page=$page&size=$size");

      return (resp.data).map<SearchWord>((json) {
          return SearchWord.fromJson(json);
        }).toList();

  }

  Future<List<WordMeaning>> getMeaning(String query, int page, int size) async{

    var resp = await dio.get("/api/v1/words/$query/meanings/?page=$page&size=$size");

    return (resp.data).map<WordMeaning>((json){
      return WordMeaning.fromJson(json);
    }).toList();
  }

}
