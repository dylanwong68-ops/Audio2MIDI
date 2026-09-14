import os
import shutil
import yt_dlp

baseDir = os.path.dirname(os.path.abspath(__file__))
audioDir = os.path.join(baseDir, "Audio")
stemsDir = os.path.join(baseDir, "Stems")
midiDir = os.path.join(baseDir, "MIDI")

def createDir():
    if not os.path.exists(audioDir):
        os.makedirs(audioDir)

    if not os.path.exists(stemsDir):
        os.makedirs(stemsDir)

    if not os.path.exists(midiDir):
        os.makedirs(midiDir)
    
def downloadAudio(ytLink, fileName):
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{audioDir}/{fileName}.%(ext)s',
        'noplaylist': True,
        'writedescription': False,
        'noprogress': False,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(ytLink, download=True)
        audioFile = ydl.prepare_filename(info)
    return audioFile

def clearDir():
    for folder in [audioDir, stemsDir]: 
        if os.path.exists(folder):
            shutil.rmtree(folder) # removed entire dir since we can use createDir to reduce lines of code
    createDir() 

        


