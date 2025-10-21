"""
Note Generator - Main Frontend

This is the main user interface for the Note Generator application.
Users can transcribe audio from files or YouTube videos using various note templates.
"""

import sys
from pathlib import Path
from transcribe import Transcriber
from note_templates import NoteTemplates
from youtube_downloader import YouTubeDownloader


class NoteGeneratorApp:
    """Main application class for the Note Generator."""

    def __init__(self):
        """Initialize the application."""
        self.transcriber = None
        self.templates = None
        self.youtube_downloader = None

        # Initialize components
        self._initialize_components()

    def _initialize_components(self):
        """Initialize transcriber and template manager."""
        try:
            self.transcriber = Transcriber()
            self.templates = NoteTemplates()
            self.youtube_downloader = YouTubeDownloader()
            return True
        except ValueError as e:
            print(f"\n❌ Error: {e}")
            print("\nPlease make sure you have:")
            print("1. Created a .env file in the project root")
            print("2. Added your OPENAI_KEY to the .env file")
            print("\nExample .env file:")
            print("OPENAI_KEY=your-api-key-here")
            return False

    def run(self):
        """Run the main application."""
        if not self.transcriber:
            if not self._initialize_components():
                sys.exit(1)

        self._print_welcome()

        # Main application loop
        while True:
            choice = self._show_main_menu()

            if choice == '1':
                self._process_audio_file()
            elif choice == '2':
                self._process_youtube_link()
            elif choice == '3':
                self._show_template_info()
            elif choice == '4':
                print("\nThank you for using Note Generator!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")

            # Ask if they want to continue
            if choice in ['1', '2']:
                print("\n" + "="*70)
                continue_choice = input("\nWould you like to transcribe another? (y/n): ").strip().lower()
                if continue_choice != 'y':
                    print("\nThank you for using Note Generator!")
                    break

    def _print_welcome(self):
        """Print welcome message."""
        print("\n" + "="*70)
        print("📝 WELCOME TO NOTE GENERATOR")
        print("="*70)
        print("\nTransform your audio into organized, formatted notes!")
        print("✓ Support for audio files and YouTube videos")
        print("✓ 5 different note templates available")
        print("✓ Powered by OpenAI Whisper API")
        print("="*70)

    def _show_main_menu(self) -> str:
        """
        Show the main menu and get user choice.

        Returns:
            User's menu choice
        """
        print("\n" + "="*70)
        print("MAIN MENU")
        print("="*70)
        print("\n1. Transcribe from Audio File")
        print("2. Transcribe from YouTube Link")
        print("3. View Template Information")
        print("4. Exit")

        return input("\nEnter your choice (1-4): ").strip()

    def _process_audio_file(self):
        """Process transcription from an audio file."""
        print("\n" + "="*70)
        print("TRANSCRIBE FROM AUDIO FILE")
        print("="*70)

        # Get audio file path
        file_path = input("\nEnter the path to your audio file: ").strip()
        file_path = file_path.strip('"').strip("'")  # Remove quotes if present

        audio_path = Path(file_path)

        if not audio_path.exists():
            print(f"\n❌ Error: File not found: {file_path}")
            return

        # Get template choice
        template_id = self._select_template()
        if not template_id:
            return

        # Get output filename
        output_path = self._get_output_filename(audio_path.stem, template_id)

        # Process
        self._transcribe_and_save(audio_path, output_path, template_id)

    def _process_youtube_link(self):
        """Process transcription from a YouTube link."""
        print("\n" + "="*70)
        print("TRANSCRIBE FROM YOUTUBE")
        print("="*70)

        # Get YouTube URL
        youtube_url = input("\nEnter the YouTube URL: ").strip()

        # Validate URL
        if not self.youtube_downloader.is_valid_youtube_url(youtube_url):
            print("\n❌ Error: Invalid YouTube URL")
            print("Please provide a valid YouTube link (e.g., https://youtube.com/watch?v=...)")
            return

        # Get template choice
        template_id = self._select_template()
        if not template_id:
            return

        try:
            # Download audio
            print("\n" + "-"*70)
            print("DOWNLOADING AUDIO FROM YOUTUBE")
            print("-"*70)

            audio_path = self.youtube_downloader.download_audio(youtube_url)

            # Get output filename
            output_path = self._get_output_filename(audio_path.stem, template_id)

            # Process
            print("\n" + "-"*70)
            print("TRANSCRIBING AUDIO")
            print("-"*70)

            self._transcribe_and_save(audio_path, output_path, template_id)

            # Ask about cleanup
            cleanup = input("\nWould you like to delete the downloaded audio file? (y/n): ").strip().lower()
            if cleanup == 'y':
                audio_path.unlink()
                print(f"✓ Deleted: {audio_path}")

        except Exception as e:
            print(f"\n❌ Error: {e}")

    def _select_template(self) -> str | None:
        """
        Let user select a note template.

        Returns:
            Template ID or None if cancelled
        """
        print("\n" + "-"*70)
        print("SELECT NOTE TEMPLATE")
        print("-"*70)

        template_info = self.templates.list_templates()

        # Display options
        print("\nAvailable Templates:")
        for i, (template_id, info) in enumerate(template_info.items(), 1):
            print(f"\n{i}. {info['name']}")
            print(f"   {info['description']}")
            print(f"   Best for: {info['best_for']}")

        # Get choice
        while True:
            choice = input(f"\nSelect template (1-{len(template_info)}) or 'c' to cancel: ").strip()

            if choice.lower() == 'c':
                return None

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(template_info):
                    template_id = list(template_info.keys())[choice_num - 1]
                    print(f"\n✓ Selected: {template_info[template_id]['name']}")
                    return template_id
                else:
                    print(f"❌ Please enter a number between 1 and {len(template_info)}")
            except ValueError:
                print("❌ Please enter a valid number or 'c' to cancel")

    def _get_output_filename(self, base_name: str, template_id: str) -> Path:
        """
        Get output filename from user or generate default.

        Args:
            base_name: Base name from the audio file
            template_id: Selected template ID

        Returns:
            Path for the output file
        """
        print("\n" + "-"*70)
        print("OUTPUT FILENAME")
        print("-"*70)

        default_name = f"{base_name}_{template_id}_notes.txt"
        print(f"\nDefault: output/{default_name}")

        custom = input("Enter custom filename (or press Enter for default): ").strip()

        if custom:
            # Ensure .txt extension
            if not custom.endswith('.txt'):
                custom += '.txt'
            output_path = Path("output") / custom
        else:
            output_path = Path("output") / default_name

        return output_path

    def _transcribe_and_save(self, audio_path: Path, output_path: Path, template_id: str):
        """
        Perform transcription and save the result.

        Args:
            audio_path: Path to the audio file
            output_path: Path for the output file
            template_id: Template ID to use
        """
        try:
            print(f"\n📝 Transcribing: {audio_path.name}")
            print(f"📋 Template: {self.templates.TEMPLATE_INFO[template_id]['name']}")
            print(f"💾 Output: {output_path}")
            print("\n⏳ Processing... (this may take a few minutes)")

            # Load template
            prompt = self.templates.get_template(template_id)

            # Transcribe and save
            saved_path = self.transcriber.transcribe_and_save(
                audio_path,
                output_path,
                prompt=prompt,
                language='en'  # You can make this configurable
            )

            print("\n" + "="*70)
            print("✅ SUCCESS!")
            print("="*70)
            print(f"\n📄 Notes saved to: {saved_path}")

            # Show preview
            content = saved_path.read_text(encoding='utf-8')
            preview_length = min(500, len(content))

            print(f"\n📖 Preview (first {preview_length} characters):")
            print("-"*70)
            print(content[:preview_length])
            if len(content) > preview_length:
                print("...")
            print("-"*70)

        except Exception as e:
            print(f"\n❌ Error during transcription: {e}")

    def _show_template_info(self):
        """Display detailed information about all templates."""
        print("\n" + "="*70)
        print("TEMPLATE INFORMATION")
        print("="*70)

        self.templates.print_available_templates()

        input("\nPress Enter to return to main menu...")


def main():
    """Main entry point."""
    # Check for command-line arguments
    if len(sys.argv) > 1:
        # Quick mode: provide audio file as argument
        audio_file = sys.argv[1]

        try:
            transcriber = Transcriber()
            templates = NoteTemplates()
        except ValueError as e:
            print(f"Error: {e}")
            print("\nMake sure you have created a .env file with your OPENAI_KEY")
            sys.exit(1)

        print(f"\n📝 Quick Transcription Mode")
        print(f"Audio file: {audio_file}")

        # Show templates
        templates.print_available_templates()

        # Get template choice
        template_id = NoteTemplates.get_template_id_from_user()

        # Get output filename
        audio_path = Path(audio_file)
        output_file = f"output/{audio_path.stem}_{template_id}_notes.txt"

        # Transcribe
        print(f"\n⏳ Transcribing...")
        prompt = templates.get_template(template_id)

        saved_path = transcriber.transcribe_and_save(
            audio_file,
            output_file,
            prompt=prompt
        )

        print(f"\n✅ Success! Notes saved to: {saved_path}")

    else:
        # Interactive mode
        app = NoteGeneratorApp()
        app.run()


if __name__ == "__main__":
    main()
