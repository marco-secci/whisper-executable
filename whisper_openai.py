# ======= #
# IMPORTS #
# ======= #
# Gui stuff:
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

# AI stuff:
import whisper
import torch

# System stuff:
import logging
import threading
import subprocess
import os

logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)


class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        root.title("Whisper Transcription")

        self.file_label = tk.Label(root, text="No file selected", width=50)
        self.file_label.pack()

        self.choose_button = tk.Button(
            root, text="Choose File", command=self.choose_file
        )
        self.choose_button.pack()

        self.transcribe_button = tk.Button(
            root, text="Transcribe", command=self.transcribe, state=tk.DISABLED
        )
        self.transcribe_button.pack()

        self.transcription_label = tk.Label(root, text="")
        self.transcription_label.pack()

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio/Video Files", "*.wav *.mp3 *.mp4 *.avi"),
                ("All Files", "*.*"),
            ],
        )
        # Enable the transcribe button
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=file_path)
            self.transcribe_button.config(state=tk.NORMAL)

    def transcribe(self):
        self.transcription_label.config(text="Transcribing...", fg="blue")
        # Move the long-running task to a separate thread
        threading.Thread(target=self.transcribe_audio).start()

    def transcribe_audio(self):
        try:
            logging.info("Transcription started.")

            # Load the Whisper model (assuming the model exists)
            model = whisper.load_model("base")

            # Transcribe the audio
            result = model.transcribe(self.file_path)

            # Update the GUI
            self.transcription_label.config(
                text=f"Transcription Completed: {result['text']}", fg="green"
            )

            logging.info("Transcription completed.")

        except Exception as e:
            # Update the GUI
            self.transcription_label.config(text=f"An error occurred: {e}", fg="red")

            # Log the error
            logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
