from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI


class OpenAITranscriptGenerator:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.client = OpenAI()
        self.speech_file_path = Path(__file__).parent / "audio.mp3"
        self.transcript_filename = "transcript.srt"

    def process_request(self, animal: str) -> None:
        facts = self._fetch_facts(animal)
        self._create_audio(facts)
        self._generate_transcript()
        print(f"Transcript saved to {self.transcript_filename}")

    def _fetch_facts(self, animal: str) -> str:
        turbo_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert about the topic a user wants to know information about. Provide 5 absolutetly UNKNOWN facts about the specific fact requested by the user. 
                    Facts that may totally blow the users mind!
                    If the user requests: Please tell me about, start your facts with something like "Elephants are amazing animals. You probably don´t know these facts.
                    Number the facts for clarity. Keep the answer short, maximum 10 words. For example: First - Elephants enjoy listening to music. 
                    Second - Elephants from Africa have larger ears than from india. 
                    Its important use enumeration like first, second, third and son on.
                    At the end say "If you enjoyed this video, dont forget to like and subscribe"
                    """,
                },
                {"role": "user", "content": f"Please tell me about: {animal}."},
            ],
        )
        return turbo_response.choices[0].message.content

    def _create_audio(self, text: str) -> None:
        response = self.client.audio.speech.create(
            model="tts-1", voice="nova", input=text
        )
        # Note: Handle stream_to_file issue if still exists
        response.stream_to_file(str(self.speech_file_path))

    def _generate_transcript(self) -> None:
        with open(self.speech_file_path, "rb") as audio_file:
            transcript_response = self.client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="srt"
            )
            transcript_text = transcript_response.rstrip("\n")
            with open(self.transcript_filename, "w") as file:
                file.write(transcript_text)
            self._append_additional_line(transcript_text)

    def _append_additional_line(self, transcript_text: str) -> None:
        last_block = transcript_text.strip().split("\n\n")[-1]
        last_index = int(last_block.split("\n")[0])
        new_index = last_index + 1
        time_stamp = last_block.split("\n")[1]
        additional_line = f"\n\n{new_index}\n{time_stamp}\n"
        with open(self.transcript_filename, "a") as file:
            file.write(additional_line)
