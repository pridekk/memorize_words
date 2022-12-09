class SearchWord {
  final String id;
  final int selectCount;
  final int priority;

  SearchWord({required this.id, required this.selectCount, required this.priority});

  factory SearchWord.fromJson(Map<String, dynamic> json){

    return SearchWord(
        id: json['_id'],
        selectCount: json['s_count'],
        priority: json['priority']);
  }

  Map<String, dynamic> toJson() =>
      {'_id': id, 's_count': selectCount, 'priority': priority};
}