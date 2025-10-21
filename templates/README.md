# Note Templates

This folder contains prompt templates that format transcriptions for different use cases. Each template provides detailed instructions to the OpenAI API on how to organize and structure the transcribed content.

## Available Templates

### 1. Study Guide (`study_guide.txt`)
**Best for:** Lectures, educational content, learning material, study sessions

Creates comprehensive educational notes with:
- Key concepts and definitions
- Main topics organized logically
- Examples and applications
- Important details and takeaways
- Questions to consider

**Use when:** You're transcribing lectures, courses, or any educational content you need to study from.

---

### 2. Meeting Minutes (`meeting_minutes.txt`)
**Best for:** Business meetings, team syncs, project discussions, planning sessions

Creates professional meeting documentation with:
- Meeting information and attendees
- Discussion summary by topic
- Key decisions and agreements
- Action items with owners and deadlines
- Next steps and follow-ups

**Use when:** You need formal documentation of meetings, decisions, and action items.

---

### 3. Step-by-Step Instructions (`instructions.txt`)
**Best for:** Tutorials, how-to guides, training sessions, demonstrations

Creates clear tutorial-style documentation with:
- Prerequisites and materials needed
- Numbered step-by-step process
- Tips and best practices
- Troubleshooting common issues
- Verification steps

**Use when:** You're transcribing tutorials, training videos, or any instructional content.

---

### 4. Brief Summary (`summary.txt`)
**Best for:** Quick reviews, executive summaries, condensed overviews

Creates concise notes focusing on:
- Executive overview
- Key points only (no fluff)
- Essential facts and decisions
- Bottom line takeaway
- Quick reference bullets

**Use when:** You need a quick overview or don't have time to read detailed notes.

---

### 5. Verbatim Transcript (`verbatim_transcript.txt`)
**Best for:** Legal records, interviews, detailed analysis, accurate documentation

Creates word-for-word transcription with:
- Timestamps for each segment
- Speaker identification
- Exact wording including filler words
- Non-verbal cues (laughs, pauses, etc.)
- Background sounds notation

**Use when:** You need an accurate, complete record of everything said.

---

## How to Use Templates

### Method 1: Using the NoteTemplates Class (Recommended)

```python
from src.transcribe import Transcriber
from src.note_templates import NoteTemplates

# Initialize
transcriber = Transcriber()
templates = NoteTemplates()

# Load a template
study_prompt = templates.get_template('study_guide')

# Transcribe with the template
result = transcriber.transcribe(
    'lecture.mp3',
    prompt=study_prompt,
    language='en'
)

# Save the formatted notes
transcriber.save_to_file(result['text'], 'study_notes.txt')
```

### Method 2: Quick Helper Function

```python
from src.transcribe import Transcriber
from src.note_templates import load_template

transcriber = Transcriber()

# One-liner to load template
prompt = load_template('meeting_minutes')

# Transcribe
result = transcriber.transcribe('meeting.mp3', prompt=prompt)
```

### Method 3: Interactive Selection

```python
from src.note_templates import NoteTemplates

templates = NoteTemplates()

# Show all available templates
templates.print_available_templates()

# Let user choose
template_id = NoteTemplates.get_template_id_from_user()
prompt = templates.get_template(template_id)
```

## Template IDs

Use these IDs when calling `get_template()` or `load_template()`:

- `study_guide` - Comprehensive study notes
- `meeting_minutes` - Professional meeting documentation
- `instructions` - Step-by-step tutorial format
- `summary` - Brief overview
- `verbatim_transcript` - Word-for-word with timestamps

## Customizing Templates

You can edit these template files to customize the output format:

1. Open the template file (e.g., `study_guide.txt`)
2. Modify the instructions or structure
3. Save the file
4. Use it as normal - changes take effect immediately

### Tips for Customization:
- Be specific about what you want
- Provide clear formatting instructions
- Include examples of desired output format
- Specify what to include and exclude
- Define the level of detail needed

## Creating New Templates

To add your own template:

1. Create a new `.txt` file in the `templates/` folder
2. Write detailed instructions for how to format the output
3. Use the existing templates as examples
4. Load it using the template filename (without .txt extension)

Example:
```python
templates = NoteTemplates()
my_template = templates.get_template('my_custom_template')
```

### Quick Example - Study Notes

```python
from src.transcribe import Transcriber
from src.note_templates import load_template

# Setup
transcriber = Transcriber()
prompt = load_template('study_guide')

# Create study notes
transcriber.transcribe_and_save(
    'biology_lecture.mp3',
    'biology_notes.txt',
    prompt=prompt
)
```

### Quick Example - Meeting Minutes

```python
from src.transcribe import Transcriber
from src.note_templates import load_template

transcriber = Transcriber()
prompt = load_template('meeting_minutes')

transcriber.transcribe_and_save(
    'team_meeting.mp3',
    'meeting_notes.txt',
    prompt=prompt
)
```

## Best Practices

1. **Choose the right template** - Each template is optimized for specific content types
2. **Specify language** - Always set the `language` parameter if you know it
3. **Review output** - Templates guide the API but may need manual refinement
4. **Combine with save** - Use `transcribe_and_save()` for convenience
5. **Test with samples** - Try different templates to see which works best for your content

## Frontend Implementation

For a user-friendly frontend, you could:

1. **Display template options** - Show all available templates with descriptions
2. **Let user select** - Radio buttons or dropdown menu
3. **Load corresponding template** - Based on user selection
4. **Transcribe with template** - Pass the template as the prompt
5. **Save with appropriate name** - Use template type in filename

Example flow:
```
User uploads audio → Selects "Study Guide" →
App loads study_guide.txt → Transcribes with template →
Saves as "lecture_study_notes.txt"
```

## Technical Details

- **Format**: Plain text files
- **Encoding**: UTF-8
- **Size**: Templates are typically 1-3 KB
- **Processing**: Templates are passed as the `prompt` parameter to the Whisper API
- **Effect**: The prompt guides how the transcription is structured and formatted

## Troubleshooting

**Template not found error:**
- Ensure the template file exists in the `templates/` folder
- Check that the template ID matches the filename (without .txt)
- Verify the templates directory path is correct

**Output doesn't match template:**
- Audio quality affects how well the API can follow instructions
- Some templates work better with certain content types
- Try a different template or customize the existing one

**Template not formatting as expected:**
- Make instructions more specific in the template file
- Add examples of desired format in the template
- Break complex instructions into numbered steps
