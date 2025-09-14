from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

TOPIC_CHOICES = [
    ('philosophy', 'Философия'),
    ('family', 'Семья'),
    ('state', 'Государство'),
    ('cooking', 'Кулинария'),
    ('love', 'Любовь'),
    ('life', 'Жизнь'),
    ('unknown', 'Не указано')
]

class Quote(models.Model):
    text = models.TextField("Текст цитаты", unique=True, error_messages={"unique":"Такая цитата уже существует"})
    source = models.CharField("Источник", max_length=200)
    topic = models.CharField("Тема", max_length=50, choices=TOPIC_CHOICES, default='unknown')
    weight = models.PositiveIntegerField("Вес", default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.text[:30]}... ({self.source})"

