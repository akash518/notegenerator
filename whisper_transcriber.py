"""
Whisper AI Transcription Class for Note Generation

This module provides a WhisperTranscriber class that handles audio transcription
using OpenAI's Whisper model.
"""

import os
from typing import Any
from pathlib import Path


class WhisperTranscriber:
    """
    A class for transcribing audio recordings using OpenAI's Whisper AI model.

    This class supports multiple Whisper model sizes and can transcribe audio
    from files or audio data in various formats.

    Attributes:
        model_size (str): The size of the Whisper model to use
        model: The loaded Whisper model instance
        device (str): The device to run the model on ('cuda' or 'cpu')
    """

    SUPPORTED_MODELS = ['tiny', 'base', 'small', 'medium', 'large']
    SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.mp4', '.webm']

    def __init__(self, model_size: str = 'base', device: str | None = None):
        """
        Initialize the Whisper transcriber.

        Args:
            model_size (str): Size of the Whisper model to use. Options are:
                             'tiny', 'base', 'small', 'medium', 'large'
                             Default is 'base' for a good balance of speed and accuracy.
            device (str, optional): Device to run the model on ('cuda' or 'cpu').
                                   If None, automatically detects GPU availability.

        Raises:
            ValueError: If an unsupported model size is specified
            ImportError: If whisper package is not installed
        """
        if model_size not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Model size '{model_size}' not supported. "
                f"Choose from: {', '.join(self.SUPPORTED_MODELS)}"
            )

        self.model_size = model_size
        self.device = device
        self.model = None

        self._load_model()

    def _load_model(self):
        """
        Load the Whisper model.

        Raises:
            ImportError: If the whisper package is not installed
        """
        try:
            import whisper
            import torch
        except ImportError as e:
            raise ImportError(
                "Whisper package not installed. "
                "Install it with: pip install openai-whisper"
            ) from e

        # Determine device if not specified
        if self.device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading Whisper '{self.model_size}' model on {self.device}...")
        self.model = whisper.load_model(self.model_size, device=self.device)
        print("Model loaded successfully!")

    def transcribe(
        self,
        audio_input: str | Path,
        language: str | None = None,
        task: str = "transcribe",
        **kwargs
    ) -> dict[str, Any]:
        """
        Transcribe an audio recording.

        Args:
            audio_input (Union[str, Path]): Path to the audio file to transcribe
            language (str, optional): Language code (e.g., 'en', 'es', 'fr').
                                     If None, language will be auto-detected.
            task (str): Either 'transcribe' or 'translate'. Default is 'transcribe'.
                       'translate' will translate to English.
            **kwargs: Additional arguments to pass to whisper.transcribe()
                     (e.g., temperature, beam_size, etc.)

        Returns:
            Dict[str, Any]: Transcription result containing:
                - 'text': The transcribed text
                - 'segments': Detailed segment information with timestamps
                - 'language': Detected or specified language

        Raises:
            FileNotFoundError: If the audio file doesn't exist
            ValueError: If the audio format is not supported
        """
        # Validate input file
        audio_path = Path(audio_input)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_input}")

        if audio_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported audio format: {audio_path.suffix}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        # Prepare transcription options
        options = {
            "task": task,
            **kwargs
        }

        if language:
            options["language"] = language

        print(f"Transcribing {audio_path.name}...")

        # Perform transcription
        result = self.model.transcribe(str(audio_path), **options)

        print("Transcription complete!")

        return result

    def transcribe_to_text(
        self,
        audio_input: str | Path,
        language: str | None = None,
        **kwargs
    ) -> str:
        """
        Transcribe an audio recording and return only the text.

        This is a convenience method that returns just the transcribed text
        without the additional metadata.

        Args:
            audio_input (Union[str, Path]): Path to the audio file to transcribe
            language (str, optional): Language code (e.g., 'en', 'es', 'fr')
            **kwargs: Additional arguments to pass to whisper.transcribe()

        Returns:
            str: The transcribed text
        """
        result = self.transcribe(audio_input, language=language, **kwargs)
        return result['text'].strip()

    def transcribe_with_timestamps(
        self,
        audio_input: str | Path,
        language: str | None = None,
        **kwargs
    ) -> list:
        """
        Transcribe an audio recording with detailed timestamp information.

        Args:
            audio_input (Union[str, Path]): Path to the audio file to transcribe
            language (str, optional): Language code (e.g., 'en', 'es', 'fr')
            **kwargs: Additional arguments to pass to whisper.transcribe()

        Returns:
            list: List of segments, each containing:
                - 'start': Start time in seconds
                - 'end': End time in seconds
                - 'text': Transcribed text for this segment
        """
        result = self.transcribe(audio_input, language=language, **kwargs)
        return [
            {
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'].strip()
            }
            for segment in result['segments']
        ]

    def save_transcription(
        self,
        audio_input: str | Path,
        output_path: str | Path,
        language: str | None = None,
        include_timestamps: bool = False,
        **kwargs
    ):
        """
        Transcribe audio and save the result to a text file.

        Args:
            audio_input (Union[str, Path]): Path to the audio file to transcribe
            output_path (Union[str, Path]): Path where the transcription will be saved
            language (str, optional): Language code (e.g., 'en', 'es', 'fr')
            include_timestamps (bool): If True, include timestamps in the output
            **kwargs: Additional arguments to pass to whisper.transcribe()
        """
        output_path = Path(output_path)

        if include_timestamps:
            segments = self.transcribe_with_timestamps(
                audio_input, language=language, **kwargs
            )

            # Format with timestamps
            lines = []
            for segment in segments:
                timestamp = f"[{self._format_time(segment['start'])} -> {self._format_time(segment['end'])}]"
                lines.append(f"{timestamp} {segment['text']}")

            content = '\n'.join(lines)
        else:
            content = self.transcribe_to_text(audio_input, language=language, **kwargs)

        # Save to file
        output_path.write_text(content, encoding='utf-8')
        print(f"Transcription saved to: {output_path}")

    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Format seconds into HH:MM:SS format.

        Args:
            seconds (float): Time in seconds

        Returns:
            str: Formatted time string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"


# Example usage
if __name__ == "__main__":
    # Example: Create transcriber and transcribe a file
    transcriber = WhisperTranscriber(model_size='base')

    # Example audio file path (replace with your actual file)
    audio_file = "recording.mp3"

    if os.path.exists(audio_file):
        # Get full transcription with metadata
        result = transcriber.transcribe(audio_file)
        print("\nFull transcription:")
        print(result['text'])

        # Or just get the text
        text = transcriber.transcribe_to_text(audio_file)
        print("\nText only:")
        print(text)

        # Or get timestamps
        segments = transcriber.transcribe_with_timestamps(audio_file)
        print("\nWith timestamps:")
        for segment in segments:
            print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")

        # Save to file
        transcriber.save_transcription(audio_file, "transcription.txt")
    else:
        print(f"Example audio file '{audio_file}' not found.")
        print("Please provide a valid audio file path to test the transcriber.")
