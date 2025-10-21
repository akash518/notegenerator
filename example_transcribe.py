"""
Example usage of the Transcriber class

This script demonstrates how to use the Transcriber for transcribing
audio recordings to text notes.
"""

from src.transcribe import Transcriber
import sys
from pathlib import Path


def main():
    """Main example function demonstrating Transcriber usage."""

    # Initialize the transcriber (loads API key from .env file)
    try:
        transcriber = Transcriber()
        print("Transcriber initialized successfully!\n")
    except ValueError as e:
        print(f"Error: {e}")
        print("\nMake sure you have created a .env file with your OPENAI_KEY:")
        print("  OPENAI_KEY=your-api-key-here")
        return

    # Example audio file path (replace with your actual file)
    audio_file = "your_recording.mp3"

    # Example 1: Simple text transcription
    print("="*60)
    print("Example 1: Simple Text Transcription")
    print("="*60)

    try:
        text = transcriber.transcribe_to_text(audio_file)
        print(f"\nTranscribed Text:\n{text}\n")

    except FileNotFoundError:
        print(f"\nAudio file '{audio_file}' not found.")
        print("Please update the 'audio_file' variable with a valid path.\n")

    # Example 2: Transcription with timestamps
    print("="*60)
    print("Example 2: Transcription with Timestamps")
    print("="*60)

    try:
        segments = transcriber.transcribe_with_timestamps(audio_file)

        print("\nSegmented Transcription:\n")
        for i, segment in enumerate(segments, 1):
            start_time = f"{segment['start']:.2f}s"
            end_time = f"{segment['end']:.2f}s"
            print(f"[{i}] ({start_time} - {end_time})")
            print(f"    {segment['text']}\n")

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.\n")
    except Exception as e:
        print(f"Note: {e}\n")

    # Example 3: Transcribe with specific language
    print("="*60)
    print("Example 3: Transcribe with Specific Language")
    print("="*60)

    try:
        # Specify language code (e.g., 'en' for English, 'es' for Spanish)
        text_en = transcriber.transcribe_to_text(audio_file, language='en')
        print(f"\nEnglish Transcription:\n{text_en}\n")

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.\n")

    # Example 4: Using prompt for better accuracy
    print("="*60)
    print("Example 4: Using Prompt for Context")
    print("="*60)

    try:
        # Providing a prompt can help with proper nouns, context, etc.
        prompt = "This is a technical discussion about Python programming and AI."
        result = transcriber.transcribe(
            audio_file,
            prompt=prompt
        )
        print(f"\nTranscription with context:\n{result['text']}\n")

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.\n")

    print("="*60)
    print("Examples completed!")
    print("="*60)


def quick_transcribe(audio_path: str) -> str | None:
    """
    Quick transcription helper function.

    Args:
        audio_path: Path to the audio file

    Returns:
        Transcribed text or None if error
    """
    try:
        transcriber = Transcriber()
        text = transcriber.transcribe_to_text(audio_path)
        return text
    except ValueError as e:
        print(f"Error: {e}")
        print("\nMake sure you have created a .env file with your OPENAI_KEY:")
        print("  OPENAI_KEY=your-api-key-here")
        return None
    except FileNotFoundError:
        print(f"Error: Audio file '{audio_path}' not found.")
        return None


if __name__ == "__main__":
    # Check if audio file path is provided as command-line argument
    if len(sys.argv) > 1:
        audio_file_arg = sys.argv[1]
        print(f"Transcribing: {audio_file_arg}\n")

        # Quick transcription
        text = quick_transcribe(audio_file_arg)

        if text:
            print(f"Transcription:\n{text}\n")

            # Optionally save to file
            audio_path = Path(audio_file_arg)
            output_file = audio_path.with_suffix('.txt')
            output_file.write_text(text, encoding='utf-8')
            print(f"Saved to: {output_file}")
    else:
        # Run all examples
        main()
