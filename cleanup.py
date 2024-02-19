import os
import shutil


def clean():
    files_to_remove = ["output_video.mp4", "transcript.srt", "audio.mp3"]
    directory_to_remove = "data"

    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"{file} has been removed.")

    if os.path.exists(directory_to_remove) and os.path.isdir(directory_to_remove):
        shutil.rmtree(directory_to_remove)
        print(f"Directory {directory_to_remove} has been removed.")
