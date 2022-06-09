import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)

    return Question.objects.create(
        question_text=question_text,
        pub_date=time
    )

def create_choice(question, choice_text):

    return question.choice_set.create(choice_text=choice_text)



class QuestionIndexViewTests(TestCase):
   
   
    def test_no_questions(self):

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")

        self.assertQuerysetEqual(response.context['latest_question_list'],[])


    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """

        question = create_question(question_text="Past question", days=-30)

        choice1 = create_choice(question, "any choice")
        choice2 = create_choice(question, "any choice")


        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """

        future_question = create_question(question_text="Future question", days=30)

        choice1 = create_choice(future_question, "any choice")
        choice2 = create_choice(future_question, "any choice")

        response = self.client.get(reverse("polls:index"))

        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        old_question = create_question(question_text="Past question.", days=-30)
        future_question = create_question(question_text="Future question.", days=30)
        
        choice1 = create_choice(old_question, "any choice")
        choice2 = create_choice(old_question, "any choice")

        choice3 = create_choice(future_question, "any choice")
        choice4 = create_choice(future_question, "any choice")
        
        
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [old_question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions with at least two choices each one.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)

        choice1 = create_choice(question1, "any choice")
        choice2 = create_choice(question1, "any choice")

        choice3 = create_choice(question2, "any choice")
        choice4 = create_choice(question2, "any choice")
        
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

    def test_questions_with_no_choices(self):
        """
        The questions index page doesn't display questions with no choices
        """

        question = create_question(question_text="Question", days=-30)

        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, "No polls are available.")

    def test_questions_with_one_choice(self):
        """
        The questions index page doesn't display questions with one choice
        """
        question = create_question(question_text="Past question 1.", days=-30)
    
        choice = create_choice(question, "any choice")

        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [],
        )
   




class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        
        """ 
            was_published_recently() returns False for questions whose
            pub_date is in future
        """

        time = timezone.now() + datetime.timedelta(days=30)

        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)



    def test_was_published_recently_with_old_question(self):

        """
            was_published_recently() returns False when the question
            has one day and one second more of having been published
        """


        time = timezone.now() - datetime.timedelta(days=1, seconds=1)

        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):

        """
            was_published_recently() returns true when the question
            hasn't passed one day of being published
        """
        time = timezone.now() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)

        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)





class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question("Future question", 30)

        choice1 = create_choice(future_question, "any choice")
        choice2 = create_choice(future_question, "any choice")

        response = self.client.get(reverse("polls:detail",args=(future_question.id,)))


        self.assertEqual(response.status_code,404)


    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """

        past_question = create_question("Old question", days = -1)

        choice1 = create_choice(past_question, "any choice")
        choice2 = create_choice(past_question, "any choice")

        response = self.client.get(reverse("polls:detail",args=(past_question.id,)))

        self.assertEqual(response.status_code,200)
        self.assertContains(response, past_question.question_text)

    def test_question_with_no_choice(self):
        """
        The detail view of a question with a pub_date in the past
        displays a 404 error
        """

        question = create_question("Old question", days = -1)


        response = self.client.get(reverse("polls:detail",args=(question.id,)))

        self.assertEqual(response.status_code,404)


class QuestionResultViewTests(TestCase):
    def test_future_question(self):
        """
        The result view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question("Future question", 30)

        choice1 = create_choice(future_question, "any choice")
        choice2 = create_choice(future_question, "any choice")


        response = self.client.get(reverse("polls:results",args=(future_question.id,)))


        self.assertEqual(response.status_code,404)


    def test_past_question(self):
        """
        The result view of a question with a pub_date in the past
        displays the question's text.
        """

        past_question = create_question("Old question", days = -1)

        choice1 = create_choice(past_question, "any choice")
        choice2 = create_choice(past_question, "any choice")

        response = self.client.get(reverse("polls:results",args=(past_question.id,)))

        self.assertEqual(response.status_code,200)
        self.assertContains(response, past_question.question_text)

    def test_choice_results(self):
        """
        The result view for a question with a choice with votes
        displays the votes of that choice
        """

        question = create_question(question_text="Any question", days=-2)

        question.choice_set.create(choice_text="First choice",votes=3)
        question.choice_set.create(choice_text="Second choice",votes=5)
        choices = question.choice_set.all()

        response = self.client.get(reverse("polls:results",args=(question.id,)))

        self.assertIs(response.status_code, 200)
        self.assertContains(response, choices[0].votes)


        context_question = response.context["question"]
        self.assertQuerysetEqual(context_question.choice_set.all(),choices, ordered=False)

        
    def test_question_with_no_choice(self):
        """
        The result view for a question with no choice choice
        displays a 404 page
        """
        question = create_question(question_text="Any question", days=-2)

        response = self.client.get(reverse("polls:results",args=(question.id,)))

        self.assertEqual(response.status_code,404)
    





