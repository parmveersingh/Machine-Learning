from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import  QMenuBar, QMenu ,QAction , QFileDialog
from PyQt5.QtGui import QIcon, QKeySequence

class Allmenu:

    def __init__(self,main_obj):
        obj = main_obj
        mb = obj.menuBar()
        trans = QTranslator()
        self.media(mb,trans,obj)
        self.playback(mb,trans,obj)
        self.audio(mb,trans,obj)
        self.video(mb,trans,obj)
        self.subtitle(mb,trans,obj)
        self.help(mb,trans,obj)


    def media(self,mb,trans,obj):

        media =QMenuBar.addMenu(mb,trans.tr("&Media"))

        openfile_action = QAction(trans.tr("&Open File..."),obj)
        openfile_action.triggered.connect(obj.openFile)
        openfile_action.setShortcut(QKeySequence(trans.tr("Ctrl+O")))
        media.addAction(openfile_action)



        openmultifile_action = QAction(trans.tr("&Open Multiple Files..."),obj)
        openmultifile_action.setShortcut(QKeySequence(trans.tr("Ctrl+Shift+O")))
        openmultifile_action.triggered.connect(obj.openMultipleFile)
        media.addAction(openmultifile_action)


        media.addSeparator()

        openquit_action = QAction(trans.tr("&Quit"),obj)
        openquit_action.setShortcut(QKeySequence(trans.tr("Ctrl+Q")))
        media.addAction(openquit_action)
        openquit_action.triggered.connect(obj.close)




    def playback(self,mb,trans,obj):

        playback =QMenuBar.addMenu(mb,trans.tr("P&layback"))

        speed = playback.addMenu(trans.tr("Sp&eed"))

        faster_speed_action = QAction(trans.tr("&Faster"),obj)
        speed.addAction(faster_speed_action)

        faster_fine_speed_action = QAction(trans.tr("Faster (fine)"),obj)
        speed.addAction(faster_fine_speed_action)

        Normal_speed_action = QAction(trans.tr("N&ormal"),obj)
        speed.addAction(Normal_speed_action)

        slower_fine_speed_action = QAction(trans.tr("Slower (fine)"),obj)
        speed.addAction(slower_fine_speed_action)

        slower_speed_action = QAction(trans.tr("Slo&wer"),obj)
        speed.addAction(slower_speed_action)

        playback.addSeparator()

        forward_action = QAction(trans.tr("&Jump Forward"),obj)
        playback.addAction(forward_action)

        backward_action = QAction(trans.tr("Jump Bac&kward"),obj)
        playback.addAction(backward_action)

        specific_time_action = QAction(trans.tr("Jump to Specific Time"),obj)
        specific_time_action.setShortcut(QKeySequence(trans.tr("Ctrl+T")))
        playback.addAction(specific_time_action)

        playback.addSeparator()

        play_action = QAction(trans.tr("&Play"),obj)
        playback.addAction(play_action)

        stop_action = QAction(trans.tr("&Stop"),obj)
        playback.addAction(stop_action)

        previous_action = QAction(trans.tr("Pre&vious"),obj)
        playback.addAction(previous_action)

        next_action = QAction(trans.tr("Next"),obj)
        playback.addAction(next_action)

    def audio(self,mb,trans,obj):

        audio =QMenuBar.addMenu(mb,trans.tr("&Audio"))

        inc_vol_action = QAction(trans.tr("&Increase Volume"),obj)
        audio.addAction(inc_vol_action)

        dec_vol_action = QAction(trans.tr("D&ecrease Volume"),obj)
        audio.addAction(dec_vol_action)

        mute_action = QAction(trans.tr("&Mute"),obj)
        audio.addAction(mute_action)

    def video(self,mb,trans,obj):

        video = QMenuBar.addMenu(mb,trans.tr("&Video"))

        zoom = video.addMenu(trans.tr("&Zoom"))

        normal = QAction(trans.tr("1:1 Original"),obj)
        zoom.addAction(normal)

        video.addSeparator()

        fit_action = QAction(trans.tr("Always Fit &Window"),obj)
        fit_action.setChecked(True)
        fit_action.setCheckable(True)
        video.addAction(fit_action)

        full_screen_action = QAction(trans.tr("&Full Screen"),obj)
        full_screen_action.setChecked(True)
        full_screen_action.setCheckable(True)
        video.addAction(full_screen_action)

    def subtitle(self,mb,trans,obj):

        subtitle = QMenuBar.addMenu(mb,trans.tr("Subti&tle"))

        add_sub_action = QAction(trans.tr("Add &Subtitle File..."),obj)
        subtitle.addAction(add_sub_action)


    def help(self,mb,trans,obj):

        help = QMenuBar.addMenu(mb,trans.tr("&Help"))

        help_action = QAction(trans.tr("&Help"),obj)
        help_action.setShortcut(QKeySequence(trans.tr("F1")))
        help.addAction(help_action)

        help.addSeparator()

        about_action = QAction(trans.tr("&About"),obj)
        about_action.setShortcut(QKeySequence(trans.tr("Shift+F1")))
        help.addAction(about_action)
