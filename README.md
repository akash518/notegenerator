# Note Generator - Whisper AI Transcription

A Python library for transcribing audio recordings into text notes using OpenAI's Whisper AI API.

## Features

- **Two-step AI pipeline** - Whisper for transcription + GPT for intelligent formatting
- **Interactive frontend** (main.py) - Easy-to-use menu interface
- **YouTube support** - Download and transcribe YouTube videos directly
- **Note templates** - 5 different formats (study guides, meeting minutes, instructions, etc.)
- **Smart formatting** - GPT structures raw transcripts into organized notes
- **Simple setup** with `.env` file for API key management
- **Multiple audio formats** supported (mp3, wav, m4a, flac, ogg, mp4, webm)
- **Fast cloud processing** - no local GPU needed
- **Cost transparency** - See estimated costs before processing
- **Clean separation** - Transcription and formatting as separate steps

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `yt-dlp` - YouTube video/audio downloader

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

## How It Works

Note Generator uses a **two-step AI pipeline** for superior results:

### Step 1: Transcription (Whisper API)
- Converts audio to raw text
- Handles any language
- Processes ~$0.006/minute

### Step 2: Formatting (GPT API)
- Structures the raw transcript
- Applies your chosen template (study guide, meeting minutes, etc.)
- Organizes information intelligently
- Processes ~$0.01-0.05 per transcription (depending on length)

**Why two steps?**
- ✅ **Whisper** excels at transcription but cannot structure content
- ✅ **GPT** excels at formatting and organizing text
- ✅ Better results than single-step approaches
- ✅ Flexibility to transcribe once, format multiple ways

**Total Cost:** Typically $0.02-0.10 per transcription depending on audio length and template used.

## Quick Start

### 🚀 Interactive Frontend (Recommended)

The easiest way to use Note Generator:

```bash
python main.py
```

**This interactive menu lets you:**
1. ✓ Choose between **audio file** or **YouTube link**
2. ✓ Select your preferred **note template** (study guide, meeting minutes, etc.)
3. ✓ Specify **output filename**
4. ✓ Get **formatted notes** automatically!

**Example Session:**
```
📝 WELCOME TO NOTE GENERATOR
==========================================
MAIN MENU
1. Transcribe from Audio File
2. Transcribe from YouTube Link  ← New!
3. View Template Information
4. Exit

Enter your choice (1-4): 2

Enter the YouTube URL: https://youtube.com/watch?v=example

SELECT NOTE TEMPLATE
1. Study Guide - Comprehensive notes...
2. Meeting Minutes - Professional documentation...
...

✅ SUCCESS! Notes saved to: output/video_title_study_guide_notes.txt
```

### Quick Mode (Command Line)

```bash
# Transcribe a file with template selection
python main.py your_recording.mp3
```

### Programmatic Usage

```python
from src.transcribe import Transcriber
from src.note_templates import load_template
from src.generate import NoteGenerator

# Initialize components (automatically load API key from .env)
transcriber = Transcriber()
note_generator = NoteGenerator()

# Step 1: Transcribe audio to raw text
raw_text = transcriber.transcribe_to_text('recording.mp3')

# Step 2: Format into structured notes using a template
template = load_template('study_guide')
formatted_notes = note_generator.generate_notes(raw_text, template)

# Save the formatted notes
with open('output/notes.txt', 'w') as f:
    f.write(formatted_notes)
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
from src.generate import NoteGenerator

# Initialize components
transcriber = Transcriber()
note_generator = NoteGenerator()

# Step 1: Transcribe audio to raw text with Whisper
raw_text = transcriber.transcribe_to_text('lecture.mp3', language='en')

# Step 2: Load a template and format with GPT
# Options: study_guide, meeting_minutes, instructions, summary, verbatim_transcript
template = load_template('study_guide')
formatted_notes = note_generator.generate_notes(raw_text, template)

# Save the formatted notes
with open('study_notes.txt', 'w') as f:
    f.write(formatted_notes)
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
template = load_template('study_guide')
raw_text = transcriber.transcribe_to_text('biology_lecture.mp3')
notes = note_generator.generate_notes(raw_text, template)
```

