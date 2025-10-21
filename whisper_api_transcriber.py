"""
Whisper AI API Transcription Class for Note Generation

This module provides a WhisperAPITranscriber class that handles audio transcription
using OpenAI's Whisper API (cloud-based service).
"""

import os
from typing import Any
from pathlib import Path


class WhisperAPITranscriber:
    """
    A class for transcribing audio recordings using OpenAI's Whisper API.

    This class sends audio files to OpenAI's cloud API for transcription,
    requiring an API key but offering fast processing without local compute.

    Attributes:
        api_key (str): OpenAI API key
        model (str): The Whisper model to use (currently only 'whisper-1' available)
        client: OpenAI client instance
    """

    SUPPORTED_FORMATS = [
        '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm', '.flac'
    ]
    MAX_FILE_SIZE_MB = 25  # OpenAI API limit

    def __init__(self, api_key: str | None = None, model: str = "whisper-1"):
        """
        Initialize the Whisper API transcriber.

        Args:
            api_key (str, optional): OpenAI API key. If None, will try to get from
                                    OPENAI_API_KEY environment variable.
            model (str): Model to use. Currently only 'whisper-1' is available.

        Raises:
            ValueError: If API key is not provided and not in environment
            ImportError: If openai package is not installed
        """
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Either pass it as 'api_key' parameter "
                "or set the OPENAI_API_KEY environment variable."
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
        print("OpenAI API client initialized successfully!")

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

        print(f"Transcribing {audio_path.name} using OpenAI API...")

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

        print("Transcription complete!")

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

        This is a convenience method that returns just the transcribed text
        without the additional metadata.

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

    def transcribe_to_srt(
        self,
        audio_input: str | Path,
        language: str | None = None,
        **kwargs
    ) -> str:
        """
        Transcribe an audio recording and return SRT subtitle format.

        Args:
            audio_input (str | Path): Path to the audio file to transcribe
            language (str, optional): Language code (e.g., 'en', 'es', 'fr')
            **kwargs: Additional arguments to pass to transcribe()

        Returns:
            str: Transcription in SRT subtitle format
        """
        result = self.transcribe(
            audio_input,
            language=language,
            response_format="srt",
            **kwargs
        )

        if isinstance(result, dict):
            return result['text']
        return result

    def transcribe_to_vtt(
        self,
        audio_input: str | Path,
        language: str | None = None,
        **kwargs
    ) -> str:
        """
        Transcribe an audio recording and return WebVTT subtitle format.

        Args:
            audio_input (str | Path): Path to the audio file to transcribe
            language (str, optional): Language code (e.g., 'en', 'es', 'fr')
            **kwargs: Additional arguments to pass to transcribe()

        Returns:
            str: Transcription in WebVTT subtitle format
        """
        result = self.transcribe(
            audio_input,
            language=language,
            response_format="vtt",
            **kwargs
        )

        if isinstance(result, dict):
            return result['text']
        return result

    def save_transcription(
        self,
        audio_input: str | Path,
        output_path: str | Path,
        language: str | None = None,
        include_timestamps: bool = False,
        format: str = "text",
        **kwargs
    ):
        """
        Transcribe audio and save the result to a file.

        Args:
            audio_input (str | Path): Path to the audio file to transcribe
            output_path (str | Path): Path where the transcription will be saved
            language (str, optional): Language code (e.g., 'en', 'es', 'fr')
            include_timestamps (bool): If True, use SRT format with timestamps
            format (str): Output format - 'text', 'srt', 'vtt'. Default is 'text'.
            **kwargs: Additional arguments to pass to transcribe()
        """
        output_path = Path(output_path)

        # Determine format
        if include_timestamps and format == "text":
            format = "srt"

        # Get transcription in the desired format
        if format == "srt":
            content = self.transcribe_to_srt(audio_input, language=language, **kwargs)
        elif format == "vtt":
            content = self.transcribe_to_vtt(audio_input, language=language, **kwargs)
        else:
            content = self.transcribe_to_text(audio_input, language=language, **kwargs)

        # Save to file
        output_path.write_text(content, encoding='utf-8')
        print(f"Transcription saved to: {output_path}")

    def translate(
        self,
        audio_input: str | Path,
        prompt: str | None = None,
        response_format: str = "json",
        temperature: float = 0.0,
    ) -> dict[str, Any]:
        """
        Translate audio to English using OpenAI's Whisper API.

        This uses the translation endpoint which translates any language to English.

        Args:
            audio_input (str | Path): Path to the audio file to translate
            prompt (str, optional): Optional text to guide the model's style
            response_format (str): Format of the response. Options: 'json', 'text',
                                  'srt', 'verbose_json', 'vtt'. Default is 'json'.
            temperature (float): Sampling temperature between 0 and 1. Default is 0.

        Returns:
            dict[str, Any]: Translation result containing:
                - 'text': The translated text (in English)
        """
        # Validate input file
        audio_path = Path(audio_input)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_input}")

        print(f"Translating {audio_path.name} to English using OpenAI API...")

        # Open and send file to translation API
        with open(audio_path, 'rb') as audio_file:
            params = {
                "model": self.model,
                "file": audio_file,
                "response_format": response_format,
                "temperature": temperature,
            }

            if prompt:
                params["prompt"] = prompt

            response = self.client.audio.translations.create(**params)

        print("Translation complete!")

        # Format response
        if response_format == "json":
            return {"text": response.text}
        elif response_format == "verbose_json":
            return response.model_dump()
        else:
            return {"text": response}


# Example usage
if __name__ == "__main__":
    # Example: Create transcriber with API key
    # You can either pass the API key directly or set OPENAI_API_KEY env variable

    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("Please set your OPENAI_API_KEY environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("\nOr pass it directly:")
        print("  transcriber = WhisperAPITranscriber(api_key='your-api-key-here')")
        exit(1)

    transcriber = WhisperAPITranscriber()

    # Example audio file path (replace with your actual file)
    audio_file = "recording.mp3"

    if os.path.exists(audio_file):
        # Simple text transcription
        text = transcriber.transcribe_to_text(audio_file)
        print("\nTranscribed text:")
        print(text)

        # Get timestamps
        segments = transcriber.transcribe_with_timestamps(audio_file)
        print("\nWith timestamps:")
        for segment in segments:
            print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")

        # Save to file
        transcriber.save_transcription(audio_file, "transcription.txt")

        # Save as SRT subtitle file
        transcriber.save_transcription(audio_file, "transcription.srt", format="srt")
    else:
        print(f"Example audio file '{audio_file}' not found.")
        print("Please provide a valid audio file path to test the transcriber.")
