#!/bin/env python3

# TODO: Chemins non locaux
import os
import sys
import xdg

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDateTimeEdit, QGridLayout, QLabel, QFileDialog, \
    QMessageBox, QCheckBox

import ffmpeg_screenshot

APPLICATION_NAME = "FFMPEG - Compare Tool"
VERSION = "0.1"
DATETIME_FORMAT = "HH:mm:ss.zzz"

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("{} {}".format(APPLICATION_NAME, VERSION))

        self.init_ui()
        self.init_events()

        self.filename_a = None
        self.filename_b = None

        self.output_filepath_a = None
        self.output_filepath_b = None

        self.output_folder = None

    def init_ui(self):
        self.spinbox_label = QLabel("")
        self.timecode_spinbox_a = QDateTimeEdit()
        self.timecode_spinbox_a.setDisplayFormat(DATETIME_FORMAT)
        self.timecode_spinbox_a.timeChanged.connect(lambda: self.on_timecode_changed("a"))

        self.timecode_spinbox_b = QDateTimeEdit()
        self.timecode_spinbox_b.setDisplayFormat(DATETIME_FORMAT)
        self.timecode_spinbox_b.timeChanged.connect(lambda: self.on_timecode_changed("b"))

        self.lock_timecode_checkbox = QCheckBox("Lock timecode")
        self.lock_timecode_checkbox.setChecked(True)

        self.button_filechooser_a = QPushButton("File A", icon=QIcon.fromTheme("document-open"))
        self.button_filechooser_b = QPushButton("File B", icon=QIcon.fromTheme("document-open"))

        self.button_open_picture_a = QPushButton("Open file A frame", icon=QIcon.fromTheme("image"))
        self.button_open_picture_a.clicked.connect(lambda: self.open_picture("a"))

        self.button_open_picture_b = QPushButton("Open file B frame", icon=QIcon.fromTheme("image"))
        self.button_open_picture_b.clicked.connect(lambda: self.open_picture("b"))

        self.ouput_folder_button = QPushButton("Set output folder", icon=QIcon.fromTheme("document-open-folder"))
        self.export_button = QPushButton("Extract", icon=QIcon.fromTheme("document-send"))

        self.ouput_log = QLabel()

        # region ----- Layout & Widget adding -----
        self.layout = QGridLayout()

        self.layout.addWidget(self.button_filechooser_a, 0, 0)
        self.layout.addWidget(self.timecode_spinbox_a, 0, 1)

        self.layout.addWidget(self.button_filechooser_b, 1, 0)
        self.layout.addWidget(self.timecode_spinbox_b, 1, 1)


        self.layout.addWidget(self.lock_timecode_checkbox, 2, 1)
        self.layout.addWidget(self.ouput_folder_button, 2, 0)
        self.layout.addWidget(self.export_button, 2, 2)

        self.layout.addWidget(self.ouput_log, 3, 0)

        self.layout.addWidget(self.button_open_picture_a, 4, 0)
        self.layout.addWidget(self.button_open_picture_b, 4, 1)
        # endregion

        self.setLayout(self.layout)

    def init_events(self):
        self.ouput_folder_button.clicked.connect(self.on_ouput_folder_button_clicked)
        self.export_button.clicked.connect(self.on_export_button_pressed)

        self.button_filechooser_a.clicked.connect(self.file_chooser)
        self.button_filechooser_b.clicked.connect(self.file_chooser)

    def file_chooser(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select a file", None, "Video files (*.mp4 *.mkv *.avi)")
        button_text = self.sender().text()

        if filename:
            if(button_text == "File A"):
                self.filename_a = filename

            elif(button_text == "File B"):
                self.filename_b = filename

    def on_timecode_changed(self, timecode_id):
        if self.lock_timecode_checkbox.isChecked():
            if(timecode_id == "a"):
                self.timecode_spinbox_b.setDateTime(self.timecode_spinbox_a.dateTime())

            elif(timecode_id == "b"):
                self.timecode_spinbox_a.setDateTime(self.timecode_spinbox_b.dateTime())

    def on_ouput_folder_button_clicked(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, "Select a output folder", None)

    def open_picture(self, picture_id):
        pictures = {"a": self.output_filepath_a,
                    "b": self.output_filepath_b}

        command = ["xdg-open", "\"{}\"".format(pictures[picture_id])]
        print(command)
        os.system(command)

    def on_export_button_pressed(self):
        self.ouput_log.setText("")
        output_msg = ""

        if self.output_folder:
            if self.filename_a:
                timecode = self.timecode_spinbox_a.dateTime().toString(DATETIME_FORMAT)
                self.output_filepath_a = ffmpeg_screenshot.extract_frame_at(self.filename_a, timecode, self.output_folder)
                output_msg += "\nFile A: {}".format(self.output_filepath_a)

            if self.filename_b:
                timecode = self.timecode_spinbox_b.dateTime().toString(DATETIME_FORMAT)
                self.output_filepath_b = ffmpeg_screenshot.extract_frame_at(self.filename_b, timecode, self.output_folder)
                output_msg += "\nFile B: {}".format(self.output_filepath_b)

            self.ouput_log.setText(output_msg)

        #if not self.filename_a and not self.filename_b:
            #QMessageBox.information(self, "Minimum of one file required", "Please select a file")

    def save_settings(self):
        pass

    def load_settings(self):
        pass

def main():
    app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()