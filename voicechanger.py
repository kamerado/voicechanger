import pyaudio
import PySimpleGUI as sg
import numpy as np
import threading


def voice_window(DEVICE):
    layout = [
        [sg.Button("Start", key="-START-"), sg.Button("Stop", key="-STOP-")],
        [sg.Output(size=(20, 5))]
    ]
    window = sg.Window("Voice Changer", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-START-':
            threading.Thread(target=start_voice_changer, args=(DEVICE), daemon=True).start()
        if event == '-STOP-':
            break
    
    window.close()

def main():

    layout1 = [
        [sg.Text("search for input device you wish to use."), sg.Button("Search", key="-SEARCH-")],
        [sg.Output(size=(60,5))],
        [sg.Text('select'), sg.Input(key='-DEVICE-')],
        [sg.Button("Select device index", key = "-SELECT-"), sg.Button('Exit')]
    ]
    
    layout2 = [
        []
    ]

    window = sg.Window('Select audio device', layout1, finalize=True)
    while True:             # Event Loop
        event, values = window.Read()
        output = str(finddevices())
        print(output)
        if event == sg.WIN_CLOSED:
            break
        if event == "-SELECT-":
            voice_window(values["-DEVICE-"])
        if event == 'Exit':
            break
            
    
    window.close()

# This function finds available audio sources and display it in the GUI.
def finddevices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    
def start_voice_changer(input):
    # Parameters for audio processing
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    DEVICE = int(input)
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=DEVICE)

    while True:
        try:
            # Read audio input
            input_data = stream.read(CHUNK)

            # Convert to NumPy array
            audio_data = np.frombuffer(input_data, dtype=np.int16)

            # Modify the pitch
            new_audio_data = np.interp(np.arange(0, len(audio_data), 2), np.arange(0, len(audio_data), 1), audio_data)

            # Convert back to bytes
            output_data = new_audio_data.astype(np.int16).tobytes()

            # Play modified audio
            stream.write(output_data)

        except KeyboardInterrupt:
            break

    #stream.stop_stream()
    #stream.close()
    #p.terminate()

if __name__ == '__main__':
    main()