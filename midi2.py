import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap

import mido
import time
import threading

class ScoreUpdaterThread(threading.Thread):
    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance
        self.stop_event = threading.Event()

    def run(self):
        with mido.open_input(self.app_instance.PORT_NAME_MAC) as port:
            while not self.stop_event.is_set():
                real_time_sequence = []
                self.app_instance.count = 0
                game_done = False
                for msg in port:
                    if msg.type == "note_on":
                        real_time_sequence.append(msg)
                        real_time_sequence = list(real_time_sequence)
                        midi_file_path = 'test.mid'
                        note_done, game_done = self.app_instance.compare_midi_sequences(midi_file_path, real_time_sequence)
                        if not note_done: # if you did not play the note correctly
                            print("restarting")
                            break
                        if game_done:
                            break
                if game_done:
                    break
                
        print("game done")
                        
    def stop(self):
        self.stop_event.set()

class HelloWorldApp(QWidget):
    def __init__(self):
        super().__init__()

        self.PORT_NAME_WINDOW = "MIDIIN2 (V25) 1"
        self.PORT_NAME_MAC = "V25 Out"

        self.label_score = QLabel("Score: 0")
        self.label_game_done = QLabel("Good luck!")
        self.label_game_done.setStyleSheet("color: red; font: bold 16pt;")

        self.existing_sequence = []
        self.midi_file = mido.MidiFile('test.mid')
        self.ticks_per_beat = self.midi_file.ticks_per_beat
        self.current_tempo = 500000
        self.count = 0
        self.start_time = -1
        self.time_tracker = 0
        self.real_time = []
        self.score = 0

        self.game_done = False

        self.label = QLabel("Welcome to Key Perfection!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: blue; font: bold 16pt;")

        image_path = "thing.png"  # Replace with the actual path to your image
        pixmap = QPixmap(image_path) 
        # pixmap.show()

        img = QLabel(self)
        img.setPixmap(pixmap)
        

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.label_game_done)
        layout.addWidget(self.label_score)
        layout.addWidget(img)
        self.button_start = QPushButton("Start game")
        self.button_start.clicked.connect(self.start_game)
        layout.addWidget(self.button_start)

        self.setLayout(layout)

        self.setWindowTitle("Key Perfection")
        self.setGeometry(100, 100, 300, 150)  # (x, y, width, height)

        for i, track in enumerate(self.midi_file.tracks):
            for msg in track:
                if type(msg) is not mido.MetaMessage:
                    self.time_tracker += mido.tick2second(msg.time, self.ticks_per_beat, self.current_tempo)
                    if msg.type == "note_on":
                        self.real_time.append(self.time_tracker)
                        self.existing_sequence.append(msg)

        self.score_updater_thread = None

    def start_game(self):
        self.score_updater_thread = ScoreUpdaterThread(self)
        self.score_updater_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_score)
        self.timer.start(5)

    def update_score(self):
        if not self.game_done:
            self.label_score.setText(f"Score: {self.score}")

    def reset_score(self):
        # Reset the score to 0
        self.label_score.setText("Score: 0")

    def compare_midi_sequences(self, midi_file_path, real_time_sequence):
        is_done = False
        if self.count == 0:
            self.start_time = time.time()
            self.count = 1
            diff = 0.0
        else:
            end_time = time.time()
            diff = end_time - self.start_time
        if real_time_sequence[-1].note == self.existing_sequence[len(real_time_sequence) - 1].note:
            if abs(diff - self.real_time[len(real_time_sequence) - 1]) > 1.5:
                self.label_game_done.setText("Wrong rhythm")
                print("wrong rhythm")
                self.score = 0
                return False, is_done
            else:
                print("correct!")
                self.label_game_done.setText("Correct")
                if abs(diff - self.real_time[len(real_time_sequence) - 1]) < .5:
                    self.score += 2
                else:
                    self.score += 1
                if len(real_time_sequence) == len(self.existing_sequence):
                    is_done = True
                    self.is_done = True
                    self.label_game_done.setText("GOOD JOB!")
                return True, is_done
        else:
            print("wrong note")
            self.label_game_done.setText("Wrong note")
            self.score = 0
            # QTimer.singleShot(2000, self.reset_score)

            return False, is_done

    def closeEvent(self, event):
        if self.score_updater_thread:
            self.score_updater_thread.stop()
            self.score_updater_thread.join()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    hello_world_app = HelloWorldApp()
    hello_world_app.show()
    sys.exit(app.exec_())
