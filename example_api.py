"""
Example usage of the WhisperAPITranscriber class

This script demonstrates various ways to use the WhisperAPITranscriber
for transcribing audio recordings using OpenAI's cloud API.
"""

from whisper_api_transcriber import WhisperAPITranscriber
import sys
import os


def main():
    """Main example function demonstrating WhisperAPITranscriber usage."""

    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("ERROR: OpenAI API key not found!")
        print("\nPlease set your OPENAI_API_KEY environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("\nOr get an API key at: https://platform.openai.com/api-keys")
        return

    # Initialize the transcriber
    print("Initializing Whisper API Transcriber...")
    transcriber = WhisperAPITranscriber()

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
    print("Example 2: Full Transcription")
    print("="*60)

    try:
        result = transcriber.transcribe(audio_file, response_format='json')
        print(f"\nFull Text:\n{result['text']}")

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    # Example 3: Transcription with timestamps (verbose JSON)
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
    except Exception as e:
        print(f"Note: Timestamps may not be available: {e}")

    # Example 4: Save transcription to file
    print("\n" + "="*60)
    print("Example 4: Save Transcription to File")
    print("="*60)

    try:
        output_file = "transcription_api_output.txt"

        # Save as plain text
        transcriber.save_transcription(
            audio_file,
            output_file,
            format='text'
        )

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    # Example 5: Generate SRT subtitle file
    print("\n" + "="*60)
    print("Example 5: Generate SRT Subtitle File")
    print("="*60)

    try:
        srt_file = "subtitles.srt"
        transcriber.save_transcription(
            audio_file,
            srt_file,
            format='srt'
        )

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    # Example 6: Generate WebVTT subtitle file
    print("\n" + "="*60)
    print("Example 6: Generate WebVTT Subtitle File")
    print("="*60)

    try:
        vtt_file = "subtitles.vtt"
        transcriber.save_transcription(
            audio_file,
            vtt_file,
            format='vtt'
        )

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    # Example 7: Transcribe with specific language
    print("\n" + "="*60)
    print("Example 7: Transcribe with Specific Language")
    print("="*60)

    try:
        # Specify language code (e.g., 'en' for English, 'es' for Spanish)
        text_en = transcriber.transcribe_to_text(audio_file, language='en')
        print(f"\nEnglish Transcription:\n{text_en}")

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    # Example 8: Translate audio to English
    print("\n" + "="*60)
    print("Example 8: Translate Audio to English")
    print("="*60)

    try:
        # This will translate non-English audio to English
        result = transcriber.translate(audio_file)
        print(f"\nTranslated Text:\n{result['text']}")

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    # Example 9: Using prompt for better accuracy
    print("\n" + "="*60)
    print("Example 9: Using Prompt for Context")
    print("="*60)

    try:
        # Providing a prompt can help with proper nouns, context, etc.
        prompt = "This is a technical discussion about Python programming and AI."
        text = transcriber.transcribe_to_text(
            audio_file,
            prompt=prompt
        )
        print(f"\nTranscription with context:\n{text}")

    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)
    print("\nNote: Using the API incurs costs (~$0.006 per minute of audio)")
    print("Check your usage at: https://platform.openai.com/usage")


def quick_transcribe(audio_path):
    """Quick transcription helper function."""
    try:
        transcriber = WhisperAPITranscriber()
        text = transcriber.transcribe_to_text(audio_path)
        return text
    except ValueError as e:
        print(f"Error: {e}")
        print("\nMake sure to set your OPENAI_API_KEY environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return None


if __name__ == "__main__":
    # Check if audio file path is provided as command-line argument
    if len(sys.argv) > 1:
        audio_file_arg = sys.argv[1]
        print(f"Using audio file from command line: {audio_file_arg}")

        # Quick transcription
        text = quick_transcribe(audio_file_arg)

        if text:
            print(f"\nTranscription:\n{text}")

            # Optionally save to file
            output_file = f"{os.path.splitext(audio_file_arg)[0]}_transcription.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"\nSaved to: {output_file}")
    else:
        # Run all examples
        main()