**Meeting Minutes** - For professional meetings:
```python
template = load_template('meeting_minutes')
raw_text = transcriber.transcribe_to_text('team_meeting.mp3')
notes = note_generator.generate_notes(raw_text, template)
```

**Quick Summary** - For fast overviews:
```python
template = load_template('summary')
raw_text = transcriber.transcribe_to_text('presentation.mp3')
notes = note_generator.generate_notes(raw_text, template)
```

See the [Templates README](templates/README.md) for detailed information on each template and how to customize them.

## YouTube Transcription

Transcribe YouTube videos directly without manually downloading them!

### Using the Frontend

```bash
python main.py
# Select option 2: Transcribe from YouTube Link
# Enter the YouTube URL
# Choose your note template
# Done!
```

### Programmatic Usage

```python
from src.transcribe import Transcriber
from src.youtube_downloader import YouTubeDownloader
from src.note_templates import load_template
from src.generate import NoteGenerator

# Initialize components
transcriber = Transcriber()
downloader = YouTubeDownloader()
note_generator = NoteGenerator()

# Download audio from YouTube
audio_file = downloader.download_audio('https://youtube.com/watch?v=...')

# Step 1: Transcribe audio to raw text
raw_text = transcriber.transcribe_to_text(audio_file)

# Step 2: Format with template
template = load_template('study_guide')
formatted_notes = note_generator.generate_notes(raw_text, template)

# Save the formatted notes
with open('output/youtube_notes.txt', 'w') as f:
    f.write(formatted_notes)

# Optionally delete the downloaded audio
audio_file.unlink()
```

### Supported YouTube URLs

- `https://youtube.com/watch?v=...`
- `https://www.youtube.com/watch?v=...`
- `https://youtu.be/...`
- `https://m.youtube.com/watch?v=...`

### YouTube Features

- **Automatic audio extraction** - Downloads best quality audio
- **MP3 conversion** - Automatically converts to MP3 format
- **Progress tracking** - See download and transcription progress
- **Cleanup option** - Optionally delete downloaded files after transcription
- **Video information** - Shows video title and duration before processing

## API Reference

### Transcriber Class

Handles audio transcription using OpenAI's Whisper API.

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

**Returns:** `str` - Raw transcribed text

**Example:**
```python
raw_text = transcriber.transcribe_to_text('meeting.mp3', language='en')
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

### NoteGenerator Class

Formats raw transcriptions into structured notes using OpenAI's GPT API.

#### `__init__(api_key=None, model='gpt-3.5-turbo')`

Initialize the note generator.

- `api_key` (optional): OpenAI API key. If None, loads from `OPENAI_KEY` in `.env` file
- `model`: GPT model to use (default: 'gpt-3.5-turbo', can use 'gpt-4' for higher quality)

#### `generate_notes(transcription, template, custom_instructions="")`

Generate formatted notes from raw transcription using a template.

**Args:**
- `transcription`: Raw text from Whisper transcription
- `template`: Template string with formatting instructions (use `load_template()` to load)
- `custom_instructions` (optional): Additional instructions to append to the template

**Returns:** `str` - Formatted notes

**Example:**
```python
from src.note_templates import load_template

