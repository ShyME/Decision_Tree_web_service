from django.contrib import admin
from decision_tree_classifier.models import DecisionTreeInput, DecisionTreeTestDataInput


admin.site.register(DecisionTreeInput)
admin.site.register(DecisionTreeTestDataInput)
