from rest_framework import serializers

from decision_tree_classifier.models import DecisionTreeInput, DecisionTreeTestDataInput


class DecisionTreeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionTreeInput
        fields = ["targetFeature", "dataFile", "testSetSize", "maxDepth", "maxFeatures"]
        extra_kwargs = {
            "dataFile": {"source": "data_file"},
            "targetFeature": {"source": "target_feature"},
            "testSetSize": {"source": "test_set_size"},
            "maxDepth": {"source": "max_depth"},
            "maxFeatures": {"source": "max_features"}
        }


class DecisionTreeTestDataInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionTreeTestDataInput
        fields = ["decisionTreeJson", "testDataFile"]
        extra_kwargs = {
            "decisionTreeJson": {"source": "decision_tree_json"},
            "testDataFile": {"source": "test_data_file"}
        }
