
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
    transcript_file = None
    output_flag = False

    load_dotenv()

    bucket_name = os.environ['GC_BUCKET_NAME']
    project_id = os.environ['GC_PROJECT_ID']

    vertexai.init(project=project_id, location="us-central1")

#    model = GenerativeModel("gemini-1.5-flash-002")
    model = GenerativeModel("gemini-2.0-flash-exp")

    prompt_en = """
    Can you transcribe this interview, in the format of timecode, speaker, caption.
    Use speaker A, speaker B, etc. to identify speakers.
    """

    prompt_de = """
    Transkribiere dieses Interview im Format von Timecode, Sprecher und Untertitel.
    Verwende Sprecher A, Sprecher B usw., um die Sprecher zu identifizieren.
    """

    parser = argparse.ArgumentParser(description="Transcribe an audio file using a generative model")

    parser.add_argument("--blob", help="Audio Blob name")
    parser.add_argument("--tf", help="Local text file to transcribe")
    parser.add_argument("--of", help="Output to stdio")
    parser.add_argument("--lang", help="Language", default="en")

    args = parser.parse_args()
    
    if args.blob:
        audio_blob = args.blob

    if args.tf:
        transcript_file = args.tf

    if args.of:
        output_flag = (args.of == "true")

    if args.lang == "de":
        prompt = prompt_de
    else:
        prompt = prompt_en

    if (audio_blob):
        print(f"Transcribing {audio_blob}...")
        transcript = generate_transcript(model, bucket_name, audio_blob, prompt)

        if output_flag:
           print(transcript)

        if not transcript_file:
            transcript_file = audio_blob.split(".")[0] +".txt"
            print(f"Writing to {transcript_file}")

        try:
            with open(transcript_file, "w", encoding="utf-8") as file:
                file.write(transcript)
                print(f"Transcript written to {transcript_file}")

        except Exception as e:
            print(f"An error occurred during transcription: {e}")

if __name__ == "__main__":

    main()


