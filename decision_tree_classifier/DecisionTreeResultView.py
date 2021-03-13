from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import pandas as pd

from decision_tree_classifier.utils import ModelJsonUtil
from decision_tree_classifier.serializers import DecisionTreeTestDataInputSerializer


class DecisionTreeResultView(APIView):
    def post(self, request):
        decision_tree_test_data_input_serializer = DecisionTreeTestDataInputSerializer(data=request.data)
        if decision_tree_test_data_input_serializer.is_valid():
            request_data = decision_tree_test_data_input_serializer.validated_data

            test_data_file = request_data["test_data_file"]
            decision_tree_json = request_data["decision_tree_json"]

            decision_tree = ModelJsonUtil.get_model_from_json_string(decision_tree_json)
            predicted_result = decision_tree.predict(pd.read_csv(test_data_file))

            return Response(
                predicted_result,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                decision_tree_test_data_input_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
