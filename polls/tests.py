from calendar import c
import datetime
from this import d
from urllib import response
from venv import create

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question
# Create your tests here.

class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        futureQuestion = Question(pub_date=time)
        self.assertIs(futureQuestion.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        oldQuestion = Question(pub_date = time)
        self.assertIs(oldQuestion.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() -datetime.timedelta(hours=23, minutes=59, seconds=59)
        recentQuestion = Question(pub_date = time)
        self.assertIs(recentQuestion.was_published_recently(), True)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text = question_text, pub_date = time)

class QuestionIndexViewTest(TestCase):

    def test_no_questions(self): 
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latestQuestionList'], [])

    def test_past_question(self):
        question1 = create_question(question_text='Past Question', days=-30)
        question2 = create_question(question_text='Past Questiun 2', days=-20)
        create_question(question_text='Future Questiuon', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latestQuestionList'],
            [question2, question1]
        )

    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latestQuestionList'],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        futureQuestion = create_question(question_text='Future question', days=5)
        url = reverse('polls:detail', args=(futureQuestion.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        pastQuestion = create_question(question_text='Past question', days=-5)
        url = reverse('polls:detail', args=(pastQuestion.id,))
        response = self.client.get(url)
        self.assertContains(response, pastQuestion.question_text)