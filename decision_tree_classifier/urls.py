from django.urls import path

from decision_tree_classifier.views.DecisionTreeResultView import DecisionTreeResultView
from decision_tree_classifier.views.DecisionTreeView import DecisionTreeView

urlpatterns = [
    path('', DecisionTreeView.as_view()),
    path('result/', DecisionTreeResultView.as_view())
]
