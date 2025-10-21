"""
Example: Using Note Templates with Transcriber

This script demonstrates how to use different note templates to format
your transcriptions according to your specific needs.
"""

from src.transcribe import Transcriber
from src.note_templates import NoteTemplates, load_template
from pathlib import Path
import sys


def demonstrate_all_templates(audio_file: str):
    """
    Demonstrate all available templates with a single audio file.

    Args:
        audio_file: Path to the audio file to transcribe
    """
    print("\n" + "="*70)
    print("NOTE TEMPLATES DEMONSTRATION")
    print("="*70 + "\n")

    # Initialize transcriber and templates
    try:
        transcriber = Transcriber()
        templates = NoteTemplates()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nMake sure you have created a .env file with your OPENAI_KEY")
        return

    # Show available templates
    templates.print_available_templates()

    # Get all template types
    template_info = templates.list_templates()

    print(f"\nTranscribing '{audio_file}' with all templates...\n")

    # Process with each template
    for template_id, info in template_info.items():
        print(f"\n{'='*70}")
        print(f"Processing: {info['name']}")
        print(f"{'='*70}\n")

        try:
            # Load the template
            prompt = templates.get_template(template_id)  # type: ignore

            # Transcribe with this template
            result = transcriber.transcribe(
                audio_file,
                prompt=prompt,
                language='en'  # Adjust as needed
            )

            # Save to file
            output_file = f"output/{template_id}_notes.txt"
            saved_path = transcriber.save_to_file(
                result['text'],
                output_file
            )

            print(f"✓ Successfully created {info['name']}")
            print(f"  Saved to: {saved_path}")
            print(f"  Preview (first 200 chars):")
            print(f"  {result['text'][:200]}...")

        except FileNotFoundError:
            print(f"✗ Audio file not found: {audio_file}")
            break
        except Exception as e:
            print(f"✗ Error processing {template_id}: {e}")

    print(f"\n{'='*70}")
    print("DEMONSTRATION COMPLETE")
    print(f"{'='*70}\n")
    print(f"Check the 'output/' directory for all generated notes.")


def example_study_guide(audio_file: str):
    """
    Example: Create comprehensive study notes from a lecture.
    """
    print("\n" + "="*70)
    print("EXAMPLE: Study Guide")
    print("="*70 + "\n")

    transcriber = Transcriber()

    # Load the study guide template
    study_prompt = load_template('study_guide')

    # Transcribe with the study guide format
    result = transcriber.transcribe(
        audio_file,
        prompt=study_prompt,
        language='en'
    )

    # Save the study notes
    output_file = transcriber.save_to_file(
        result['text'],
        'output/study_notes.txt'
    )

    print(f"✓ Study guide created: {output_file}")
    print(f"\nYour comprehensive study notes include:")
    print("  - Key concepts and definitions")
    print("  - Main topics organized logically")
    print("  - Examples and applications")
    print("  - Important details and takeaways")


def example_meeting_minutes(audio_file: str):
    """
    Example: Create professional meeting minutes.
    """
    print("\n" + "="*70)
    print("EXAMPLE: Meeting Minutes")
    print("="*70 + "\n")

    transcriber = Transcriber()

    # Load the meeting minutes template
    meeting_prompt = load_template('meeting_minutes')

    # Transcribe with meeting minutes format
    result = transcriber.transcribe(
        audio_file,
        prompt=meeting_prompt,
        language='en'
    )

    # Save the meeting minutes
    output_file = transcriber.save_to_file(
        result['text'],
        'output/meeting_minutes.txt'
    )

    print(f"✓ Meeting minutes created: {output_file}")
    print(f"\nYour meeting minutes include:")
    print("  - Discussion summary")
    print("  - Key decisions made")
    print("  - Action items with owners")
    print("  - Next steps and deadlines")


def example_instructions(audio_file: str):
    """
    Example: Create step-by-step instructions from a tutorial.
    """
    print("\n" + "="*70)
    print("EXAMPLE: Step-by-Step Instructions")
    print("="*70 + "\n")

    transcriber = Transcriber()

    # Load the instructions template
    instructions_prompt = load_template('instructions')

    # Transcribe with instructions format
    result = transcriber.transcribe(
        audio_file,
        prompt=instructions_prompt,
        language='en'
    )

    # Save the instructions
    output_file = transcriber.save_to_file(
        result['text'],
        'output/instructions.txt'
    )

    print(f"✓ Instructions created: {output_file}")
    print(f"\nYour instructions include:")
    print("  - Prerequisites and materials needed")
    print("  - Numbered step-by-step process")
    print("  - Tips and best practices")
    print("  - Troubleshooting common issues")


