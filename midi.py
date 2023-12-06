import mido
import time

print("Welcome to KeyPerfection!")

# existing_sequence = []
# midi_file = mido.MidiFile('test.mid')

# ticks_per_beat = midi_file.ticks_per_beat
# current_tempo = 500000  

# count = 0
# start_time = -1

# time_tracker = 0
# real_time = []

# score = 0


# Real-time MIDI input
# PORT_NAME_WINDOW = "MIDIIN2 (V25) 1"
# PORT_NAME_MAC = "V25 Out"

import tkinter as tk
from tkinter import ttk

class KeyPerfectionGUI:
    
    def __init__(self, root):
        self.PORT_NAME_WINDOW = "MIDIIN2 (V25) 1"
        self.PORT_NAME_MAC = "V25 Out"
        self.root = root
    
        self.existing_sequence = []
        self.midi_file = mido.MidiFile('test.mid')
        self.ticks_per_beat = self.midi_file.ticks_per_beat
        self.current_tempo = 500000  
        self.count = 0
        self.start_time = -1
        self.time_tracker = 0
        self.real_time = []
        self.score = 0
        

        self.root.title("Welcome to KeyPerfection")

        # Create a label with the welcome message
        self.label = tk.Label(root, text="Welcome to KeyPerfection", font=("Arial", 16))
        self.label.pack(pady=20)

        # Create a dropdown menu with 5 songs
        self.song_options = ["Song 1", "Song 2", "Song 3", "Song 4", "Song 5"]
        self.song_var = tk.StringVar()
        self.song_var.set(self.song_options[0])

        self.song_dropdown = ttk.Combobox(root, textvariable=self.song_var, values=self.song_options)
        self.song_dropdown.pack(pady=10)

        # Create a "Start" button
        self.start_button = tk.Button(root, text="Start", command=self.start_game)
        self.start_button.pack(pady=10)

        # Load Midi file
        for i, track in enumerate(self.midi_file.tracks):
            for msg in track:
                if type(msg) is not mido.MetaMessage:
                    self.time_tracker += mido.tick2second(msg.time, self.ticks_per_beat, self.current_tempo)
                    if msg.type == "note_on":
                        self.real_time.append(self.time_tracker)
                        self.existing_sequence.append(msg)

    # Function to compare two MIDI sequences
    def compare_midi_sequences(self, midi_file_path, real_time_sequence):
        # global count, start_time, score

        if self.count == 0:
            self.start_time = time.time()
            self.count = 1
            diff = 0.0
        else:
            end_time = time.time()
            diff = end_time - self.start_time     
        if real_time_sequence[-1].note == self.existing_sequence[len(real_time_sequence)-1].note:
            if abs(diff - self.real_time[len(real_time_sequence) - 1]) > 0.75:
                print("wrong rhythm")
                return False
            else:
                print("correct!")
                self.score += 1
                return True
        else:
            print("wrong note")
            return False
            
    def start_game(self):
        selected_song = self.song_var.get()
        print(f"Starting game for {selected_song}!")

        with mido.open_input(self.PORT_NAME_MAC) as port:
            done = False
            while not done:
                score = 0
                real_time_sequence = []
                count = 0
                for msg in port:
                    if msg.type == "note_on":
                        real_time_sequence.append(msg)
                        real_time_sequence = list(real_time_sequence)
                        midi_file_path = 'test.mid'
                        done = self.compare_midi_sequences(midi_file_path, real_time_sequence)
                        if not done:
                            print("restarting")
                            break

        print("Good job! Your score is: ", score)

if __name__ == "__main__":
    root = tk.Tk()
    gui = KeyPerfectionGUI(root)
    root.mainloop()