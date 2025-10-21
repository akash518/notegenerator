"""
Audio Transcription Backend for Note Generation

Transcribes audio recordings using OpenAI's Whisper or GPT-4o transcription models.
"""

import os
from typing import Any
from pathlib import Path
from config import OPENAI_KEY

class Transcriber:
    """
    Transcribes audio recordings using OpenAI's API.

    This class handles the core transcription functionality, sending audio files
    to OpenAI's cloud API and returning the transcribed text.

    Attributes:
        model (str): The OpenAI model to use
        client: OpenAI client instance
    """

    SUPPORTED_FORMATS = [
        '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm', '.flac'
    ]
    MAX_FILE_SIZE_MB = 50  # OpenAI API limit

    def __init__(self, model: str = "gpt-4o-transcribe"):
        """
        Initialize the transcriber.

        Args:
            model (str): Model to use.
            Options:
                - whisper-1
                - gpt-4o-transcribe

        Raises:
            ValueError: If API key is not provided and not in environment
            ImportError: If openai package is not installed
        """
        # Get API key from parameter or environment variable (OPENAI_KEY)
        self.api_key = OPENAI_KEY

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided."
            )

        self.model = model
        self.client = None

        self._initialize_client()

    def _initialize_client(self):
        """
        Initialize the OpenAI client.

        Raises:
            ImportError: If the openai package is not installed
        """
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError(
                "OpenAI package not installed. "
                "Install it with: pip install openai"
            ) from e

        self.client = OpenAI(api_key=self.api_key)

    def transcribe(
        self,
        audio_input: str | Path,
        language: str | None = None,
        prompt: str | None = None,
        response_format: str = "json",
        temperature: float = 0.0,
    ) -> dict[str, Any]:
        """
        Transcribe an audio recording using OpenAI's API.

        Args:
            audio_input (str | Path): Path to the audio file to transcribe
            language (str, optional): Language code in ISO-639-1 format (e.g., 'en', 'es').
                                     If None, language will be auto-detected.
            prompt (str, optional): Optional text to guide the model's style or continue
                                   a previous audio segment. Must match the audio language.
            response_format (str): Format of the response. Options: 'json', 'text',
                                  'srt', 'verbose_json', 'vtt'. Default is 'json'.
            temperature (float): Sampling temperature between 0 and 1. Default is 0.

        Returns:
            dict[str, Any]: Transcription result containing:
                - 'text': The transcribed text
                - Additional fields depending on response_format

        Raises:
            FileNotFoundError: If the audio file doesn't exist
            ValueError: If the audio format is not supported or file is too large
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

        # Check file size
        file_size_mb = audio_path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.MAX_FILE_SIZE_MB:
            raise ValueError(
                f"File size ({file_size_mb:.2f} MB) exceeds the maximum "
                f"allowed size of {self.MAX_FILE_SIZE_MB} MB"
            )

        # Open and send file to API
        with open(audio_path, 'rb') as audio_file:
            # Build request parameters
            params = {
                "model": self.model,
                "file": audio_file,
                "response_format": response_format,
                "temperature": temperature,
            }

            if language:
                params["language"] = language

            if prompt:
                params["prompt"] = prompt

            # Make API call
            response = self.client.audio.transcriptions.create(**params)

        # Format response based on response_format
        if response_format == "json":
            return {"text": response.text}
        elif response_format == "verbose_json":
            return response.model_dump()
        else:
            # For text, srt, vtt formats, response is a string
            return {"text": response}

    def transcribe_to_text(
        self,
        audio_input: str | Path,
        language: str | None = None,
        **kwargs
    ) -> str:
        """
        Transcribe an audio recording and return only the text.

        This is a convenience method for getting just the transcribed text.

        Args:
            audio_input (str | Path): Path to the audio file to transcribe
            language (str, optional): Language code (e.g., 'en', 'es', 'fr')
            **kwargs: Additional arguments to pass to transcribe()

        Returns:
            str: The transcribed text
        """
        result = self.transcribe(
            audio_input,
            language=language,
            response_format="text",
            **kwargs
        )

        # Handle both string and dict responses
        if isinstance(result, dict):
            return result['text'].strip()
        return result.strip()

    def transcribe_with_timestamps(
        self,
        audio_input: str | Path,
        language: str | None = None,
        **kwargs
    ) -> list[dict[str, Any]]:
        """
        Transcribe an audio recording with detailed timestamp information.

        Args:
            audio_input (str | Path): Path to the audio file to transcribe
            language (str, optional): Language code (e.g., 'en', 'es', 'fr')
            **kwargs: Additional arguments to pass to transcribe()

        Returns:
            list: List of segments, each containing:
                - 'start': Start time in seconds
                - 'end': End time in seconds
                - 'text': Transcribed text for this segment
        """
        result = self.transcribe(
            audio_input,
            language=language,
            response_format="verbose_json",
            **kwargs
        )

        # Extract segments from verbose response
        segments = []
        if 'segments' in result:
            for segment in result['segments']:
                segments.append({
                    'start': segment.get('start', 0),
                    'end': segment.get('end', 0),
                    'text': segment.get('text', '').strip()
                })

        return segments

    def save_to_file(
        self,
        text: str,
        output_path: str | Path,
        include_timestamps: bool = False,
        segments: list[dict[str, Any]] | None = None
    ) -> Path:
        """
        Save transcribed text to a file.

        Args:
            text (str): The transcribed text to save
            output_path (str | Path): Path where the file will be saved
            include_timestamps (bool): If True, format with timestamps (requires segments)
            segments (list, optional): Timestamp segments for formatted output

        Returns:
            Path: The path to the saved file

        Raises:
            ValueError: If include_timestamps is True but segments is None
        """
        output_path = Path(output_path)

        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if include_timestamps:
            if not segments:
                raise ValueError(
                    "Cannot include timestamps without segments. "
                    "Use transcribe_with_timestamps() to get segments first."
                )

            # Format with timestamps
            lines = []
            for i, segment in enumerate(segments, 1):
                timestamp = f"[{self._format_time(segment['start'])} -> {self._format_time(segment['end'])}]"
                lines.append(f"{timestamp} {segment['text']}")

            content = '\n'.join(lines)
        else:
            content = text

        # Write to file
        output_path.write_text(content, encoding='utf-8')

        return output_path

    def transcribe_and_save(
        self,
        audio_input: str | Path,
        output_path: str | Path,
        language: str | None = None,
        include_timestamps: bool = False,
        **kwargs
    ) -> Path:
        """
        Transcribe an audio file and save the result to a text file.

        This is a convenience method that combines transcription and file saving.

        Args:
            audio_input (str | Path): Path to the audio file to transcribe
            output_path (str | Path): Path where the transcription will be saved
            language (str, optional): Language code (e.g., 'en', 'es', 'fr')
            include_timestamps (bool): If True, include timestamps in the output
            **kwargs: Additional arguments to pass to transcribe()

        Returns:
            Path: The path to the saved file
        """
        if include_timestamps:
            # Get transcription with timestamps
            segments = self.transcribe_with_timestamps(
                audio_input,
                language=language,
                **kwargs
            )
            # Combine all segment text
            text = ' '.join(segment['text'] for segment in segments)

            # Save with timestamps
            return self.save_to_file(
                text,
                output_path,
                include_timestamps=True,
                segments=segments
            )
        else:
            # Get plain text transcription
            text = self.transcribe_to_text(
                audio_input,
                language=language,
                **kwargs
            )

            # Save without timestamps
            return self.save_to_file(text, output_path)

    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Format seconds into MM:SS or HH:MM:SS format.

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
