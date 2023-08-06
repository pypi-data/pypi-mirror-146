import copy
import os, shutil

class copy_camera_accuracy:
    """
    This Function will copy your CSV which contain Camera Accuracy Name, and will move those file to Report Per Chunk Folder that will generate on this script too"""    
    def __init__(self,location,directory):
        self.location = location
        self.directory = directory
    def copy_camera_accuracy(location,directory):
        path_move = os.path.join(location,directory)
        os.mkdir(path_move)

        substring = "Camera Accuracy"
        for file in os.listdir(location):
            if file.find(substring) != -1:
                shutil.move(os.path.join(location,file),os.path.join(location,directory))