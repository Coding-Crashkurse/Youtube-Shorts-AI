import os
import typer
from colorama import Fore, Style
from pexels import PexelsImageSearch
from scale_img import ImageResizer
from whisper_api import OpenAITranscriptGenerator
from create_video import VideoCreator
from youtube import upload_video
from cleanup import clean
from dotenv import load_dotenv, find_dotenv

app = typer.Typer()

load_dotenv(find_dotenv())

@app.command()
def clean_folder():
    """
    Run the cleanup routine.
    """
    try:
        typer.echo(f"{Fore.GREEN}Performing cleanup...{Style.RESET_ALL}")
        clean()
        typer.echo(f"{Fore.GREEN}Cleanup successful.{Style.RESET_ALL}")
    except Exception as e:
        typer.echo(f"{Fore.RED}Error during cleanup: {e}{Style.RESET_ALL}")



@app.command()
def main(fact: str = typer.Option(..., help="Fact for the video"),
         do_cleanup: bool = typer.Option(True, help="Perform cleanup before running the script"),
         upload: bool = typer.Option(True, help="Upload video after creation"),
         target_width: int = typer.Option(1080, help="Target width for image resizing"),
         target_height: int = typer.Option(1920, help="Target height for image resizing")):
    try:
        if do_cleanup:
            typer.echo(f"{Fore.GREEN}Performing cleanup...{Style.RESET_ALL}")
            clean()
    except Exception as e:
        typer.echo(f"{Fore.RED}Error during cleanup: {e}{Style.RESET_ALL}")
        return

    try:
        typer.echo(f"{Fore.BLUE}Searching for {fact} images...{Style.RESET_ALL}")
        api_key = os.getenv("PEXELS_API_KEY")
        pexels = PexelsImageSearch(api_key)
        pexels.process_images(fact)
    except Exception as e:
        typer.echo(f"{Fore.RED}Error searching for images: {e}{Style.RESET_ALL}")
        return

    try:
        typer.echo(f"{Fore.YELLOW}Resizing images to {target_width}x{target_height}...{Style.RESET_ALL}")
        # 2. Resize images
        resizer = ImageResizer(target_width, target_height)
        resizer.process_dir()
    except Exception as e:
        typer.echo(f"{Fore.RED}Error resizing images: {e}{Style.RESET_ALL}")
        return

    try:
        typer.echo(f"{Fore.MAGENTA}Generating transcript and audio for {fact}...{Style.RESET_ALL}")
        # 3. Use Whisper API for MP3 and SRT file
        generator = OpenAITranscriptGenerator()
        generator.process_request(fact)
    except Exception as e:
        typer.echo(f"{Fore.RED}Error generating transcript and audio: {e}{Style.RESET_ALL}")
        return

    try:
        typer.echo(f"{Fore.CYAN}Creating video...{Style.RESET_ALL}")
        # 4. Create video
        video_creator = VideoCreator('transcript.srt', 'audio.mp3')
        video_creator.create_video()
    except Exception as e:
        typer.echo(f"{Fore.RED}Error creating video: {e}{Style.RESET_ALL}")
        return

    try:
        if upload:
            typer.echo(f"{Fore.GREEN}Uploading video to YouTube...{Style.RESET_ALL}")
            upload_video(video_path="output_video.mp4", topic=fact)
    except Exception as e:
        typer.echo(f"{Fore.RED}Error uploading video: {e}{Style.RESET_ALL}")
        return

    typer.echo(f"{Fore.GREEN}Process completed successfully.{Style.RESET_ALL}")


if __name__ == "__main__":
    app()
