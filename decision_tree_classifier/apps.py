import os
import pathlib

from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

from decision_tree_classifier.model_image.DropboxClient import DropboxClient
from decision_tree_classifier.utils.utils import delete_old_files_from
from mlt_decisionTree.settings import BASE_DIR


class DecisionTreeClassifierConfig(AppConfig):
    name = 'decision_tree_classifier'
    image_file_path = os.path.join(BASE_DIR / "served_images/")

    def ready(self):
        self.__create_image_dir()
        self.__schedule_tasks()

    def __create_image_dir(self):
        pathlib.Path(DecisionTreeClassifierConfig.image_file_path).mkdir(parents=True, exist_ok=True)

    def __schedule_tasks(self):
        self.__scheduler = BackgroundScheduler()
        self.__scheduler.add_job(DropboxClient().delete_old_files, 'cron', [15*60], hour='*/1')
        self.__scheduler.add_job(delete_old_files_from, 'cron', [DecisionTreeClassifierConfig.image_file_path, 15*60], hour="*/1")
        self.__scheduler.start()
