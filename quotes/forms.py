from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'topic', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите текст цитаты...'
            }),
            'source': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Источник цитаты (книга, автор, фильм...)'
            }),
            'topic': forms.Select(attrs={
                'class': 'form-select'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Число от 1 до 10...'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get("source")

        if source:
            count = Quote.objects.filter(source=source).count()
            if count >= 3:
                raise forms.ValidationError("У этого источника уже есть 3 цитаты. Можно добавить не более 3 цитат с одного источника")
        return cleaned_data
