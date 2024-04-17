# Pypanel
# from projectmanager import project

# def createInterface():
#    return project.ProjectManager()

import hou
import os
from hutil.Qt import QtWidgets, QtUiTools
import datetime
      
class ProjectManager(QtWidgets.QWidget):

    def __init__(self):
        super(ProjectManager, self).__init__()
        
        self.projectpath = hou.getenv("JOB") + "/"
        
        # load UI
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load("C:/Users/Markel/Documents/houdini19.5/scripts/python/projectmanager/projectui.ui")

        # get ui elements
        self.setproj = self.ui.findChild(QtWidgets.QPushButton, "setproj")
        self.projpath = self.ui.findChild(QtWidgets.QLabel, "projectpath")
        self.projname = self.ui.findChild(QtWidgets.QLabel, "projectname")
        self.scenelist = self.ui.findChild(QtWidgets.QListWidget, "scenelist")
        self.datelist = self.ui.findChild(QtWidgets.QListWidget, "datelist")
        
        # create connection
        self.setproj.clicked.connect(self.setproject)
        
        # layout
        mainLayout = QtWidgets.QVBoxLayout()    
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

    def setproject(self):
        # set project
        setjob = hou.ui.selectFile(title = "Set Project", file_type=hou.fileType.Directory)
        hou.hscript("setenv JOB=" + setjob)

        self.projectpath = hou.getenv("JOB") + "/"

        # name tabs
        projname = setjob.split("/")[-2]
        setjob = os.path.dirname(setjob)
        
        self.projname.setText(projname)
        self.projpath.setText(setjob + "/")
        projpath = os.path.split(setjob)[0]
        
        self.datelist = self.ui.findChild(QtWidgets.QListWidget, "datelist")

        self.createInterface()

    def openScene(self, scene):
        sceneName = scene.data()
        hipFile = self.projectpath + sceneName
        # open scene
        hou.hipFile.load(hipFile)
        print("Loaded scene " + sceneName)

    def get_file_modification_date(self, filename):
        # get the date of craeation and modification of the files
        modification_time = os.path.getmtime(filename)
        modification_date = datetime.datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
        return modification_date

    def createInterface(self): 
        # cleaning previous values 
        self.scenelist.clear()      
        self.datelist.clear() 
        # display date and file name
        for file in os.listdir(self.projectpath):
            if file.endswith(".hip"):
                modification_date = self.get_file_modification_date(os.path.join(self.projectpath, file))
                self.scenelist.addItem(file)
                self.datelist.addItem(modification_date)

        # let scene load by double clicking
        self.scenelist.doubleClicked.connect(self.openScene)