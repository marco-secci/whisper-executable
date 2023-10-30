# conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
# whisper .\fine_lez.ogg --language Italian --model small --device cuda --task transcribe

import whisper
import torch

# model = whisper.load_model("base")
# result = model.transcribe("lezione_fli.mp3")
# print(result["text"])
print(torch.cuda.is_available())
