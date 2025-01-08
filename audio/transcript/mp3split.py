
import argparse
import math

from mutagen.mp3 import MP3
from pydub import AudioSegment

def get_mp3_info_from_mutagen(audio_file):
    audio = MP3(audio_file)
    minutes = int(audio.info.length / 60)
    seconds = int(audio.info.length % 60)
    print(f"duration: {minutes:03}:{seconds:02}")

def get_mp3_info(audio_file):
    audio = AudioSegment.from_file(audio_file)
    total_duration = len(audio)
    print(f"duration: {total_duration}")

def split_audio(audio_file, segment_duration):
    """Splits an audio file into segments of specified duration.

    Args:
        audio_path: Path to the audio file.
        segment_duration: Duration of each segment in milliseconds.
    """

    file_name = audio_file.split("/")[-1]
    file_name = file_name.split(".")[0]

    try:
        audio = AudioSegment.from_file(audio_file)
        total_duration = len(audio)
        num_segments = math.ceil(total_duration / segment_duration)

        for i in range(num_segments):
            start = i * segment_duration
            end = min((i + 1) * segment_duration, total_duration)
            segment = audio[start:end]
            segment.export(f"{file_name}_{start}_{end}_{i+1}.mp3", format="mp3")

        print("Audio file splitted successfully")

    except Exception as e:
        print(f"Error splitting audio: {e}")


def main():
    
    audio_file = None
    segment_length = 30000

    print("mp3split v0.1.0")

    parser = argparse.ArgumentParser(description="Split an MP3 file in equally sized segments")
    parser.add_argument("--fname", help="File to split")
    parser.add_argument("--sl", help="segment length in minutes")

    args = parser.parse_args()
    
    if args.fname:
        audio_file = args.fname
    if args.sl:
        segment_length = (int(args.sl) * 60 * 1000)

    if audio_file and segment_length:
        split_audio(audio_file, segment_length)


if __name__ == "__main__":
    main()
