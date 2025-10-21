"""
Note Templates Module

This module provides utilities for loading and using different note-taking templates
to format transcriptions according to specific user needs.
"""

from pathlib import Path
from typing import Literal


# Define available template types
NoteType = Literal[
    "study_guide",
    "meeting_minutes",
    "instructions",
    "summary",
    "verbatim_transcript"
]


class NoteTemplates:
    """
    Utility class for managing note-taking templates.

    Templates provide structured prompts that guide the transcription API
    to format output in specific ways (study notes, meeting minutes, etc.).
    """

    # Template descriptions for user selection
    TEMPLATE_INFO = {
        "study_guide": {
            "name": "Study Guide / Comprehensive Notes",
            "description": "Detailed educational notes with key concepts, definitions, examples, and organized by topic. Best for lectures, courses, or learning material.",
            "best_for": "Lectures, educational content, learning material, study sessions"
        },
        "meeting_minutes": {
            "name": "Meeting Minutes",
            "description": "Professional meeting notes with agenda items, decisions, action items, and deadlines. Best for business meetings and team discussions.",
            "best_for": "Business meetings, team syncs, project discussions, planning sessions"
        },
        "instructions": {
            "name": "Step-by-Step Instructions",
            "description": "Clear tutorial-style notes with numbered steps, prerequisites, troubleshooting, and tips. Best for how-to content and tutorials.",
            "best_for": "Tutorials, how-to guides, training sessions, demonstrations"
        },
        "summary": {
            "name": "Brief Summary",
            "description": "Condensed notes focusing on key points and takeaways only. Best when you need a quick overview without details.",
            "best_for": "Quick reviews, executive summaries, condensed overviews, time-saving"
        },
        "verbatim_transcript": {
            "name": "Verbatim Transcript with Timestamps",
            "description": "Word-for-word transcription with timestamps and speaker identification. Best for accurate record-keeping and detailed review.",
            "best_for": "Legal records, interviews, detailed analysis, accurate documentation"
        }
    }

    def __init__(self, templates_dir: str | Path | None = None):
        """
        Initialize the template manager.

        Args:
            templates_dir: Path to templates directory. If None, uses default location.
        """
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            # Default: templates/ folder in project root
            self.templates_dir = Path(__file__).parent.parent / "templates"

        if not self.templates_dir.exists():
            raise FileNotFoundError(
                f"Templates directory not found: {self.templates_dir}\n"
                f"Make sure the templates folder exists with the template files."
            )

    def get_template(self, note_type: NoteType) -> str:
        """
        Load a template by type.

        Args:
            note_type: The type of notes to generate

        Returns:
            str: The template content to use as a prompt

        Raises:
            FileNotFoundError: If the template file doesn't exist
            ValueError: If the note_type is not recognized
        """
        if note_type not in self.TEMPLATE_INFO:
            valid_types = ", ".join(self.TEMPLATE_INFO.keys())
            raise ValueError(
                f"Invalid note type: '{note_type}'\n"
                f"Valid types: {valid_types}"
            )

        template_file = self.templates_dir / f"{note_type}.txt"

        if not template_file.exists():
            raise FileNotFoundError(
                f"Template file not found: {template_file}\n"
                f"Expected template file for '{note_type}' at this location."
            )

        return template_file.read_text(encoding='utf-8')

    def list_templates(self) -> dict[str, dict[str, str]]:
        """
        Get information about all available templates.

        Returns:
            dict: Dictionary mapping template IDs to their info
        """
        return self.TEMPLATE_INFO.copy()

    def print_available_templates(self):
        """
        Print a formatted list of available templates with descriptions.
        Useful for helping users choose the right template.
        """
        print("\n" + "="*70)
        print("AVAILABLE NOTE TEMPLATES")
        print("="*70 + "\n")

        for template_id, info in self.TEMPLATE_INFO.items():
            print(f"📋 {info['name']}")
            print(f"   ID: '{template_id}'")
            print(f"   Description: {info['description']}")
            print(f"   Best for: {info['best_for']}")
            print()

        print("="*70)
        print("Usage: transcriber.transcribe(..., prompt=templates.get_template('template_id'))")
        print("="*70 + "\n")

    @staticmethod
    def get_template_id_from_user() -> NoteType:
        """
        Interactive helper to get template selection from user input.

        Returns:
            NoteType: The selected template ID
        """
        templates = NoteTemplates()
        templates.print_available_templates()

        valid_ids = list(templates.TEMPLATE_INFO.keys())

        while True:
            choice = input("Enter template ID: ").strip().lower()

            if choice in valid_ids:
                return choice  # type: ignore
            else:
                print(f"Invalid choice. Please enter one of: {', '.join(valid_ids)}")


# Convenience function for quick access
def load_template(note_type: NoteType) -> str:
    """
    Quick helper to load a template.

    Args:
        note_type: The type of notes to generate

    Returns:
        str: The template content

    Example:
        >>> from src.note_templates import load_template
        >>> prompt = load_template('study_guide')
        >>> transcriber.transcribe(audio_file, prompt=prompt)
    """
    templates = NoteTemplates()
    return templates.get_template(note_type)
