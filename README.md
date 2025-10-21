# Note Generator - Whisper AI Transcription

A Python library for transcribing audio recordings into text notes using OpenAI's Whisper AI model.

**Two implementations available:**
- **Local**: Run Whisper models locally on your machine (free, private, offline)
- **API**: Use OpenAI's cloud API (fast, requires API key, pay-per-use)

## Features

### Local Implementation (`whisper_transcriber.py`)
- Support for multiple Whisper model sizes (tiny, base, small, medium, large)
- Automatic GPU/CPU detection
- Runs completely offline after initial model download
- Free, unlimited usage
- Privacy - audio never leaves your machine

### API Implementation (`whisper_api_transcriber.py`)
- Fast cloud-based transcription
- No local GPU/CPU resources needed
- Additional subtitle formats (SRT, VTT)
- Translation to English from any language
- Requires OpenAI API key

### Common Features
- Multiple audio format support (mp3, wav, m4a, flac, ogg, mp4, webm)
- Timestamp extraction for detailed transcriptions
- Easy-to-use API for common transcription tasks
- Save transcriptions directly to text files

## Installation

### For Local Implementation

1. Install system dependencies (FFmpeg is required):

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (using chocolatey)
choco install ffmpeg
```

2. Install Python dependencies:

```bash
# Install only local dependencies
pip install openai-whisper torch numpy ffmpeg-python
```

### For API Implementation

```bash
# Install only API dependencies
pip install openai
```

### For Both Implementations

```bash
# Install all dependencies
pip install -r requirements.txt
```

## Quick Start

### Option 1: Local Implementation

```python
from whisper_transcriber import WhisperTranscriber

# Create a transcriber instance
transcriber = WhisperTranscriber(model_size='base')

# Transcribe an audio file
text = transcriber.transcribe_to_text('recording.mp3')
print(text)
```

### Option 2: API Implementation

```python
from whisper_api_transcriber import WhisperAPITranscriber

# Set your API key (or use OPENAI_API_KEY environment variable)
transcriber = WhisperAPITranscriber(api_key='your-api-key-here')

# Transcribe an audio file
text = transcriber.transcribe_to_text('recording.mp3')
print(text)
```

## Usage Examples

### Local Implementation - Advanced

```python
from whisper_transcriber import WhisperTranscriber

# Initialize with a specific model and device
transcriber = WhisperTranscriber(model_size='medium', device='cuda')

# Get full transcription with metadata
result = transcriber.transcribe('recording.mp3', language='en')
print(result['text'])
print(f"Detected language: {result['language']}")

# Get transcription with timestamps
segments = transcriber.transcribe_with_timestamps('recording.mp3')
for segment in segments:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")

# Save transcription to file
transcriber.save_transcription(
    'recording.mp3',
    'transcription.txt',
    include_timestamps=True
)
```

### API Implementation - Advanced

```python
from whisper_api_transcriber import WhisperAPITranscriber
import os

# Use environment variable for API key
os.environ['OPENAI_API_KEY'] = 'your-api-key-here'
transcriber = WhisperAPITranscriber()

# Simple transcription
text = transcriber.transcribe_to_text('recording.mp3')
print(text)

# Get transcription with timestamps
segments = transcriber.transcribe_with_timestamps('recording.mp3')
for segment in segments:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")

# Save as SRT subtitle file
transcriber.save_transcription(
    'recording.mp3',
    'subtitles.srt',
    format='srt'
)

