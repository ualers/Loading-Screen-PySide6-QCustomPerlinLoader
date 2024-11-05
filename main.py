########################################################################
## IMPORTS Libs
import sys
import time
from firebase_admin import credentials, initialize_app, storage, db, delete_app
########################################################################

########################################################################
# IMPORT .qrc
from src import icones_interpreter
########################################################################

########################################################################
# IMPORT GUI SoftwareAI
from src.ui_cliente_and_chat import Ui_MainWindow_SoftwareAI
########################################################################

########################################################################
# IMPORT GUI splash_screen
from src.ui_splash_screen import *
########################################################################

########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QCustomLoadingIndicators import QCustomPerlinLoader
from Custom_Widgets.QCustomLoadingIndicators import QCustomQProgressBar
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomModals import QCustomModals
########################################################################

########################################################################
# IMPORT Pyside6
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCore import Signal, QThread
########################################################################


########################################################################
# MainWindow_SoftwareAI
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow_SoftwareAI()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles = {"JsonStyle/style.json"}
                      )
        ########################################################################


########################################################################
# Update Loading Screen
class Updateloader(QThread):
    messagesignal = Signal(str)
    circleColor1signal = Signal(str)
    circleColor2signal = Signal(str)
    finishedd = Signal()
    def __init__(self, message, color1, color2):
        super().__init__()
        self.message = message
        self.color1 = color1
        self.color2 = color2
        self.running = True

    def run(self):
        while self.running:
            time.sleep(4)
            self.messagesignal.emit(self.message)

            self.messagesignal.emit("LOADING..")

            self.circleColor1signal.emit(self.color1)
            self.circleColor2signal.emit(self.color2)

            self.messagesignal.emit("LOADING...")

            self.finishedd.emit()

    def stop(self):
        self.running = False
        self.wait()

########################################################################
# MainWindow Loading Screen
class LoadingScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles = {"JsonStyle/style.json"}
                      )
        self.myParentWidget = self.ui.widget
        
        self.myParentWidget.message="LOADING."
        self.myParentWidget.size=QSize(600, 600)
        self.myParentWidget.color=QColor("white")
        self.myParentWidget.fontFamily="Ebrima"
        self.myParentWidget.fontSize=30
        self.myParentWidget.rayon=200
        self.myParentWidget.duration=60 * 1000
        self.myParentWidget.noiseOctaves=0.8
        self.myParentWidget.noiseSeed=int(time.time())
        self.myParentWidget.backgroundColor=QColor("transparent")
        self.myParentWidget.circleColor1=QColor("#ff2e63")
        self.myParentWidget.circleColor2=QColor("#082e63")
        self.myParentWidget.circleColor3=QColor(57, 115, 171, 100)
        # myModal = QCustomModals.InformationModal(
        #     title="Loading SoftwareAI", 
        #     parent=self,
        #     position='top-right',
        #     closeIcon=":/feather/icons/feather/window_close.png",
        #     modalIcon=":/feather/icons/feather/info.png",
        #     description="loading should take a few seconds...",
        #     isClosable=False,
        #     duration=3000
        # )
        #myModal.show()

        ########################################################################
        #QAppSettings.updateAppSettings(self)
        ########################################################################
        message = "LOADING."
        circleColor1 = QColor("#1e0880")
        circleColor2 = QColor("#000000")


        self.threadUpdateloader = Updateloader(message, circleColor1, circleColor2)
        self.threadUpdateloader.messagesignal.connect(self.message_signal)
        self.threadUpdateloader.circleColor1signal.connect(self.circleColor1_signal)
        self.threadUpdateloader.circleColor2signal.connect(self.circleColor2_signal)
        self.threadUpdateloader.finishedd.connect(self.finish_loading)
        self.threadUpdateloader.start()


        #self.show()

    def circleColor1_signal(self, Color1):
        self.myParentWidget.circleColor1=Color1

    def circleColor2_signal(self, Color2):
        self.myParentWidget.circleColor2=Color2

    def message_signal(self, mensage):
        self.myParentWidget.message=mensage

    def finish_loading(self):
        QTimer.singleShot(1000, self.show_main_window)

    def show_main_window(self):
        # Interrompe a thread e abre a janela principal
        self.threadUpdateloader.stop()
        self.close()
        self.main_window = MainWindow()
        self.main_window.show()


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    loading_screen = LoadingScreen()
    loading_screen.show()
    sys.exit(app.exec())
########################################################################
## END===>
######################################################################## 

