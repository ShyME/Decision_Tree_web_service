from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn_json import classification

from io import StringIO
import pydotplus


class DecisionTree:
    def __init__(self, data_frame=None, target_feature=None, test_set_size=None, max_depth=None, max_features=None, model_as_json=None):
        self.__classifier = None  # Decision Tree Classifier

        if model_as_json is not None:
            self.__init_model_from_json(model_as_json)
        elif data_frame is not None and target_feature is not None and test_set_size is not None:
            self.__accuracy = None  # Model accuracy score, only exists when the model is built with raw data as it
            # requires testing data sets
            self.__class_names = None  # Distinct target feature class names
            self.__init_model_from_data(data_frame, target_feature, test_set_size, max_depth, max_features)
        else:
            raise Exception("Decision Tree initialization requires either model object as JSON string or raw data csv "
                            "filename with target feature specified")

    def __init_model_from_data(self, data_frame, target_feature, test_set_size, max_depth, max_features):
        self.__classifier = DecisionTreeClassifier()

        headers = data_frame.columns.to_list()
        data_frame = data_frame.iloc[1:]

        self.__headers_without_target = headers.copy()
        self.__headers_without_target.remove(target_feature)

        X = data_frame[self.__headers_without_target]
        Y = data_frame[target_feature]

        self.__class_names = self.__get_class_names(Y)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_set_size, random_state=1)

        self.__classifier = DecisionTreeClassifier(max_depth=max_depth, max_features=max_features).fit(X_train, Y_train)
        self.__accuracy = self.__test_model_accuracy(X_test, Y_test)

    def __init_model_from_json(self, model_as_json):
        self.__classifier = classification.deserialize_decision_tree(model_as_json)

    def __test_model_accuracy(self, X_test, Y_test):
        Y_predicted = self.__classifier.predict(X_test)
        return metrics.accuracy_score(Y_test, Y_predicted)

    @staticmethod
    def __get_class_names(target_feature_frame):
        distinct_class_names = target_feature_frame.unique()
        distinct_class_names = [str(name) for name in distinct_class_names]
        return distinct_class_names

    def predict(self, X_test):
        return self.__classifier.predict(X_test)

    def create_image(self, image_name):
        dot_data = StringIO()
        export_graphviz(self.__classifier, out_file=dot_data,
                        filled=True, rounded=True,
                        special_characters=True, feature_names=self.__headers_without_target, class_names=self.__class_names)
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_png(image_name)

    @property
    def accuracy(self):
        if self.__accuracy is not None:
            return self.__accuracy
        else:
            raise Exception("Accuracy attribute is not present")

    @property
    def classifier(self):
        return self.__classifier
