import sys
import os
import whisper
from tabulate import tabulate

modes = ["tiny", "base", "small", "medium", "large", "turbo"]

def format_timestamp(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"

def transcribe_audio(file_path, mode, task):
    if mode not in modes:
        print("Wrong model entered!")
        return -1
    model = whisper.load_model(mode)
    # result = model.transcribe(file_path, word_timestamps=True, task=task)
    if task == "transcribe":
        result = model.transcribe(file_path, word_timestamps=True)
    elif task == "translate":
        # Explicitly set the task to translate and the target language to English
        result = model.transcribe(file_path, word_timestamps=True, task="translate", language="zh", fp16=False)
    
    return result

def organize_transcript(result):
    organized_text = []
    for segment in result['segments']:
        start_time = format_timestamp(segment['start'])
        end_time = format_timestamp(segment['end'])
        text = segment['text'].strip()
        organized_text.append(f"[{start_time} - {end_time}] {text}")
    return "\n\n".join(organized_text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]

    # Create a table for model information
    headers = ["Size", "Parameters", "English-only model", "Multilingual model", "Required VRAM", "Relative speed"]
    data = [
        ["tiny", "39 M", "tiny.en", "tiny", "~1 GB", "~10x"],
        ["base", "74 M", "base.en", "base", "~1 GB", "~7x"],
        ["small", "244 M", "small.en", "small", "~2 GB", "~4x"],
        ["medium", "769 M", "medium.en", "medium", "~5 GB", "~2x"],
        ["large", "1550 M", "N/A", "large", "~10 GB", "1x"],
        ["turbo", "809 M", "N/A", "turbo", "~6 GB", "~8x"]
    ]

    table = tabulate(data, headers=headers, tablefmt="grid")
    
    print("Choose the task:")
    print("1. Transcribe audio")
    print("2. Translate Chinese (traditional/TW) audio to English")
    task_choice = input("Enter your choice (1 or 2): ")
    
    if task_choice == '1':
        task = "transcribe"
        output_suffix = "transcript"
    elif task_choice == '2':
        task = "translate"
        output_suffix = "translation"
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)
    
    print(f"\nWhat is the model you want to run:\n\n{table}\n")
    mode = input("Type in the model size you wish to run (e.g., base): ")
    
    result = transcribe_audio(audio_file, mode, task)
    if result != -1:
        organized_output = organize_transcript(result)
        
        # Generate output file name
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        output_file = f"{base_name}_{output_suffix}.txt"
        
        # Save the output to a file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(organized_output)
        
        print(f"{'Transcript' if task == 'transcribe' else 'Translation'} saved to {output_file}")