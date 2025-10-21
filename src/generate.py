"""
Note Generator using GPT API

This module provides a NoteGenerator class that takes raw transcription text
and formats it into structured notes using OpenAI's GPT models.
"""

import os
from typing import Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class NoteGenerator:
    """
    Generates formatted notes from raw transcription text using GPT API.

    This class takes plain transcription text and uses GPT models to
    restructure and format it according to specific note-taking templates.
    """

    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Initialize the note generator.

        Args:
            model (str): GPT model to use. Options:
                        - 'gpt-3.5-turbo' (faster, cheaper)
                        - 'gpt-4' (better quality, more expensive)
                        - 'gpt-4-turbo-preview' (balance of speed and quality)

        Raises:
            ValueError: If API key is not provided
            ImportError: If openai package is not installed
        """
        self.api_key = os.getenv('OPENAI_KEY')

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. "
                "Set the OPENAI_KEY environment variable in your .env file."
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

    def generate_notes(
        self,
        transcription: str,
        template: str,
        custom_instructions: str = ""
    ) -> str:
        """
        Generate formatted notes from raw transcription using a template.

        Args:
            transcription (str): Raw transcription text from Whisper
            template (str): The formatting template/instructions
            custom_instructions (str): Additional custom instructions (optional)

        Returns:
            str: Formatted notes according to the template

        Raises:
            ValueError: If transcription is empty or API call fails
        """
        if not transcription or not transcription.strip():
            raise ValueError("Transcription text cannot be empty")

        # Build the system message
        system_message = template

        # Build the user message
        user_message = f"""Please format the following transcription according to the instructions provided.

TRANSCRIPTION:
{transcription}
"""

        if custom_instructions:
            user_message += f"\n\nADDITIONAL INSTRUCTIONS:\n{custom_instructions}"

        try:
            # Make API call to GPT
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,  # Lower temperature for more consistent formatting
                max_tokens=4000,   # Adjust based on expected note length
            )

            # Extract the formatted notes
            formatted_notes = response.choices[0].message.content

            if not formatted_notes:
                raise ValueError("GPT returned empty response")

            return formatted_notes.strip()

        except Exception as e:
            raise ValueError(f"Failed to generate notes with GPT: {str(e)}") from e

    def generate_notes_streaming(
        self,
        transcription: str,
        template: str,
        custom_instructions: str = ""
    ):
        """
        Generate formatted notes with streaming output (for real-time display).

        Args:
            transcription (str): Raw transcription text from Whisper
            template (str): The formatting template/instructions
            custom_instructions (str): Additional custom instructions (optional)

        Yields:
            str: Chunks of formatted notes as they're generated

        Raises:
            ValueError: If transcription is empty or API call fails
        """
        if not transcription or not transcription.strip():
            raise ValueError("Transcription text cannot be empty")

        # Build messages
        system_message = template

        user_message = f"""Please format the following transcription according to the instructions provided.

TRANSCRIPTION:
{transcription}
"""

        if custom_instructions:
            user_message += f"\n\nADDITIONAL INSTRUCTIONS:\n{custom_instructions}"

        try:
            # Make streaming API call
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=4000,
                stream=True
            )

            # Yield chunks as they arrive
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            raise ValueError(f"Failed to stream notes generation: {str(e)}") from e

    def estimate_cost(self, transcription: str, template: str) -> dict:
        """
        Estimate the cost of generating notes.

        Args:
            transcription (str): The transcription text
            template (str): The template text

        Returns:
            dict: Estimated cost information including:
                - 'input_tokens': Estimated input tokens
                - 'output_tokens': Estimated output tokens
                - 'estimated_cost': Estimated cost in USD
        """
        # Rough token estimation (1 token ≈ 4 characters)
        input_chars = len(transcription) + len(template)
        input_tokens = input_chars // 4

        # Output is usually similar to input for note formatting
        output_tokens = input_tokens  # Conservative estimate

        # Pricing (as of 2024, may change)
        pricing = {
            'gpt-3.5-turbo': {'input': 0.0005 / 1000, 'output': 0.0015 / 1000},
            'gpt-4': {'input': 0.03 / 1000, 'output': 0.06 / 1000},
            'gpt-4-turbo-preview': {'input': 0.01 / 1000, 'output': 0.03 / 1000},
        }

        model_pricing = pricing.get(self.model, pricing['gpt-3.5-turbo'])

        input_cost = input_tokens * model_pricing['input']
        output_cost = output_tokens * model_pricing['output']
        total_cost = input_cost + output_cost

        return {
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'estimated_cost_usd': round(total_cost, 4),
            'model': self.model
        }


# Convenience function
def generate_notes_from_transcription(
    transcription: str,
    template: str,
    model: str = "gpt-3.5-turbo"
) -> str:
    """
    Quick helper to generate formatted notes.

    Args:
        transcription: Raw transcription text
        template: Formatting template/instructions
        model: GPT model to use

    Returns:
        str: Formatted notes

    Example:
        >>> from src.generate import generate_notes_from_transcription
        >>> from src.note_templates import load_template
        >>>
        >>> template = load_template('study_guide')
        >>> notes = generate_notes_from_transcription(transcription, template)
    """
    generator = NoteGenerator(model=model)
    return generator.generate_notes(transcription, template)
