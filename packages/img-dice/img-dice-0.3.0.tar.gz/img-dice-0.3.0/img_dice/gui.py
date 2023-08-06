import os
import sys
from queue import Queue

from PySide2 import QtCore
from PySide2.QtCore import QSize, QThread, Signal, Slot
from PySide2.QtGui import QIcon, QTextCursor
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QMainWindow

from img_dice.lib import dice


def resource_path(relative_path: str):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class DiceThread(QThread):
    result_ready = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = dice(*self.args, **self.kwargs)
        self.result_ready.emit(result)


class ImgDiceGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI
        loader = QUiLoader(self)
        self.ui = loader.load(resource_path("resources/form.ui"), self)
        icon = QIcon()
        icon.addFile(
            resource_path("resources/img-dice.ico"), QSize(), QIcon.Normal, QIcon.Off
        )
        self.setWindowIcon(icon)
        self.setWindowTitle("Img Dice")

        # Connect signals/slots
        self.ui.pushButtonRun.clicked.connect(self.handle_run)
        self.ui.toolButtonImgPath.clicked.connect(self.handle_img_path_select)
        self.ui.toolButtonTileIndex.clicked.connect(self.handle_tile_index_select)
        self.ui.toolButtonOutDir.clicked.connect(self.handle_out_dir_select)

    @Slot()
    def handle_run(self):
        self.worker_thread = DiceThread(self.img_path, self.tile_index_path, self.out_dir)
        self.worker_thread.result_ready.connect(self.handle_results)
        self.worker_thread.start()

    @Slot()
    def handle_results(self):
        print("Done!")

    @Slot()
    def handle_img_path_select(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", filter="Images (*.tif)")
        self.ui.lineEditImgPath.setText(path)

    @property
    def img_path(self):
        return self.ui.lineEditImgPath.text()

    @Slot()
    def handle_tile_index_select(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Tile Index", filter="Shapefiles (*.shp)")
        self.ui.lineEditTileIndex.setText(path)

    @property
    def tile_index_path(self):
        return self.ui.lineEditTileIndex.text()

    @Slot()
    def handle_out_dir_select(self):
        path = QFileDialog.getExistingDirectory(self, "Choose Save Location")
        self.ui.lineEditOutDir.setText(path)

    @property
    def out_dir(self):
        return self.ui.lineEditOutDir.text()

    @Slot(str)
    def append_to_log(self, text):
        self.ui.textEdit.moveCursor(QTextCursor.End)
        self.ui.textEdit.insertPlainText(text)


# The new Stream Object which replaces the default stream associated with sys.stdout
# This object just puts data in a queue!
class WriteStream(object):
    def __init__(self, queue):
        self.q = queue

    def write(self, text):
        self.q.put(text)

    def flush(self):
        with self.q.mutex:
            self.q.queue.clear()


# A QObject (to be run in a QThread) which sits waiting for data to come through a Queue.Queue().
# It blocks until data is available, and one it has got something from the queue, it sends
# it to the "MainThread" by emitting a Qt Signal
class LoggingThread(QThread):
    text_received = Signal(str)

    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            text = self.queue.get()
            self.text_received.emit(text)

    @Slot()
    def stop(self):
        print("Exiting")  # Required to exit the waiting queue in run loop
        self.running = False
        self.quit()
        self.wait()


if __name__ == "__main__":
    # Create Queue and redirect sys.stdout to this queue
    queue = Queue()
    sys.stdout = WriteStream(queue)

    # Create QApplication and QWidget
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    widget = ImgDiceGUI()
    widget.show()

    # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
    receiver = LoggingThread(queue)
    receiver.text_received.connect(widget.append_to_log)
    app.aboutToQuit.connect(receiver.stop)
    receiver.start()

    sys.exit(app.exec_())
