import mido
import time

print("Welcome to KeyPerfection!")

existing_sequence = []
midi_file = mido.MidiFile('test.mid')

ticks_per_beat = midi_file.ticks_per_beat
current_tempo = 500000  

count = 0
start_time = -1

time_tracker = 0
real_time = []

score = 0

for i, track in enumerate(midi_file.tracks):
    for msg in track:
        if type(msg) is not mido.MetaMessage:
            time_tracker += mido.tick2second(msg.time, ticks_per_beat, current_tempo)
            if msg.type == "note_on":
                real_time.append(time_tracker)
                existing_sequence.append(msg)

# Function to compare two MIDI sequences
def compare_midi_sequences(midi_file_path, real_time_sequence):
    global count, start_time, score

    if count == 0:
        start_time = time.time()
        count = 1
        diff = 0.0
    else:
        end_time = time.time()
        diff = end_time - start_time     
    if real_time_sequence[-1].note == existing_sequence[len(real_time_sequence)-1].note:
        if abs(diff - real_time[len(real_time_sequence) - 1]) > 0.75:
            print("wrong rhythm")
            return False
        else:
            print("correct!")
            score += 1
            return True
    else:
        print("wrong note")
        return False


# Real-time MIDI input
PORT_NAME_WINDOW = "MIDIIN2 (V25) 1"
PORT_NAME_MAC = "V25 Out"

with mido.open_input(PORT_NAME_MAC) as port:
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
                done = compare_midi_sequences(midi_file_path, real_time_sequence)
                if not done:
                    break

print("Good job! Your score is: ", score)