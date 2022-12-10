class WordMeaning {
  final String id;
  final String meaning;
  final int selectCount;
  final int priority;

  WordMeaning({required this.id, required this.meaning, required this.selectCount, required this.priority});

  factory WordMeaning.fromJson(Map<String, dynamic> json){

    return WordMeaning(
        id: json['m_id'],
        meaning: json['meaning'],
        selectCount: json['s_count'],
        priority: json['priority']);
  }

  Map<String, dynamic> toJson() =>
      {'m_id': id, 'meaning': meaning, 's_count': selectCount, 'priority': priority};
}