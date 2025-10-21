"""
Audio Transcription Backend for Note Generation

This module provides a Transcriber class that handles audio transcription
using OpenAI's Whisper API.
"""

import os
from typing import Any
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Transcriber:
    """
    Backend class for transcribing audio recordings using OpenAI's Whisper API.

    This class handles the core transcription functionality, sending audio files
    to OpenAI's cloud API and returning the transcribed text.

    Attributes:
        api_key (str): OpenAI API key loaded from environment
        model (str): The Whisper model to use
        client: OpenAI client instance
    """

    SUPPORTED_FORMATS = [
        '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm', '.flac'
    ]
    MAX_FILE_SIZE_MB = 25  # OpenAI API limit

    def __init__(self, api_key: str | None = None, model: str = "whisper-1"):
        """
        Initialize the transcriber.

        Args:
            api_key (str, optional): OpenAI API key. If None, will try to get from
                                    OPENAI_KEY environment variable.
            model (str): Model to use. Currently only 'whisper-1' is available.

        Raises:
            ValueError: If API key is not provided and not in environment
            ImportError: If openai package is not installed
        """
        # Get API key from parameter or environment variable (OPENAI_KEY)
        self.api_key = api_key or os.getenv('OPENAI_KEY')

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Either pass it as 'api_key' parameter "
                "or set the OPENAI_KEY environment variable in your .env file."
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
        Transcribe an audio recording using OpenAI's Whisper API.

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
