from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.db import models

from decision_tree_classifier.validators import validate_file_size


class DecisionTreeInput(models.Model):
    data_file = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv']), validate_file_size])
    test_set_size = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    target_feature = models.CharField(max_length=100)
    max_depth = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    max_features = models.IntegerField(null=True, validators=[MinValueValidator(1)])


class DecisionTreeTestDataInput(models.Model):
    decision_tree_json = models.JSONField()
    test_data_file = models.FileField()
