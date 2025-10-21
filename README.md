# Note Generator - Whisper AI Transcription

A Python class for transcribing audio recordings into text notes using OpenAI's Whisper AI model.

## Features

- Support for multiple Whisper model sizes (tiny, base, small, medium, large)
- Automatic GPU/CPU detection
- Multiple audio format support (mp3, wav, m4a, flac, ogg, mp4, webm)
- Timestamp extraction for detailed transcriptions
- Easy-to-use API for common transcription tasks
- Save transcriptions directly to text files

## Installation

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
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from whisper_transcriber import WhisperTranscriber

# Create a transcriber instance
transcriber = WhisperTranscriber(model_size='base')

# Transcribe an audio file
text = transcriber.transcribe_to_text('recording.mp3')
print(text)
```

### Advanced Usage

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

## API Reference

### WhisperTranscriber

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

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- OGG (.ogg)
- MP4 (.mp4)
- WebM (.webm)

## Example Script

See `example.py` for a complete working example.

## Requirements

- Python 3.8+
- FFmpeg (system dependency)
- PyTorch
- OpenAI Whisper

## Troubleshooting

### CUDA Out of Memory

If you encounter CUDA out of memory errors, try:
- Using a smaller model size
- Using CPU instead: `WhisperTranscriber(model_size='base', device='cpu')`

### FFmpeg Not Found

Make sure FFmpeg is installed and available in your system PATH.

## License

This project uses OpenAI's Whisper model. Please refer to the [Whisper repository](https://github.com/openai/whisper) for license information.
