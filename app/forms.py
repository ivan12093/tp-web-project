from itertools import chain

from django import forms
from django.core.exceptions import ValidationError

from app.models import User, Question, Tag, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).first():
            raise ValidationError('User with this username already exists!')
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).first():
            raise ValidationError('User with this email already exists.')
        return self.cleaned_data['email']

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )
        user.save()


class UpdateUserForm(forms.ModelForm):
    current_password = forms.CharField(label='Enter current password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'avatar']

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exclude(username=self.instance.username).first():
            raise ValidationError('User with this username already exists!')
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exclude(email=self.instance.email).first():
            raise ValidationError('User with this email already exists.')
        return self.cleaned_data['email']

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise ValidationError('Wrong password!')
        return self.cleaned_data['current_password']

    def save(self):
        print(self.instance.email, self.instance.username, self.instance.password)
        self.instance.email = self.cleaned_data['email']
        self.instance.username = self.cleaned_data['username']
        if self.cleaned_data['password']:
            print(f'Password - {self.cleaned_data["password"]}')
            self.instance.set_password(self.cleaned_data['password'])
        self.instance.save()


class CreateQuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def save(self, user: User) -> Question:
        question = Question(
            title=self.cleaned_data['title'],
            text=self.cleaned_data['text'],
            author=user
        )
        question.save()

        tags_splitted = set(self.cleaned_data['tags'].split())
        old_tags = []
        new_tags = []
        for tag in tags_splitted:
            tag_db_obj = Tag.objects.filter(name=tag).first()
            if not tag_db_obj:
                tag_db_obj = Tag(name=tag)
                new_tags.append(tag_db_obj)
            else:
                old_tags.append(tag_db_obj)
        Tag.objects.bulk_create(new_tags)
        for tag in chain(old_tags, new_tags):
            question.tags.add(tag)

        return question


class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def save(self, author: User, related_question: Question) -> Answer:
        answer = Answer(
            text=self.cleaned_data['text'],
            related_question=related_question,
            author=author,
        )
        answer.save()
        return answer
