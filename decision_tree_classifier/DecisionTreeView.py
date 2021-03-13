import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import pandas as pd

from decision_tree_classifier.DropboxClient import DropboxClient
from decision_tree_classifier.apps import DecisionTreeClassifierConfig
from decision_tree_classifier.utils import ModelJsonUtil, get_unique_filename
from decision_tree_classifier.DecisionTree import DecisionTree
from decision_tree_classifier.serializers import DecisionTreeInputSerializer


class DecisionTreeView(APIView):
    def post(self, request):
        decision_tree_input_serializer = DecisionTreeInputSerializer(data=request.data)
        if decision_tree_input_serializer.is_valid():
            request_data = decision_tree_input_serializer.validated_data

            data_file = request_data["data_file"]
            target_feature = request_data["target_feature"]
            test_set_size = request_data["test_set_size"]
            max_depth = request_data["max_depth"]
            max_features = request_data["max_features"]

            data_frame = pd.read_csv(data_file)

            decision_tree = DecisionTree(data_frame, target_feature, test_set_size, max_depth, max_features)

            # image_path = os.path.dirname(__file__)
            # tree_img_file_path = os.path.join(image_path, ("/mlt_dtree/images/" + get_unique_filename("png")))
            tree_image_file_path = os.path.join(DecisionTreeClassifierConfig.image_file_path, get_unique_filename("png"))
            decision_tree.create_image(tree_image_file_path)

            return Response(
                {
                    "accuracy": decision_tree.accuracy,
                    "model": ModelJsonUtil.get_model_as_json_string(decision_tree),
                    "imageUrl": DropboxClient().upload_share_file(tree_image_file_path)
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                decision_tree_input_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

