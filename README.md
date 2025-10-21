# Note Generator - Whisper AI Transcription

A Python library for transcribing audio recordings into text notes using OpenAI's Whisper AI API.

## Features

- **Backend transcription** using OpenAI's Whisper API
- **Note templates** for different formats (study guides, meeting minutes, instructions, etc.)
- **Simple setup** with `.env` file for API key management
- **Multiple audio formats** supported (mp3, wav, m4a, flac, ogg, mp4, webm)
- **Timestamp support** for detailed transcriptions
- **Fast cloud processing** - no local GPU needed
- **Save to file** functionality with automatic directory creation
- **Clean API** focused on core transcription functionality

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management

### 2. Set Up API Key

1. Get your OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

2. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

3. Edit `.env` and add your API key:

```
OPENAI_KEY=your-api-key-here
```

## Quick Start

### Basic Usage

```python
from transcribe import Transcriber

# Initialize transcriber (automatically loads API key from .env)
transcriber = Transcriber()

# Transcribe an audio file
text = transcriber.transcribe_to_text('recording.mp3')
print(text)
```

### Command Line Usage

```bash
# Transcribe a file and save to text
python example_transcribe.py your_recording.mp3
```

## Note Templates

Transform your transcriptions into organized, formatted notes using templates! Choose from 5 different note-taking styles:

### Available Templates

1. **Study Guide** - Comprehensive notes with key concepts, definitions, and examples
2. **Meeting Minutes** - Professional documentation with action items and decisions
3. **Instructions** - Step-by-step tutorials with troubleshooting
4. **Summary** - Concise overview with key points only
5. **Verbatim Transcript** - Word-for-word with timestamps and speaker identification

### Using Templates

```python
from src.transcribe import Transcriber
from src.note_templates import load_template

# Initialize transcriber
transcriber = Transcriber()

# Load a template (study_guide, meeting_minutes, instructions, summary, verbatim_transcript)
prompt = load_template('study_guide')

# Transcribe with the template
result = transcriber.transcribe(
    'lecture.mp3',
    prompt=prompt,
    language='en'
)

# Save the formatted notes
transcriber.save_to_file(result['text'], 'study_notes.txt')
```

### Interactive Template Selection

```bash
# Run the interactive example
python example_with_templates.py your_audio.mp3
```

This will show you all available templates and let you choose which format you want for your notes.

### Template Examples

**Study Guide** - Perfect for lectures and educational content:
```python
prompt = load_template('study_guide')
transcriber.transcribe_and_save('biology_lecture.mp3', 'bio_notes.txt', prompt=prompt)
```

**Meeting Minutes** - For professional meetings:
```python
prompt = load_template('meeting_minutes')
transcriber.transcribe_and_save('team_meeting.mp3', 'minutes.txt', prompt=prompt)
```

**Quick Summary** - For fast overviews:
```python
prompt = load_template('summary')
transcriber.transcribe_and_save('presentation.mp3', 'summary.txt', prompt=prompt)
```

See the [Templates README](templates/README.md) for detailed information on each template and how to customize them.

## API Reference

### Transcriber Class

#### `__init__(api_key=None, model='whisper-1')`

Initialize the transcriber.

- `api_key` (optional): OpenAI API key. If None, loads from `OPENAI_KEY` in `.env` file
- `model`: Whisper model to use (default: 'whisper-1')

#### `transcribe_to_text(audio_input, language=None, **kwargs)`

Transcribe audio and return plain text.

**Args:**
- `audio_input`: Path to audio file
- `language` (optional): Language code (e.g., 'en', 'es', 'fr')
- `**kwargs`: Additional options (prompt, temperature)

**Returns:** `str` - Transcribed text

**Example:**
```python
text = transcriber.transcribe_to_text('meeting.mp3', language='en')
```

#### `transcribe_with_timestamps(audio_input, language=None, **kwargs)`

Transcribe audio with timestamp information for each segment.

**Args:**
- `audio_input`: Path to audio file
- `language` (optional): Language code

**Returns:** `list[dict]` - List of segments with 'start', 'end', and 'text'

