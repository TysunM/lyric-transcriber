"""
Lyric Transcription Backend Server
This Flask server provides real vocal separation and transcription capabilities.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
import whisper
from demucs.pretrained import get_model
from demucs.apply import apply_model
import torch
import torchaudio

app = Flask(__name__)
CORS(app)

# Load models (do this once at startup)
print("Loading models... This may take a minute...")
whisper_model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
demucs_model = get_model('htdemucs')
print("Models loaded successfully!")

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'lyric_transcriber_full.html')

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    """
    Main endpoint that:
    1. Receives audio file
    2. Separates vocals using Demucs
    3. Transcribes vocals using Whisper
    4. Returns lyrics as text
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']

        # Save uploaded file
        temp_input = os.path.join(UPLOAD_FOLDER, 'input.mp3')
        audio_file.save(temp_input)

        # Step 1: Separate vocals from music
        print("Separating vocals from music...")
        vocal_path = separate_vocals(temp_input)

        # Step 2: Transcribe vocals
        print("Transcribing lyrics...")
        lyrics = transcribe_vocals(vocal_path)

        # Cleanup
        os.remove(temp_input)
        if os.path.exists(vocal_path):
            os.remove(vocal_path)

        return jsonify({
            'success': True,
            'lyrics': lyrics
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def separate_vocals(audio_path):
    """
    Separate vocals from background music using Demucs
    Returns path to isolated vocals
    """
    # Load audio
    wav, sr = torchaudio.load(audio_path)

    # Resample to 44.1kHz if needed (Demucs requirement)
    if sr != 44100:
        resampler = torchaudio.transforms.Resample(sr, 44100)
        wav = resampler(wav)

    # Apply Demucs model
    with torch.no_grad():
        sources = apply_model(demucs_model, wav[None], device='cpu')[0]

    # Extract vocals (index 3 in htdemucs output: drums, bass, other, vocals)
    vocals = sources[3]

    # Save vocals
    vocal_path = os.path.join(OUTPUT_FOLDER, 'vocals.wav')
    torchaudio.save(vocal_path, vocals.cpu(), 44100)

    return vocal_path

def transcribe_vocals(vocal_path):
    """
    Transcribe vocals to text using Whisper
    """
    result = whisper_model.transcribe(
        vocal_path,
        language='en',  # Change if needed, or use None for auto-detection
        task='transcribe',
        fp16=False  # Set to True if you have a GPU
    )

    # Format the transcription
    lyrics = result['text'].strip()

    return lyrics

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'models_loaded': True})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Lyric Transcription Server")
    print("="*50)
    print("Server starting on http://0.0.0.0:5000")
    print("="*50 + "\n")

    # Run server accessible on your network
    app.run(host='0.0.0.0', port=5000, debug=False)