# Translate non-English audio to English
result = transcriber.translate('spanish_audio.mp3')
print(result['text'])
```

## Model Sizes

Choose a model size based on your needs:

| Model  | Parameters | Relative Speed | Relative Accuracy |
|--------|------------|----------------|-------------------|
| tiny   | 39 M       | Fastest        | Good              |
| base   | 74 M       | Fast           | Better            |
| small  | 244 M      | Moderate       | Good              |
| medium | 769 M      | Slower         | Very Good         |
| large  | 1550 M     | Slowest        | Best              |

**Recommendation**: Start with `base` for a good balance of speed and accuracy.

## Which Implementation Should I Use?

| Feature | Local | API |
|---------|-------|-----|
| **Cost** | Free | ~$0.006/minute |
| **Speed** | Slower (depends on hardware) | Very fast |
| **Privacy** | Complete (offline) | Audio sent to OpenAI |
| **Internet** | Only for initial download | Required |
| **Hardware** | GPU recommended | None needed |
| **API Key** | Not needed | Required |
| **Max File Size** | No limit | 25 MB |
| **Best For** | Privacy, bulk processing, offline use | Quick tasks, no GPU available |

## API Reference

### WhisperTranscriber (Local)

#### `__init__(model_size='base', device=None)`

Initialize the transcriber.

- `model_size`: Model size to use ('tiny', 'base', 'small', 'medium', 'large')
- `device`: Device to run on ('cuda' or 'cpu'). Auto-detected if None.

#### `transcribe(audio_input, language=None, task='transcribe', **kwargs)`

Transcribe an audio file and return full results.

- `audio_input`: Path to audio file
- `language`: Language code (e.g., 'en', 'es'). Auto-detected if None.
- `task`: Either 'transcribe' or 'translate' (to English)
- Returns: Dictionary with 'text', 'segments', and 'language'

#### `transcribe_to_text(audio_input, language=None, **kwargs)`

Transcribe and return only the text string.

#### `transcribe_with_timestamps(audio_input, language=None, **kwargs)`

Transcribe and return list of segments with timestamps.

#### `save_transcription(audio_input, output_path, language=None, include_timestamps=False, **kwargs)`

Transcribe and save to a file.

---

### WhisperAPITranscriber (Cloud API)

#### `__init__(api_key=None, model='whisper-1')`

Initialize the API transcriber.

- `api_key`: OpenAI API key (or use OPENAI_API_KEY env variable)
- `model`: Model to use (currently only 'whisper-1' available)

#### `transcribe(audio_input, language=None, prompt=None, response_format='json', temperature=0.0)`

Transcribe an audio file using the API.

- `audio_input`: Path to audio file
- `language`: Language code (e.g., 'en', 'es')
- `prompt`: Optional text to guide transcription style
- `response_format`: 'json', 'text', 'srt', 'verbose_json', or 'vtt'
- `temperature`: Sampling temperature (0.0-1.0)

#### `transcribe_to_text(audio_input, language=None, **kwargs)`

Transcribe and return only the text string.

#### `transcribe_with_timestamps(audio_input, language=None, **kwargs)`

Transcribe and return list of segments with timestamps.

#### `transcribe_to_srt(audio_input, language=None, **kwargs)`

Transcribe and return SRT subtitle format.

#### `transcribe_to_vtt(audio_input, language=None, **kwargs)`

Transcribe and return WebVTT subtitle format.

#### `save_transcription(audio_input, output_path, language=None, include_timestamps=False, format='text', **kwargs)`

Transcribe and save to a file.

#### `translate(audio_input, prompt=None, response_format='json', temperature=0.0)`

Translate audio to English (works with any language).

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- OGG (.ogg)
- MP4 (.mp4)
- WebM (.webm)

## Example Scripts

- `example.py` - Complete examples for local implementation
- `example_api.py` - Complete examples for API implementation

## Requirements

- Python 3.8+
- FFmpeg (system dependency)
- PyTorch
- OpenAI Whisper

## Getting an OpenAI API Key

To use the API implementation:

1. Go to [OpenAI's website](https://platform.openai.com/signup)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Set it as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Troubleshooting

### Local Implementation

**CUDA Out of Memory**
- Use a smaller model size
- Use CPU instead: `WhisperTranscriber(model_size='base', device='cpu')`

**FFmpeg Not Found**
- Make sure FFmpeg is installed and available in your system PATH

### API Implementation

**Authentication Error**
- Verify your API key is correct
- Check that OPENAI_API_KEY environment variable is set

**File Too Large**
- API has a 25 MB file size limit
- Consider using local implementation for large files
- Or compress/split your audio file

**Rate Limiting**
- OpenAI API has rate limits
- Add delays between requests if processing multiple files

## License

This project uses OpenAI's Whisper model. Please refer to the [Whisper repository](https://github.com/openai/whisper) for license information.
