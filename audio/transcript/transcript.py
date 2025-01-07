
from dotenv import load_dotenv
import os
import argparse


import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part

# Setup YOUR PROJECT_ID
# 

def generate_transcript(model: GenerativeModel,  bucket_name: str, audio_blob: str, prompt: str):

    audio_file_uri = "gs://" + bucket_name + "/" + audio_blob
    audio_file = Part.from_uri(audio_file_uri, mime_type="audio/mpeg")

    contents = [audio_file, prompt]

    response = model.generate_content(contents, generation_config=GenerationConfig(audio_timestamp=True))

    return response.text

def main():

    audio_blob = None
    transcript_file = "transcript.txt"

    load_dotenv()

    bucket_name = os.environ['GC_BUCKET_NAME']
    project_id = os.environ['GC_PROJECT_ID']

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    prompt = """
    Can you transcribe this interview, in the format of timecode, speaker, caption.
    Use speaker A, speaker B, etc. to identify speakers.
    """

    parser = argparse.ArgumentParser(description="Transcribe an audio file using a generative model")

    parser.add_argument("--blob", help="Audio Blob name")
    parser.add_argument("--tf", help="Local text file to transcribe")

    args = parser.parse_args()
    
    if args.blob:
        audio_blob = args.blob

    if args.tf:
        transcript_file = args.tf

#    audio_blob = "gl-001500-002000.mp3"
    if (audio_blob):
        print(f"Transcribing {audio_blob}...")
        transcript = generate_transcript(model, bucket_name, audio_blob, prompt)
        print(transcript)

        try:
            with open(transcript_file, "w", encoding="utf-8") as file:
                file.write(transcript)
                print(f"Transcript written to {transcript_file}")

        except Exception as e:
            print(f"An error occurred during transcription: {e}")

if __name__ == "__main__":

    main()


