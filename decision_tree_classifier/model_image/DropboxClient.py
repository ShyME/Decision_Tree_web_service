import dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode
from datetime import datetime, timezone

from decision_tree_classifier.secrets import DROPBOX_APP_TOKEN
from decision_tree_classifier.utils.singleton import singleton


@singleton
class DropboxClient:
    def __init__(self):
        access_token = DROPBOX_APP_TOKEN
        self.__dropbox = dropbox.Dropbox(access_token)

    def upload_share_file(self, filepath):
        filename = filepath[filepath.rindex("\\"):].replace("\\", "/")
        with open(filepath, "rb") as file:
            self.__dropbox.files_upload(file.read(), filename, mode=WriteMode.overwrite)
        try:
            return self.__dropbox.sharing_create_shared_link_with_settings(filename).url + "&raw=1"
        except ApiError as error:
            return error.error.get_shared_link_already_exists().get_metadata().url + "&raw=1"

    def delete_old_files(self, time_old):
        response = self.__dropbox.files_list_folder("")
        for file in response.entries:
            time_delta = datetime.now(timezone.utc) - file.client_modified.replace(tzinfo=timezone.utc)
            if time_delta.seconds >= time_old:
                self.__delete_file(file.path_display)

    def __delete_file(self, file):
        self.__dropbox.files_delete_v2(file)
