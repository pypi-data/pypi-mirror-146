from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from ob_dj_survey.apis.survey.views import AnswerView, QuestionView, SurveyView

app_name = "survey"

router = DefaultRouter()

router.register(r"", SurveyView, basename="survey")

urlpatterns = [
    path("", include(router.urls)),
    path("answers", AnswerView.as_view(), name="survey-answers"),
    path("question", QuestionView.as_view(), name="survey-question"),
]
