from django.forms import ModelForm
from django.forms.widgets import Textarea
from mainapp.models import Review, Message


class ReviewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Review
        fields = ['content']
        widgets = {'content': Textarea}


class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Message
        fields = ['text']
        widgets = {'text': Textarea}
