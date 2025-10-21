"""
YouTube Audio Downloader for Transcription

This module provides functionality to download audio from YouTube videos
for transcription purposes.
"""

import os
from pathlib import Path
from typing import Optional
from config import DOWNLOADS_DIR


class YouTubeDownloader:
    """
    Downloads audio from YouTube videos for transcription.

    Uses yt-dlp to download audio in a format compatible with OpenAI.
    """

    def __init__(self, output_dir: str | Path = DOWNLOADS_DIR):
        """
        Initialize the YouTube downloader.

        Args:
            output_dir: Directory where audio files will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_audio(
        self,
        youtube_url: str,
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Download audio from a YouTube video.

        Args:
            youtube_url: The YouTube video URL
            output_filename: Optional custom filename (without extension)
                           If None, uses the video title

        Returns:
            Path: Path to the downloaded audio file

        Raises:
            ImportError: If yt-dlp is not installed
            ValueError: If the URL is invalid or download fails
        """
        try:
            import yt_dlp
        except ImportError as e:
            raise ImportError(
                "yt-dlp package not installed. "
                "Install it with: pip install yt-dlp"
            ) from e

        # Configure yt-dlp options optimized for Whisper API compatibility
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }, {
                'key': 'FFmpegMetadata',
            }],
            'postprocessor_args': [
                '-ar', '16000',  # Whisper uses 16kHz sample rate
                '-ac', '1',       # Convert to mono
                '-b:a', '128k',   # Constant bitrate for compatibility
            ],
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'keepvideo': False,
        }

        # If custom filename provided, use it
        if output_filename:
            # Remove any extension if provided
            output_filename = Path(output_filename).stem
            ydl_opts['outtmpl'] = str(self.output_dir / f'{output_filename}.%(ext)s')

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info first
                print(f"Fetching video information...")
                info = ydl.extract_info(youtube_url, download=False)
                video_title = info.get('title', 'video')
                duration = info.get('duration', 0)

                # Show video info
                print(f"\nVideo: {video_title}")
                print(f"Duration: {self._format_duration(duration)}")

                # Download
                print(f"\nDownloading audio...")
                ydl.download([youtube_url])

                # Determine output filename
                if output_filename:
                    expected_file = self.output_dir / f"{output_filename}.mp3"
                else:
                    # yt-dlp sanitizes the title for the filename
                    sanitized_title = ydl.prepare_filename(info)
                    expected_file = Path(sanitized_title).with_suffix('.mp3')

                # Find the downloaded file
                audio_file = self._find_downloaded_file(video_title, output_filename)

                if not audio_file:
                    raise ValueError(
                        f"Download completed but could not find the audio file in {self.output_dir}"
                    )

                # Validate the downloaded file
                if not self._validate_audio_file(audio_file):
                    raise ValueError(
                        f"Downloaded audio file appears to be invalid or corrupted. "
                        f"File: {audio_file}, Size: {audio_file.stat().st_size} bytes"
                    )

                print(f"✓ Audio downloaded: {audio_file}")
                print(f"  File size: {audio_file.stat().st_size / (1024*1024):.2f} MB")
                return audio_file

        except Exception as e:
            raise ValueError(f"Failed to download audio from YouTube: {str(e)}") from e

    def _find_downloaded_file(
        self,
        video_title: str,
        custom_filename: Optional[str] = None
    ) -> Optional[Path]:
        """
        Find the downloaded audio file in the output directory.

        Args:
            video_title: The video title
            custom_filename: Custom filename if provided

        Returns:
            Path to the file if found, None otherwise
        """
        if custom_filename:
            # Check for custom filename
            expected = self.output_dir / f"{custom_filename}.mp3"
            if expected.exists():
                return expected

        # Look for the most recently created mp3 file
        mp3_files = list(self.output_dir.glob("*.mp3"))
        if mp3_files:
            # Return the most recently created file
            return max(mp3_files, key=lambda p: p.stat().st_mtime)

        return None

    @staticmethod
    def _validate_audio_file(audio_path: Path) -> bool:
        """
        Validate that the downloaded audio file is usable.

        Args:
            audio_path: Path to the audio file

        Returns:
            True if file is valid, False otherwise
        """
        # Check file exists
        if not audio_path.exists():
            return False

        # Check file size (should be at least 1KB)
        file_size = audio_path.stat().st_size
        if file_size < 1024:  # Less than 1KB is suspicious
            return False

        # Check if file has .mp3 extension
        if audio_path.suffix.lower() != '.mp3':
            return False

        # Basic MP3 header check (MP3 files start with ID3 or 0xFF 0xFB)
        try:
            with open(audio_path, 'rb') as f:
                header = f.read(3)
                # Check for ID3 tag or MP3 sync word
                if header.startswith(b'ID3') or header[:2] in [b'\xff\xfb', b'\xff\xf3', b'\xff\xf2']:
                    return True
        except Exception:
            pass

        # If we can't verify the header, assume it's okay if size is reasonable
        return file_size > 10000  # At least 10KB



    @staticmethod
    def _format_duration(seconds: int) -> str:
        """
        Format duration in seconds to HH:MM:SS or MM:SS.

        Args:
            seconds: Duration in seconds

        Returns:
            Formatted duration string
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

    @staticmethod
    def is_valid_youtube_url(url: str) -> bool:
        """
        Check if a URL is a valid YouTube URL.

        Args:
            url: URL to check

        Returns:
            True if valid YouTube URL, False otherwise
        """
        youtube_domains = [
            'youtube.com',
            'youtu.be',
            'www.youtube.com',
            'm.youtube.com'
        ]

        url_lower = url.lower()
        return any(domain in url_lower for domain in youtube_domains)

    def cleanup_old_downloads(self, keep_latest: int = 5):
        """
        Remove old downloaded files, keeping only the most recent ones.

        Args:
            keep_latest: Number of most recent files to keep
        """
        mp3_files = list(self.output_dir.glob("*.mp3"))

        if len(mp3_files) <= keep_latest:
            return

        # Sort by modification time (newest first)
        mp3_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        # Remove old files
        for old_file in mp3_files[keep_latest:]:
            print(f"Removing old download: {old_file.name}")
            old_file.unlink()


# Convenience function
def download_youtube_audio(youtube_url: str, output_dir: str = DOWNLOADS_DIR) -> Path:
    """
    Quick helper to download YouTube audio.

    Args:
        youtube_url: The YouTube video URL
        output_dir: Directory to save the audio file

    Returns:
        Path to the downloaded audio file

    Example:
        >>> from src.youtube_downloader import download_youtube_audio
        >>> audio_file = download_youtube_audio('https://youtube.com/watch?v=...')
        >>> print(audio_file)
    """
    downloader = YouTubeDownloader(output_dir)
    return downloader.download_audio(youtube_url)
