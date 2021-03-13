import dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode
from datetime import datetime

from decision_tree_classifier.decorators import singleton


@singleton
class DropboxClient:
    def __init__(self):
        access_token = "Ss7Piru_lYUAAAAAAAAAAbd0nbJOl-mly2ADF4oXPQ-dy1lFngRsBh1Temf_5mqc"
        self.__dropbox = dropbox.Dropbox(access_token)

    def upload_share_file(self, filepath):
        filename = filepath[filepath.rindex("/"):]
        print(filename)
        with open(filepath, "rb") as file:
            self.__dropbox.files_upload(file.read(), filename, mode=WriteMode.overwrite)
        try:
            return self.__dropbox.sharing_create_shared_link_with_settings(filename).url + "&raw=1"
        except ApiError as error:
            return error.error.get_shared_link_already_exists().get_metadata().url + "&raw=1"

    def delete_old_files(self):
        response = self.__dropbox.files_list_folder("")
        for file in response.entries:
            time_delta = datetime.now() - file.client_modified
            if time_delta.seconds >= 21600:  # 6 hours
                self.__delete_file(file.path_display)

    def __delete_file(self, file):
        self.__dropbox.files_delete_v2(file)