template = load_template('study_guide')
formatted_notes = note_generator.generate_notes(raw_text, template)
```

#### `estimate_cost(transcription, template)`

Estimate the cost of generating notes before making the API call.

**Args:**
- `transcription`: Raw text from Whisper transcription
- `template`: Template string

**Returns:** `dict` with keys:
- `input_tokens`: Estimated input token count
- `output_tokens`: Estimated output token count
- `estimated_cost_usd`: Estimated cost in USD
- `model`: Model being used

**Example:**
```python
cost_info = note_generator.estimate_cost(raw_text, template)
print(f"Estimated cost: ${cost_info['estimated_cost_usd']:.4f}")
```

#### `generate_notes_streaming(transcription, template, custom_instructions="")`

Generate notes with streaming output for real-time display.

**Args:**
- `transcription`: Raw text from Whisper transcription
- `template`: Template string with formatting instructions
- `custom_instructions` (optional): Additional instructions

**Yields:** `str` - Chunks of formatted notes as they're generated

**Example:**
```python
for chunk in note_generator.generate_notes_streaming(raw_text, template):
    print(chunk, end='', flush=True)
```

## Usage Examples

### Example 1: Simple Transcription (Raw Text Only)

```python
from src.transcribe import Transcriber

transcriber = Transcriber()
raw_text = transcriber.transcribe_to_text('recording.mp3')
print(raw_text)  # Plain transcription without formatting
```

### Example 2: Formatted Notes with Template

```python
from src.transcribe import Transcriber
from src.generate import NoteGenerator
from src.note_templates import load_template

# Initialize components
transcriber = Transcriber()
note_generator = NoteGenerator()

# Step 1: Transcribe
raw_text = transcriber.transcribe_to_text('lecture.mp3', language='en')

# Step 2: Format with template
template = load_template('study_guide')
formatted_notes = note_generator.generate_notes(raw_text, template)

# Save formatted notes
with open('formatted_notes.txt', 'w') as f:
    f.write(formatted_notes)
```

### Example 3: Transcription with Timestamps

```python
from src.transcribe import Transcriber

transcriber = Transcriber()
segments = transcriber.transcribe_with_timestamps('lecture.mp3')

for i, segment in enumerate(segments, 1):
    print(f"[{i}] {segment['start']:.2f}s - {segment['end']:.2f}s")
    print(f"    {segment['text']}\n")
```

### Example 4: Cost Estimation Before Processing

```python
from src.transcribe import Transcriber
from src.generate import NoteGenerator
from src.note_templates import load_template

transcriber = Transcriber()
note_generator = NoteGenerator()

# Transcribe first
raw_text = transcriber.transcribe_to_text('meeting.mp3')

# Estimate cost before formatting
template = load_template('meeting_minutes')
cost_info = note_generator.estimate_cost(raw_text, template)

print(f"Estimated cost: ${cost_info['estimated_cost_usd']:.4f}")
print(f"Input tokens: {cost_info['input_tokens']}")
print(f"Output tokens: {cost_info['output_tokens']}")

# Proceed with formatting if acceptable
if cost_info['estimated_cost_usd'] < 0.10:  # Less than 10 cents
    formatted_notes = note_generator.generate_notes(raw_text, template)
    print(formatted_notes)
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
├── src/
│   ├── main.py                # Interactive frontend (START HERE!)
│   ├── transcribe.py          # Transcriber class (Whisper API)
│   ├── generate.py            # NoteGenerator class (GPT API)
│   ├── note_templates.py      # Template management
│   └── youtube_downloader.py  # YouTube audio downloader
├── templates/                  # Note formatting templates
│   ├── study_guide.txt
│   ├── meeting_minutes.txt
│   ├── instructions.txt
│   ├── summary.txt
│   ├── verbatim_transcript.txt
│   └── README.md
├── example_transcribe.py      # Basic usage examples
├── example_with_templates.py  # Template examples
├── .env.example               # Example environment file
├── .env                       # Your API key (git-ignored)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Additional Implementations

This project also includes optional local Whisper implementations:

- `whisper_transcriber.py` - Local CPU/GPU transcription (free, offline)
- `whisper_api_transcriber.py` - Full-featured API client with SRT/VTT support

These are provided for reference but are not the primary implementation.

## License

This project uses OpenAI's Whisper API. Refer to OpenAI's terms of service for API usage.
