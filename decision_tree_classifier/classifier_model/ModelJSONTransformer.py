import json

from sklearn_json import classification

from decision_tree_classifier.classifier_model.DecisionTree import DecisionTree


class ModelJSONTransformer:
    @staticmethod
    def get_model_as_json_string(decision_tree):
        model_as_json = classification.serialize_decision_tree(decision_tree.classifier)
        json_string = json.dumps(model_as_json)
        return json_string

    @staticmethod
    def get_model_from_json_string(model_as_json):
        decision_tree = DecisionTree(model_as_json=json.loads(model_as_json))
        return decision_tree
