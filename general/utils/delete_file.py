import os
from core import settings


class DeleteFile:
    media_path_from = settings.MEDIA_ROOT

    def delete(self, file_path=None):
        file_exist = os.path.exists(file_path)
        if file_exist:
            os.remove(file_path)
            return True
        else:
            return False