def example_summary(audio_file: str):
    """
    Example: Create a brief summary for quick review.
    """
    print("\n" + "="*70)
    print("EXAMPLE: Brief Summary")
    print("="*70 + "\n")

    transcriber = Transcriber()

    # Load the summary template
    summary_prompt = load_template('summary')

    # Transcribe with summary format
    result = transcriber.transcribe(
        audio_file,
        prompt=summary_prompt,
        language='en'
    )

    # Save the summary
    output_file = transcriber.save_to_file(
        result['text'],
        'output/summary.txt'
    )

    print(f"✓ Summary created: {output_file}")
    print(f"\nYour summary includes:")
    print("  - Executive overview")
    print("  - Key points only")
    print("  - Essential facts and decisions")
    print("  - Bottom line takeaway")


def example_verbatim_transcript(audio_file: str):
    """
    Example: Create word-for-word transcript with timestamps.
    """
    print("\n" + "="*70)
    print("EXAMPLE: Verbatim Transcript")
    print("="*70 + "\n")

    transcriber = Transcriber()

    # Load the verbatim transcript template
    verbatim_prompt = load_template('verbatim_transcript')

    # Transcribe with verbatim format
    result = transcriber.transcribe(
        audio_file,
        prompt=verbatim_prompt,
        language='en'
    )

    # Save the transcript
    output_file = transcriber.save_to_file(
        result['text'],
        'output/verbatim_transcript.txt'
    )

    print(f"✓ Verbatim transcript created: {output_file}")
    print(f"\nYour transcript includes:")
    print("  - Word-for-word transcription")
    print("  - Timestamps for each segment")
    print("  - Speaker identification")
    print("  - Non-verbal cues and actions")


def interactive_template_selection(audio_file: str):
    """
    Let the user interactively choose which template to use.
    """
    print("\n" + "="*70)
    print("INTERACTIVE TEMPLATE SELECTION")
    print("="*70 + "\n")

    try:
        transcriber = Transcriber()
        templates = NoteTemplates()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nMake sure you have created a .env file with your OPENAI_KEY")
        return

    # Show options
    templates.print_available_templates()

    # Get user choice
    print("Which template would you like to use?")
    template_id = NoteTemplates.get_template_id_from_user()

    print(f"\nYou selected: {templates.TEMPLATE_INFO[template_id]['name']}")
    print(f"Transcribing '{audio_file}'...\n")

    try:
        # Load selected template
        prompt = templates.get_template(template_id)

        # Transcribe with selected template
        result = transcriber.transcribe(
            audio_file,
            prompt=prompt,
            language='en'
        )

        # Save with template name
        output_file = f"output/{template_id}_notes.txt"
        saved_path = transcriber.save_to_file(
            result['text'],
            output_file
        )

        print(f"\n✓ Success!")
        print(f"  Notes saved to: {saved_path}")
        print(f"\nFirst 300 characters of your notes:")
        print("-" * 70)
        print(result['text'][:300])
        print("...")
        print("-" * 70)

    except FileNotFoundError:
        print(f"✗ Audio file not found: {audio_file}")
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Main function with usage examples."""

    print("\n" + "="*70)
    print("NOTE TEMPLATES - USAGE EXAMPLES")
    print("="*70)

    # Example audio file
    audio_file = "your_recording.mp3"

    if not Path(audio_file).exists():
        print(f"\nNote: Audio file '{audio_file}' not found.")
        print("These examples will show you how to use templates.")
        print("Replace 'your_recording.mp3' with your actual audio file.\n")

    print("\nChoose an example to run:")
    print("1. Study Guide - Comprehensive educational notes")
    print("2. Meeting Minutes - Professional meeting notes")
    print("3. Instructions - Step-by-step tutorial")
    print("4. Summary - Brief overview")
    print("5. Verbatim Transcript - Word-for-word with timestamps")
    print("6. Interactive Selection - Choose your template")
    print("7. Demonstrate All Templates - Create notes with all formats")
    print("\n0. Exit")

    choice = input("\nEnter choice (0-7): ").strip()

    examples = {
        '1': lambda: example_study_guide(audio_file),
        '2': lambda: example_meeting_minutes(audio_file),
        '3': lambda: example_instructions(audio_file),
        '4': lambda: example_summary(audio_file),
        '5': lambda: example_verbatim_transcript(audio_file),
        '6': lambda: interactive_template_selection(audio_file),
        '7': lambda: demonstrate_all_templates(audio_file),
    }

    if choice in examples:
        try:
            examples[choice]()
        except ValueError as e:
            print(f"\nError: {e}")
            print("Make sure you have created a .env file with your OPENAI_KEY")
    elif choice == '0':
        print("Exiting...")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If audio file provided as argument, use interactive selection
        audio_file = sys.argv[1]
        interactive_template_selection(audio_file)
    else:
        # Otherwise show menu
        main()
