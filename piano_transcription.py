import os
import numpy as np
import librosa
import urllib.request
from piano_transcription_inference import PianoTranscription
 
modelDir  = os.path.join(os.path.expanduser("~"), "piano_transcription_inference_data")
modelPath = os.path.join(modelDir, "CRNN_note_F1=0.9677_pedal_F1=0.9186.pth")
modelUrl  = "https://zenodo.org/record/4034264/files/CRNN_note_F1%3D0.9677_pedal_F1%3D0.9186.pth?download=1"
 
 
def downloadMODEL():
    """Download the pretrained model if it isn't already on disk."""
    if os.path.exists(modelPath):
        return
    os.makedirs(modelDir, exist_ok=True)
    print("Downloading model (~165MB), this only happens once...")
    urllib.request.urlretrieve(modelUrl, modelPath)
    print("Download complete.")
 
 
def transcribe(audio_path, output_midi_path):
    downloadMODEL()
 
    os.makedirs(os.path.dirname(output_midi_path), exist_ok=True)
 
    audio, _ = librosa.load(audio_path, sr=16000, mono=True)
    audio = audio.astype(np.float32)
 
    transcriptor = PianoTranscription(device='cpu', checkpoint_path=modelPath)
    transcriptor.transcribe(audio, output_midi_path)
 
    return output_midi_path
