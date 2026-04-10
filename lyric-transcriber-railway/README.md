# Lyric Transcriber - Setup Guide

## What You Get

A complete web-based lyric transcription system with:
- **Vocal Separation**: Automatically isolates vocals from background music using Demucs AI
- **High-Accuracy Transcription**: Uses OpenAI's Whisper AI to convert vocals to text
- **Mobile-Friendly**: Works perfectly on your Android browser
- **Offline Capable**: Once set up, can run without internet

## Two Versions Included

### 1. Demo Version (lyric_transcriber.html)
- Frontend-only demonstration
- Shows you the UI/UX
- No actual transcription (browser limitations)
- **Use this to**: See what the final app looks like

### 2. Full Version (Complete System)
- **Backend**: Python server with AI models (backend_server.py)
- **Frontend**: Web interface (lyric_transcriber_full.html)
- **Real transcription**: Actually separates vocals and transcribes lyrics
- **Use this for**: Actual lyric transcription

---

## Setup Instructions

### Option A: Run on Your Computer (Recommended for Beginners)

#### Step 1: Install Python
1. Download Python 3.10+ from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"

#### Step 2: Install Dependencies
Open Terminal (Mac/Linux) or Command Prompt (Windows):

```bash
# Navigate to the folder with your files
cd /path/to/lyric-transcriber

# Install required libraries
pip install -r requirements.txt
```

**Note**: This download is about 2-3 GB (includes AI models). Takes 10-30 minutes depending on internet speed.

#### Step 3: Run the Server
```bash
python backend_server.py
```

You'll see:
```
==================================================
Lyric Transcription Server
==================================================
Server starting on http://localhost:5000
Open this URL in your Android browser
==================================================
```

#### Step 4: Use on Your Android
1. Make sure your Android is on the **same WiFi network** as your computer
2. Find your computer's IP address:
   - **Windows**: Open Command Prompt, type `ipconfig`, look for "IPv4 Address"
   - **Mac**: System Preferences → Network → look for IP address
   - **Linux**: Type `hostname -I` in terminal

3. On your Android browser, go to:
   ```
   http://YOUR_COMPUTER_IP:5000
   ```
   Example: `http://192.168.1.105:5000`

4. Upload a song and start transcribing!

---

### Option B: Deploy to a Cloud Server (Advanced)

For access anywhere, not just your home network:

#### Free Options:
1. **Render.com** (500 free hours/month)
2. **Railway.app** (Free tier available)
3. **Google Cloud / AWS** (Free tier for first year)

#### Quick Deploy to Render:
1. Create account at render.com
2. Create new "Web Service"
3. Connect your GitHub repo or upload files
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python backend_server.py`
6. Deploy!
7. Access from anywhere using your Render URL

---

## How to Use

### Step 1: Open the App
Navigate to `http://localhost:5000` (or your server URL) in your Android browser

### Step 2: Upload Audio
- Click the upload area or drag-and-drop
- Supports: MP3, WAV, M4A, OGG, FLAC
- Works with any song (vocals + music or acapella)

### Step 3: Transcribe
- Click "Start Transcription"
- Wait 1-3 minutes (depends on song length)
- Watch the progress bar

### Step 4: Get Your Lyrics
- Copy to clipboard
- Download as .txt file
- Transcribe another song

---

## Troubleshooting

### "Server Offline" message
- Make sure you ran `python backend_server.py`
- Check that no firewall is blocking port 5000
- Verify you're using the correct IP address

### Slow transcription
- First run downloads AI models (~2GB) - this is normal
- Song length affects processing time (3-minute song = ~2 minutes processing)
- Close other programs to free up RAM

### "Out of memory" error
- Large audio files (>10MB) need more RAM
- Try converting to MP3 with lower bitrate first
- Close other applications

### Poor transcription quality
- Works best with clear vocals
- Heavy autotune or vocal effects may reduce accuracy
- Multiple singers can confuse the AI
- Non-English songs: Change `language='en'` to your language in backend_server.py

---

## Technical Details

### What's Happening Behind the Scenes

1. **Upload**: Song sent to server
2. **Vocal Separation**: Demucs AI separates the song into 4 stems:
   - Drums
   - Bass
   - Other instruments
   - **Vocals** (this is what we keep)
3. **Transcription**: Whisper AI converts vocal audio to text
4. **Return**: Lyrics sent back to your browser

### Models Used
- **Demucs htdemucs**: State-of-the-art vocal separation
- **Whisper base**: Fast, accurate speech recognition
  - Can upgrade to 'medium' or 'large' for better accuracy (but slower)

### Supported Languages
Whisper supports 90+ languages including:
English, Spanish, French, German, Italian, Portuguese, Dutch, Russian, Arabic, Hindi, Japanese, Korean, Chinese, and many more.

To change language, edit line 73 in `backend_server.py`:
```python
language='en',  # Change to 'es', 'fr', 'ja', etc. or None for auto-detect
```

---

## Customization

### Use Better AI Models

Edit `backend_server.py` line 18:
```python
# Faster, less accurate:
whisper_model = whisper.load_model("tiny")

# Balanced (default):
whisper_model = whisper.load_model("base")

# More accurate, slower:
whisper_model = whisper.load_model("medium")

# Best quality, very slow:
whisper_model = whisper.load_model("large")
```

### Add Timestamps

Uncomment lines 97-101 in `backend_server.py` to get:
```
[00:15 - 00:18] First line of lyrics
[00:18 - 00:22] Second line of lyrics
```

### Change Port

Edit line 122 in `backend_server.py`:
```python
app.run(host='0.0.0.0', port=8080, debug=True)  # Changed from 5000 to 8080
```

---

## File Structure

```
lyric-transcriber/
├── lyric_transcriber_full.html     # Full version (connects to backend)
├── backend_server.py               # Python server with AI models
├── requirements.txt                # Python dependencies
├── Procfile                        # Railway deployment configuration
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## Performance Expectations

| Song Length | Processing Time | File Size Limit |
|-------------|-----------------|-----------------|
| 1-2 minutes | ~1 minute       | Up to 10 MB     |
| 3-4 minutes | ~2 minutes      | Up to 20 MB     |
| 5+ minutes  | ~3-4 minutes    | Up to 50 MB     |

**Hardware Requirements:**
- Minimum: 4GB RAM, dual-core CPU
- Recommended: 8GB RAM, quad-core CPU
- With GPU: 10x faster (NVIDIA GPU with CUDA)

---

## Privacy & Security

- All processing happens locally on your server
- No data sent to external services
- Audio files deleted after transcription
- No logs kept (unless you enable debugging)

---

## Future Enhancements

Potential features to add:
- [ ] Batch processing (multiple songs at once)
- [ ] Speaker diarization (identify different singers)
- [ ] Export to SRT/LRC format (for karaoke)
- [ ] Real-time transcription (for live performances)
- [ ] Language detection and auto-translation
- [ ] Integration with Spotify/Apple Music

---

## Credits

Built using:
- **OpenAI Whisper**: Speech recognition
- **Demucs**: Vocal separation by Meta AI
- **Flask**: Web server
- **PyTorch**: Machine learning framework

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all dependencies installed correctly
3. Try with a shorter, simpler audio file first
4. Check Python and library versions match requirements

---

## License

Free for personal use. AI models have their own licenses:
- Whisper: MIT License
- Demucs: MIT License

---

Enjoy transcribing your lyrics! 🎵
