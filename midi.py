import mido

print("welcome to the game")

existing_sequence = []
midi_file = mido.MidiFile('test.mid')

for i, track in enumerate(midi_file.tracks):
    for msg in track:
        if type(msg) is not mido.MetaMessage:
            existing_sequence.append(msg)

print(existing_sequence)

# Function to compare two MIDI sequences
def compare_midi_sequences(midi_file_path, real_time_sequence):
    print(real_time_sequence[-1].note)
    print(existing_sequence[len(real_time_sequence)-1].note)

    if real_time_sequence[-1].note == existing_sequence[len(real_time_sequence)-1].note:
        print("good job")
    else:
        print("you suck")


# Real-time MIDI input
with mido.open_input('V25 Out') as port:
    real_time_sequence = []

    for msg in port:
        print(msg)
        print(msg.time)

        real_time_sequence.append(msg)
        real_time_sequence = list(real_time_sequence)

        midi_file_path = 'test.mid'
        compare_midi_sequences(midi_file_path, real_time_sequence)
