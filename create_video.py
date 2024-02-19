import os

from moviepy.config import change_settings
from moviepy.editor import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    concatenate_videoclips,
    vfx,
)
from moviepy.video.tools.subtitles import SubtitlesClip

imagemagick_binary_path = os.getenv("IMAGEMAGICK_BINARY_PATH")


class VideoCreator:
    def __init__(self, srt_path: str, audio_path: str, directory: str = "data"):
        self.directory = directory
        self.srt_path = srt_path
        self.audio_path = audio_path
        imagemagick_binary = os.getenv("IMAGEMAGICK_BINARY", "usr/bin/convert")
        if imagemagick_binary:
            change_settings({"IMAGEMAGICK_BINARY": imagemagick_binary})
        else:
            raise EnvironmentError(
                "The IMAGEMAGICK_BINARY environment variable is not set."
            )

    def create_video(self, output_path: str = "output_video.mp4") -> None:
        audio_clip = AudioFileClip(self.audio_path)
        audio_duration = audio_clip.duration
        image_files = [
            os.path.join(self.directory, f)
            for f in os.listdir(self.directory)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
        ]

        if not image_files:
            raise FileNotFoundError(
                "No images available for Fact. Please add images to the directory and try again."
            )

        image_clips = [
            self._create_image_clip(image_file, audio_duration / len(image_files))
            for image_file in image_files
        ]
        final_clip = concatenate_videoclips(image_clips)

        subtitles = self._create_subtitles(final_clip)
        video = CompositeVideoClip([final_clip, subtitles]).set_duration(audio_duration)

        video = video.set_audio(audio_clip)
        video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
        )

    def _create_image_clip(self, image_path: str, duration: float) -> ImageClip:
        clip = ImageClip(image_path)
        zoom_clip = clip.fx(
            vfx.resize, newsize=lambda t: self._zoom_effect(t, duration)
        )
        return zoom_clip.set_duration(duration).crop(
            x_center=zoom_clip.w / 2, y_center=zoom_clip.h / 2, width=1080, height=1920
        )

    def _zoom_effect(self, t: float, duration: float) -> float:
        zoom_peak = duration / 2
        zoom_strength = 0.03
        if t <= zoom_peak:
            return 1 + zoom_strength * (t / zoom_peak)
        else:
            return 1 + zoom_strength * (1 - (t - zoom_peak) / (duration / 2))

    def _create_subtitles(self, clip: ImageClip) -> SubtitlesClip:
        generator = lambda txt: TextClip(
            txt,
            font="Arial-Bold",
            fontsize=80,
            color="yellow",
            stroke_color="black",
            stroke_width=4,
            align="center",
            size=(clip.w, None),
            method="caption",
        )
        return SubtitlesClip(self.srt_path, generator).set_position(
            ("center", 0.45 * clip.h)
        )