**Example:**
```python
segments = transcriber.transcribe_with_timestamps('lecture.mp3')
for segment in segments:
    print(f"[{segment['start']:.2f}s] {segment['text']}")
```

#### `transcribe(audio_input, language=None, prompt=None, response_format='json', temperature=0.0)`

Full transcription method with all options.

**Args:**
- `audio_input`: Path to audio file
- `language` (optional): Language code
- `prompt` (optional): Text to guide transcription style
- `response_format`: 'json', 'text', 'srt', 'verbose_json', or 'vtt'
- `temperature`: Sampling temperature (0.0-1.0)

**Returns:** `dict[str, Any]` - Transcription result

**Example:**
```python
result = transcriber.transcribe(
    'interview.mp3',
    language='en',
    prompt='Technical discussion about AI and machine learning'
)
print(result['text'])
```

## Usage Examples

### Example 1: Simple Transcription

```python
from transcribe import Transcriber

transcriber = Transcriber()
text = transcriber.transcribe_to_text('recording.mp3')
print(text)
```

### Example 2: Transcription with Timestamps

```python
from transcribe import Transcriber

transcriber = Transcriber()
segments = transcriber.transcribe_with_timestamps('lecture.mp3')

for i, segment in enumerate(segments, 1):
    print(f"[{i}] {segment['start']:.2f}s - {segment['end']:.2f}s")
    print(f"    {segment['text']}\n")
```

### Example 3: Transcription with Context Prompt

```python
from transcribe import Transcriber

transcriber = Transcriber()

# Provide context to improve accuracy for technical terms
prompt = "Discussion about Python programming, machine learning, and neural networks"

result = transcriber.transcribe(
    'tech_talk.mp3',
    language='en',
    prompt=prompt
)

print(result['text'])
```

### Example 4: Save Transcription to File

```python
from transcribe import Transcriber
from pathlib import Path

transcriber = Transcriber()

audio_file = 'meeting.mp3'
text = transcriber.transcribe_to_text(audio_file)

# Save to text file
output_file = Path(audio_file).with_suffix('.txt')
output_file.write_text(text, encoding='utf-8')
print(f"Saved to {output_file}")
```

## Supported Audio Formats

- MP3 (.mp3)
- MP4 (.mp4, .m4a)
- MPEG (.mpeg, .mpga)
- WAV (.wav)
- WebM (.webm)
- FLAC (.flac)

**Max file size:** 25 MB (OpenAI API limit)

## Configuration

### Environment Variables

The transcriber uses environment variables from a `.env` file:

```bash
# .env
OPENAI_KEY=your-api-key-here
```

You can also pass the API key directly:

```python
transcriber = Transcriber(api_key='your-api-key-here')
```

## Cost

OpenAI Whisper API pricing: **~$0.006 per minute** of audio

Check your usage at: [https://platform.openai.com/usage](https://platform.openai.com/usage)

## Troubleshooting

### ValueError: OpenAI API key not provided

**Solution:** Make sure you have:
1. Created a `.env` file in the project root
2. Added `OPENAI_KEY=your-actual-api-key` to the file
3. Verified the API key is correct

### FileNotFoundError: Audio file not found

**Solution:** Check that:
1. The file path is correct
2. The file exists
3. You have read permissions

### ValueError: Unsupported audio format

**Solution:** Convert your audio to a supported format (mp3, wav, m4a, etc.)

### ValueError: File size exceeds maximum

**Solution:**
- Compress the audio file
- Split into smaller chunks
- Use a lower bitrate

### ImportError: openai package not installed

**Solution:**
```bash
pip install openai python-dotenv
```

## Project Structure

```
notegenerator/
├── transcribe.py           # Main Transcriber class
├── example_transcribe.py   # Usage examples
├── .env.example           # Example environment file
├── .env                   # Your API key (git-ignored)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Additional Implementations

This project also includes optional local Whisper implementations:

- `whisper_transcriber.py` - Local CPU/GPU transcription (free, offline)
- `whisper_api_transcriber.py` - Full-featured API client with SRT/VTT support

These are provided for reference but are not the primary implementation.

## License

This project uses OpenAI's Whisper API. Refer to OpenAI's terms of service for API usage.
