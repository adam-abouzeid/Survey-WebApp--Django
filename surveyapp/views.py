from django.shortcuts import render
from .models import User, Survey, Category, SubmittedSurveys
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.


def index(request):
    categories = Category.objects.all()
    return render(request, "surveyapp/index.html", {"categories": categories})


@login_required(login_url="/login")
def Surveys(request, topic):
    surveys = Survey.objects.filter(category=topic)
    category = Category.objects.get(id=topic)
    users = category.users
    x = users.split(',')
    return render(request, "surveyapp/surveys.html", {"surveys": surveys, "points": request.user.points, "users": x})


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "surveyapp/signup.html", {"message": "password and confirmation arent the same"})

        try:
            user = User.objects.create_user(username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "surveyapp/signup.html", {"message": "username already taken"})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "surveyapp/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "surveyapp/login.html", {"message": "Invalid Username or password."})
    else:
        return render(request, "surveyapp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def single_survey(request, single_survey_name):
    if request.method == "POST":
        s = SubmittedSurveys()
        survey = Survey.objects.get(id=single_survey_name)
        s.survey = survey
        s.user = request.user.username
        survey.people += 1
        user = User.objects.get(username=request.user.username)
        user.points += 1
        user.save()
        survey.save()
        category = Category.objects.get(category_name=survey.category)
        if request.user.username in category.users:
            pass
        else:
            category.users += str(request.user.username) + ","
            category.save()
        # survey = Survey.objects.get(id=single_survey_name)
        question = survey.question
        s.question = question
        s.answer = request.POST["choice"]
        if s.answer == "Strongly Agree":
            survey.stronglyagree += 1
        elif s.answer == "Agree":
            survey.agree += 1
        elif s.answer == "Neutral":
            survey.neutral += 1
        elif s.answer == "Disagree":
            survey.disagree += 1
        elif s.answer == "Strongly Disagree":
            survey.stronglydisagree += 1
        s.save()
        survey.save()
        # questions = Questions.objects.filter(survey=single_survey_name)
        # length = len(questions)
        # answers = []
        # questions = []
        # for i in range(length):
        #     answers.append(request.POST[f"choice{i + 1}"])
        #     questions.append(request.POST[f"question{i + 1}"])
        # s.answers = str(answers)
        # s.questions = str(questions)

        # submitted = SubmittedSurveys.objects.get(survey=single_survey_name)
        # print(submitted.answer)


        # print(answers)
        return render(request, "surveyapp/postsurvey.html", {
            "survey": survey,
            "question": question,
            "people": survey.people-1 ,
            "answer": s.answer,
            "agree": survey.agree,
            "stronglya": survey.stronglyagree,
            "neutral": survey.neutral,
            "disagree": survey.disagree,
            "stronglyd": survey.stronglydisagree

            # "questioned": questions
        })
    else:
        survey = Survey.objects.get(id=single_survey_name)
        question = survey.question
        return render(request, "surveyapp/singlesurvey.html", {"survey": survey, "question": question})


#
# @login_required(login_url="/login")
# def postsurvey(request, survey_name):
#     # if request.method == "POST":
#         # s = SubmittedSurveys()
#         # survey = Survey.objects.get(id=survey_name)
#         # s.survey = survey
#         # s.user = request.user.username
#         # survey.people += 1
#         # survey.save()
#         # questions = Questions.objects.filter(survey=survey_name)
#         # length = len(questions)
#         # answers = []
#         # questions = []
#         # for i in range(length):
#         #     answers.append(request.POST[f"choice{i+1}"])
#         #     questions.append(request.POST[f"question{i+1}"])
#         # s.answers = str(answers)
#         # s.questions = str(questions)
#         # s.save()
#         # survey = Survey.objects.get(id=survey_name)
#         # return render(request, "surveyapp/postsurvey.html", {"survey": survey, "people": survey.people,})
#
#     # else:  # get
#     return render(request, "surveyapp/postsurvey.html")


def addcat(request):
    if request.method == "POST":
        c = Category()
        c.category_name = request.POST["category"]
        c.icon = request.POST["icon"]
        c.save()
        return HttpResponseRedirect(reverse("index"))
    else:

        return render(request, "surveyapp/addcat.html")


def deletecat(request):
    if request.method == "POST":
        x = request.POST.get("categorydelete")
        y = x[1:len(x)-1]
        category = Category.objects.get(category_name=y)
        category.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "surveyapp/deletecat.html", {
            "categories": Category.objects.all()
        })


def addsurv(request):
    if request.method == "POST":
        s = Survey()
        s.title_name = request.POST["title"]
        s.question = request.POST["question"]
        s.subtitle = request.POST["subtitle"]
        # s.category = request.POST["category"]
        x = request.POST["category"]
        y = x[1:len(x)-1]
        category = Category.objects.get(category_name=y)
        s.category = category
        s.save()
        return HttpResponseRedirect(reverse("index"))
    else:

        categories = Category.objects.all()
        return render(request, "surveyapp/addsurv.html",
                      {
                          "category": categories,

                      })


def deletesurvey(request):
    if request.method == "POST":
        survey = request.POST["survey"]
        survey = survey[1:len(survey) - 1]
        s = Survey.objects.get(id=survey)
        s.delete()
        return HttpResponseRedirect(reverse("index"))
        # print(x)
        # print(y)
        # print(survey)
    else:

        s = Survey.objects.all()
        return render(request, "surveyapp/deletesurvey.html", {
            "surveys": s
        })
