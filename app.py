from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import logging
import whisper
import os

# Log:
logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)


# Choose file function:
def choose_file():
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[
            ("Audio/Video Files", "*.wav *.mp3 *.mp4 *.avi"),
            ("All Files", "*.*"),
        ],
    )

    if file_path:
        file_label.config(text=file_path)
        transcribe_button.config(state=NORMAL)
    return file_path


# Transcribe function:
def transcribe():
    try:
        # Extracting path from the input file:
        input_dir = os.path.dirname(choose_file())

        # Constructing the output file path:
        output_file_path = os.path.join(input_dir, f"{choose_file()}.txt")

        model = whisper.load_model("base")
        result = model.transcribe(choose_file())
        print(result["text"])
    # Showing errors directly in the GUI, in red:
    except Exception as e:
        return f"An error occurred: {e}"


# Setting up the main app window:
root = Tk()
root.title("Transcription of your audio file")

# Creating a 'frame' widget which will hold the content of the UI:
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Creating the button to choose the file:
file_label = Label(root, text="No file selected", width=50)
file_label.pack()

choose_button = Button(root, text="Choose File", command=choose_file())
choose_button.pack()

transcribe_button = Button(
    root, text="Transcribe", command=transcribe(), state=DISABLED
)
transcribe_button.pack()
