# Whisper Script

## About
this is a script to setup a local Whisper model on your device.

there are two modes for this script:
- transcribe
- translate (Chinese to English)

when executing, it will prompt you to choose the mode you wish to run

> more about Whisper: https://github.com/openai/whisper

## Requirements
- Homebrew(checkout: https://brew.sh/)
- Python
```
brew install python
````
- FFmpeg
```
brew install ffmpeg
```
- Whisper
```
pip3 install openai-whisper
```
- tabulate
```
pip3 install tabulate
```

## Running the code
once the above requirements are install and set up, run the following command
```
python3 main.py {path/to/your/file} 
```

and enjoy!



