"""
Example usage of the WhisperTranscriber class

This script demonstrates various ways to use the WhisperTranscriber
for transcribing audio recordings.
"""

from whisper_transcriber import WhisperTranscriber
import sys


def main():
    """Main example function demonstrating WhisperTranscriber usage."""

    # Initialize the transcriber with the 'base' model
    # You can also use: 'tiny', 'small', 'medium', or 'large'
    print("Initializing Whisper Transcriber...")
    transcriber = WhisperTranscriber(model_size='base')

    # Example 1: Simple text transcription
    print("\n" + "="*60)
    print("Example 1: Simple Text Transcription")
    print("="*60)

    audio_file = "your_recording.mp3"  # Replace with your audio file

    try:
        text = transcriber.transcribe_to_text(audio_file)
        print(f"\nTranscribed Text:\n{text}")

    except FileNotFoundError:
        print(f"\nAudio file '{audio_file}' not found.")
        print("Please update the 'audio_file' variable with a valid path.")

    # Example 2: Full transcription with metadata
    print("\n" + "="*60)
    print("Example 2: Full Transcription with Metadata")
    print("="*60)

    try:
        result = transcriber.transcribe(audio_file)

        print(f"\nDetected Language: {result['language']}")
        print(f"\nFull Text:\n{result['text']}")
        print(f"\nNumber of Segments: {len(result['segments'])}")

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    # Example 3: Transcription with timestamps
    print("\n" + "="*60)
    print("Example 3: Transcription with Timestamps")
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
        print(f"Audio file '{audio_file}' not found.")

    # Example 4: Save transcription to file
    print("\n" + "="*60)
    print("Example 4: Save Transcription to File")
    print("="*60)

    try:
        output_file = "transcription_output.txt"

        # Save without timestamps
        transcriber.save_transcription(
            audio_file,
            output_file,
            include_timestamps=False
        )

        # Save with timestamps
        output_file_with_timestamps = "transcription_with_timestamps.txt"
        transcriber.save_transcription(
            audio_file,
            output_file_with_timestamps,
            include_timestamps=True
        )

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    # Example 5: Transcribe with specific language
    print("\n" + "="*60)
    print("Example 5: Transcribe with Specific Language")
    print("="*60)

    try:
        # Specify language code (e.g., 'en' for English, 'es' for Spanish)
        text_en = transcriber.transcribe_to_text(audio_file, language='en')
        print(f"\nEnglish Transcription:\n{text_en}")

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    # Example 6: Translate to English
    print("\n" + "="*60)
    print("Example 6: Translate Audio to English")
    print("="*60)

    try:
        # This will translate non-English audio to English
        result = transcriber.transcribe(audio_file, task='translate')
        print(f"\nTranslated Text:\n{result['text']}")

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    # Check if audio file path is provided as command-line argument
    if len(sys.argv) > 1:
        audio_file_arg = sys.argv[1]
        print(f"Using audio file from command line: {audio_file_arg}")

        # Quick transcription
        transcriber = WhisperTranscriber(model_size='base')
        text = transcriber.transcribe_to_text(audio_file_arg)
        print(f"\nTranscription:\n{text}")
    else:
        # Run all examples
        main()
