import os
import yt_dlp
import demucs.separate
import funcs
from piano_transcription import transcribe
from flask import jsonify


from flask import (
    Flask,
    redirect,
    url_for,
    render_template,
    request,
    session, 
    flash,
    jsonify 
)

app = Flask(__name__)
app.secret_key = "test"


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        try:
            usrLink = request.form.get("user_input")
            usrFile = request.files.get("audioFile")         
            fileName = request.form.get("fileName")
            soloPiece = request.form.get("soloPiece")

            session["temp"] = usrFile
            
            if usrLink:
                audioFile = funcs.downloadAudio(usrLink, fileName)
            if usrFile:
                fileExt = os.path.splitext(usrFile.filename)[1]
                audioFile = os.path.join(funcs.audioDir, f"{fileName}{fileExt}")
                usrFile.save(audioFile)
            

            if soloPiece:
                pianoStem = audioFile
            else:
                # demucs implementation kept here since its one line
                demucs.separate.main(["-n", "htdemucs_6s", "--two-stems", "piano", "--out", funcs.stemsDir, audioFile])
                pianoStem = os.path.join(funcs.stemsDir, "htdemucs_6s", fileName, "piano.wav")
                
            transcribe(pianoStem, os.path.join(funcs.midiDir, f"{fileName}.mid"))

    
            return redirect(url_for("home"))

        except yt_dlp.utils.DownloadError as de:
            flash("Failed to download video")
            return redirect(url_for("home"))
        
        except SystemExit:
            
            return redirect(url_for("home"))
    else:  
        flash("Welcome!")
        return render_template("home.html")

@app.route("/clrDir", methods=["POST"])
def run_function():
    funcs.clearDir()
    return jsonify({"message": "Files cleared"})

if __name__ == "__main__":
    app.run(debug=True)
