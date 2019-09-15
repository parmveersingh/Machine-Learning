from PyQt5.QtWidgets import QMainWindow, QApplication ,QWidget , QVBoxLayout , QDockWidget ,  QButtonGroup , QFileDialog ,QPushButton, QDial , QHBoxLayout, QStyle, QSlider, QLabel, QSpacerItem,  QSizePolicy
import sys
from PyQt5.QtGui import QIcon, QKeySequence , QPixmap
from PyQt5.QtCore import QTranslator , QUrl, Qt , QDir , QSize , QEvent
from menus import Allmenu
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer , QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
import random

class Start(QMainWindow):
    def __init__(self):
        super(Start,self).__init__()
        self.titles = "Media Player"
        self.left = 500
        self.top = 300
        self.width = 400
        self.height = 200
        self.window_main()
        self.adding_menus()

    def openMultipleFile(self):
        dialogs = QFileDialog(self)
        self.fnames,_ =  dialogs.getOpenFileNames(self, 'Open Media Files',
        QDir.homePath(),"Videos (*.mp4 *.mkv *.3pg)")
        if self.fnames != '':
            self.playlist = QMediaPlaylist(self)
            self.fnamelist = []
            for playlst in self.fnames:
                self.fnamelist.append(QMediaContent(QUrl.fromLocalFile(playlst)))
            self.playlist.addMedia(self.fnamelist)
            self.playlist.setCurrentIndex(1)
            self.videoWidget = QVideoWidget(self)
            
            self.mediaPlayer.setVideoOutput(self.videoWidget)
    #        self.videoWidget.setAspectRatioMode(60, 60,Qt.KeepAspectRatioByExpanding)

            self.mediaPlayer.setPlaylist(self.playlist)
            self.playlist.currentIndexChanged.connect(self.mediaNameChange)
            self.mediaPlayer.play()
            self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.play.setEnabled(True)
            self.stop.setEnabled(True)
            self.loop.setEnabled(True)
            if(len(self.fnamelist) > 1):
                self.forw.setEnabled(True)
                self.shuffl.setEnabled(True)
            self.l1.setText("00:00")
            mediaName = self.fnames[0].rsplit('/', 1)[-1]
            self.fulltitle = mediaName+" - "+self.titles
            self.setWindowTitle(self.fulltitle)
            self.mediaPlayer.durationChanged.connect(self.sliderDuration)


    def openFile(self):
        self.fname,_ =  QFileDialog.getOpenFileName(self, 'Open Media Files',
        QDir.homePath(),"Videos (*.mp4 *.mkv *.3pg)")

        if self.fname != '':
            mediaName = self.fname.rsplit('/', 1)[-1]
            self.fulltitle = mediaName+" - "+self.titles
            self.setWindowTitle(self.fulltitle)
            self.playlist = QMediaPlaylist(self)
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.fname)))
            self.playlist.setCurrentIndex(1)
            self.mediaPlayer.setPlaylist(self.playlist)
            self.playlist.currentIndexChanged.connect(self.mediaNameChange)
            self.mediaPlayer.play()
            self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.play.setEnabled(True)
            self.stop.setEnabled(True)
            self.loop.setEnabled(True)
            self.l1.setText("00:00")
            self.mediaPlayer.durationChanged.connect(self.sliderDuration)




    def window_main(self):
        self.setWindowTitle(self.titles)
        qw = QWidget()
        self.setGeometry(self.left,self.top,qw.maximumWidth(),qw.maximumHeight())
        self.setMinimumSize(540, 0)
        self.setWindowIcon(QIcon("mediaplayer.png"))
        self.video()
        self.show()


    def sliderChanged(self , position):
        pos = position*1000
        self.mediaPlayer.setPosition(pos)
        self.slider.setValue(position)


    def adding_menus(self):
        menu = Allmenu(self)

    def volumeChange(self,vol):
        self.mediaPlayer.setVolume(vol)


    def sliderDuration(self,duratn):
        milisec = self.mediaPlayer.duration()
        sec = int(milisec/1000)
        hour = int(sec/3600)
        min = int((sec/60) - (hour*60))
        secs = int(sec - (min*60) - (hour*60*60))
        self.l2.setText(str(hour)+":"+str(min)+":"+str(secs))
        self.slider.setMaximum(sec)

    def sliderDuration2(self,duratn):
        second = int(duratn/1000)
        self.slider.setValue(second)
        hour = int(second/3600)
        min = int((second/60) - (hour*60))
        secs = int(second - (min*60) - (hour*60*60))
        if (min<10):
            min = "0"+str(min)
        else:
            min = str(min)

        if (secs<10):
            secs = "0"+str(secs)
        else:
            secs = str(secs)

        if (hour == 0):
            self.l1.setText(min+":"+secs)
        else:
            self.l1.setText(str(hour)+":"+min+":"+secs)

    def mediaNameChange(self,index):
        mediaName = self.fnames[index].rsplit('/', 1)[-1]
        self.fulltitle = mediaName+" - "+self.titles
        self.setWindowTitle(self.fulltitle)
        if(self.playlist.playbackMode() == 4):
            self.forw.setEnabled(True)
            self.back.setEnabled(True)
        else:
            if((index+1) == self.playlist.mediaCount()):
                self.forw.setEnabled(False)
                self.back.setEnabled(True)
            else:
                self.back.setEnabled(True)

    def video(self):
         self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
         self.mediaPlayer.positionChanged.connect(self.sliderDuration2)
         self.mediaPlayer.setVolume(10)

         videoWidget = QVideoWidget()
         layout = QVBoxLayout()

         wid = QWidget(self)
         self.play = QPushButton()
         self.play.setEnabled(False)
         self.play.setFixedWidth(40)
         self.play.setFixedHeight(30)
         self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
         self.play.setIconSize(QSize(20,20))
         self.play.clicked.connect(self.playAction)
         self.play.setShortcut(QKeySequence("Space"))

         self.back = QPushButton()
         self.back.setEnabled(False)
         self.back.setFixedWidth(40)
         self.back.setFixedHeight(25)
         self.back.setStyleSheet("margin-left: 10px")
         self.back.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
         self.back.setIconSize(QSize(14,14))
         self.back.clicked.connect(self.prevAction)

         self.back.setShortcut(QKeySequence("Ctrl+b"))

         self.stop = QPushButton()
         self.stop.setEnabled(False)
         self.stop.setFixedWidth(40)
         self.stop.setFixedHeight(25)
         self.stop.setStyleSheet("margin-left: 0px")
         self.stop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
         self.stop.setIconSize(QSize(14,14))
         self.stop.clicked.connect(self.stopAction)
         self.stop.setShortcut(QKeySequence("s"))


         self.forw = QPushButton()
         self.forw.setEnabled(False)
         self.forw.setFixedWidth(40)
         self.forw.setFixedHeight(25)
         self.forw.setStyleSheet("margin-left: 0px")
         self.forw.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
         self.forw.setIconSize(QSize(14,14))
         self.forw.clicked.connect(self.forwAction)
         self.forw.setShortcut(QKeySequence("Ctrl+f"))


         self.loop = QPushButton()
         self.loop.setEnabled(False)
         self.loop.setFixedWidth(40)
         self.loop.setFixedHeight(25)
         self.loop.setStyleSheet("margin-left: 10px")
         self.loop.setIcon(QIcon(QPixmap("loop.svg")))
         self.loop.setIconSize(QSize(14,14))
         self.loop.clicked.connect(self.loopAction)
         self.loop.setShortcut(QKeySequence("Ctrl+l"))

         self.shuffl = QPushButton()
         self.shuffl.setEnabled(False)
         self.shuffl.setFixedHeight(25)
         self.shuffl.setStyleSheet("margin-left: 0px")
         self.shuffl.setFixedWidth(40)
         self.shuffl.setFixedHeight(25)
         self.shuffl.setStyleSheet("margin-left: 0px")
         self.shuffl.setIcon(QIcon(QPixmap("shuffl.svg")))
         self.shuffl.setIconSize(QSize(14,14))
         self.shuffl.clicked.connect(self.shufflAction)
         self.shuffl.setShortcut(QKeySequence("Ctrl+shift+s"))

         spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)


         self.volume = QDial()
         self.volume.setFixedWidth(40)
         self.volume.setFixedHeight(40)
         self.volume.setMaximum(100)
         self.volume.setMinimum(0)
         self.volume.setToolTip("Volume")
         self.volume.valueChanged.connect(self.volumeChange)

         hlayout = QHBoxLayout()
         hlayout.addWidget(self.play)
         hlayout.addWidget(self.back)
         hlayout.addWidget(self.stop)
         hlayout.addWidget(self.forw)
         hlayout.addWidget(self.loop)
         hlayout.addWidget(self.shuffl)
         hlayout.addItem(spacer)
         hlayout.addWidget(self.volume)



         hslayout = QHBoxLayout()
         self.slider = QSlider(Qt.Horizontal)
         self.slider.setMinimum(0)
         self.slider.setMaximum(0)
         self.l1 = QLabel()
         self.l1.setText("--:--:--")
         self.l2 = QLabel()
         self.l2.setText("--:--:--")
         self.slider.sliderMoved.connect(self.sliderChanged)
         hslayout.addWidget(self.l1)
         hslayout.addWidget(self.slider)
         hslayout.addWidget(self.l2)


         layout.addWidget(videoWidget)

         layout.addLayout(hslayout)
         layout.addLayout(hlayout)
         wid.setLayout(layout)

         self.setCentralWidget(wid)
         self.mediaPlayer.setVideoOutput(videoWidget)

    def playAction(self):
         if (self.mediaPlayer.state()==1):
            self.mediaPlayer.pause()
            self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
         elif (self.mediaPlayer.state()==2):
            self.mediaPlayer.play()
            self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

         else:
             self.back.setEnabled(False)
             self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


    def stopAction(self):
        self.mediaPlayer.stop()
        self.play.setEnabled(False)
        self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.setWindowTitle(self.titles)
        self.l1.setText("--:--:--")
        self.l2.setText("--:--:--")


    def forwAction(self):
        if(self.playlist.playbackMode() == 4):
            self.forw.setEnabled(True)
            self.back.setEnabled(True)
            indexes = random.randint(0,(self.playlist.mediaCount()-1));
            self.playlist.setCurrentIndex(indexes)
        elif(self.playlist.playbackMode() == 1):
            self.playlist.next()
        else:
            print(self.playlist.currentIndex())
            if((self.playlist.currentIndex()+2) == self.playlist.mediaCount()):
                self.forw.setEnabled(False)
                self.playlist.next()
                self.back.setEnabled(True)
            else:
                self.playlist.next()
                self.back.setEnabled(True)


    def prevAction(self):
        if(self.playlist.playbackMode() == 4):
            self.forw.setEnabled(True)
            self.back.setEnabled(True)
            indexes = random.randint(0,(self.playlist.mediaCount()-1));
            self.playlist.setCurrentIndex(indexes)
        elif(self.playlist.playbackMode() == 1):
            self.playlist.previous()
        else:
            if(self.playlist.currentIndex() == 1):
                self.forw.setEnabled(True)
                self.playlist.previous()
                self.back.setEnabled(False)
            else:
                self.playlist.previous()
                self.forw.setEnabled(True)

    def loopAction(self):
        if(self.playlist.playbackMode() != 1):
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            self.loop.setIcon(QIcon(QPixmap("greenloop.svg")))
            self.shuffl.setIcon(QIcon(QPixmap("shuffl.svg")))
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            self.loop.setIcon(QIcon(QPixmap("loop.svg")))

    def shufflAction(self):
        if(self.playlist.playbackMode() != 4):
            self.playlist.setPlaybackMode(QMediaPlaylist.Random)
            self.shuffl.setIcon(QIcon(QPixmap("greenshuffl.svg")))
            self.loop.setIcon(QIcon(QPixmap("loop.svg")))
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            self.shuffl.setIcon(QIcon(QPixmap("shuffl.svg")))

    def close(self):
        sys.exit(1)

if __name__ == "__main__":
        app = QApplication(sys.argv)
        strt = Start()
        sys.exit(app.exec_())
