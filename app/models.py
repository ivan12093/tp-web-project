from django.db import models

# Create your models here.
ANSWERS = [
    {'question_id': i,
     'text': f'Answer{i}',
     'author': f'Author{i}',
     'likes': i,
     'is_correct': i % 2 == 0,
     }
    for i in range(1, 10)
]

QUESTIONS = {
    'questions': [
        {
            'id': i,
            'title': f'Question #{i}',
            'text': f'Question text #{i}',
            'author': f'Author #{i}',
            'answers_number': i,
            'tags': [f'tag{k}' for k in range(i)],
            'likes': i,
            'answers': [answer for answer in ANSWERS if answer['question_id'] == i]
        }
        for i in range(1, 10)
    ],
}
