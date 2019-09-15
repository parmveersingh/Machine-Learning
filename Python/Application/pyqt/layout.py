from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget ,QPushButton, QGroupBox , QHBoxLayout ,QVBoxLayout
import sys

class window(QWidget):
    def __init__(self):
        super(window,self).__init__()
        self.title = "any application"
        self.top = 12
        self.left = 300
        self.mainwindow()
        self.layout_alignment()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupbox)
        self.setLayout(vbox)
        self.show()

    def mainwindow(self):
        self.setWindowTitle(self.title)
        qw = QWidget()
        self.setGeometry(self.top,self.left,qw.maximumWidth(),qw.maximumHeight())


    def layout_alignment(self):
        self.groupbox = QGroupBox("Select a prefered Sports:")
        self.groupbox.setGeometry(100,100,100,100)
        #widget = QWidget()
        layout = QHBoxLayout()
        
        button1 = QPushButton("Hockey",self)
        layout.addWidget(button1)
        button2 = QPushButton("Cricket",self)
        layout.addWidget(button2)
        button3 = QPushButton("Football",self)
        layout.addWidget(button3)

        self.groupbox.setLayout(layout)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = window()
    sys.exit(app.exec_())
