import os

from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

from decision_tree_classifier.model_image.DropboxClient import DropboxClient
from decision_tree_classifier.utils.utils import delete_old_files_from


class DecisionTreeClassifierConfig(AppConfig):
    name = 'decision_tree_classifier'
    image_file_path = os.path.join(os.path.dirname(__file__), "/mlt_dtree/images/")

    def ready(self):
        self.__schedule_tasks()
        print(DecisionTreeClassifierConfig.image_file_path)

    def __schedule_tasks(self):
        self.__scheduler = BackgroundScheduler()

        self.__scheduler.add_job(DropboxClient().delete_old_files, 'cron', hour='*/4')
        self.__scheduler.add_job(delete_old_files_from, 'cron', [DecisionTreeClassifierConfig.image_file_path], hour="*/4")

        self.__scheduler.start()
