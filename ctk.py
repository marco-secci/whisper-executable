# ======= #
# IMPORTS #
# ======= #
# Gui stuff:
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, ttk

# from pydub import AudioSegment
# from moviepy.editor import VideoFileClip

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
        # Languages available in whisper:
        # TODO the language choice should use the three char version in the code ("ita", "eng", etc)
        self.result = None
        self.file_path = None
        self.languages = [
            "Choose a language",
            "Spanish",
            "Italian",
            "English",
            "Portuguese",
            "German",
            "Japanese",
            "Polish",
            "Russian",
            "Dutch",
            "Indonesian",
            "Catalan",
            "French",
            "Turkish",
            "Swedish",
            "Ukrainian",
            "Malay",
            "Norwegian",
            "Finnish",
            "Vietnamese",
            "Thai",
            "Slovak",
            "Greek",
            "Czech",
            "Croatian",
            "Tagalog",
            "Danish",
            "Korean",
            "Romanian",
            "Bulgarian",
            "Chinese",
            "Galician",
            "Bosnian",
            "Arabic",
            "Macedonian",
            "Hungarian",
            "Tamil",
            "Hindi",
            "Estonian",
            "Urdu",
            "Slovenian",
            "Latvian",
            "Azerbaijani",
            "Hebrew",
            "Lithuanian",
            "Persian",
            "Welsh",
            "Serbian",
            "Afrikaans",
            "Kannada",
            "Kazakh",
            "Icelandic",
            "Marathi",
            "Maori",
            "Swahili",
            "Armenian",
            "Belarusian",
            "Nepali",
        ]

        self.root = root
        root.title("Whisper Transcription")

        self.file_label = ctk.CTkLabel(root, text="No file selected", width=50)
        self.file_label.pack()

        self.choose_button = ctk.CTkButton(
            root, text="Choose File", command=self.choose_file
        )
        self.choose_button.pack()

        self.transcribe_button = ctk.CTkButton(
            root, text="Transcribe", command=self.transcribe, state=ctk.DISABLED
        )
        self.transcribe_button.pack()

        self.transcription_label = ctk.CTkLabel(root, text="")
        self.transcription_label.pack()

        # Choose language button:
        self.language_combobox = ttk.Combobox(
            root, values=self.languages, state="readonly"
        )
        self.language_combobox.current(0)
        self.language_combobox.pack()

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio/Video Files", "*.wav *.mp3 *.mp4 *.avi *.ogg *.aac"),
                ("All Files", "*.*"),
            ],
        )
        # Enable the transcribe button
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=file_path)
            self.transcribe_button.config(state=tk.NORMAL)

    def transcribe(self):
        # Initializing GPU:
        torch.cuda.init()
        # Logging:
        logging.info(f"GPU-CUDA available: {torch.cuda.is_available()} ")
        self.transcription_label.config(text="Transcribing...", fg="blue")
        # Move the long-running task to a separate thread
        threading.Thread(target=self.transcribe_audio).start()

    def transcribe_audio(self):
        try:
            # Logging:
            logging.info("Transcription started.")

            # Selecting language:
            selected_language = self.language_combobox.get()

            # If left to default, whisper will detect on its own the language:
            if selected_language == "Choose a language":
                selected_language = None
            logging.info(f"Language chosen: {selected_language}")

            # Load the Whisper model (only 'base' model is supported as of now):
            model = whisper.load_model("base")

            # Transcribe the audio:
            with torch.cuda.device("cuda"):
                self.result = model.transcribe(
                    self.file_path,
                    language=selected_language,
                    # word_timestamps=True,
                    # fp16=False,
                    # patience=2,
                    # beam_size=5,
                )

            # Logging:
            logging.info(self.result)
            output_file_path = os.path.splitext(self.file_path)[0] + ".txt"

            # Writing the transcription to a text file:
            with open(output_file_path, "w", encoding="utf-8") as f:
                # Going to a newline at every full stop:
                formatted_text = self.result["text"] = self.result["text"].replace(
                    ".", ".\n"
                )

                # Writing the output in the file just created:
                f.write(formatted_text)
                f.flush()

            # Update the GUI:
            self.transcription_label.config(
                text=f"Transcription Completed. ", fg="green"
            )

            logging.info("Transcription completed.")

        except Exception as e:
            # Update the GUI:
            self.transcription_label.config(text=f"An error occurred: {e}", fg="red")

            # Log the error:
            logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = TranscriptionApp(root)
    root.mainloop()
