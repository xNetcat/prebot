# prebot

Bot that can respond to someone asking if you are present in the class.
It's not that advanced so please use with caution

## Requirements

### Python

* Only python3 is supported

### Virtual audio cable

* [VB-Cable](https://vb-audio.com/Cable/)
* [Virtual Audio Cable (Vac)](https://vac.muzychenko.net/en/)
* or any other program that forwards audio from input to output

### Python libraries

* `wave`
* `speech_recognition`
* `wit`
* `pydub`
* `pyaudio`

### Audio files

For bot to operate you have to record yourself and put it in the data folder. For example `hello.mp3` file should be placed in `data/responses/presence_check/hello.mp3`

Audio files should be in .wav format but if you don't know how to convert them make sure that option `PREPROCESS_FILES` is set to `yes` in config file

## How to run the bot

After providing configuration just execute `python main.py`

## Installation

### Downloading and installing requirements

1. Download and unpack the bot from [here](https://github.com/xNetcat/teams-bot/archive/main.zip) or git clone the repo
2. `pip3 install -r requirements.txt`
3. if you have troubles installing pyaudio check next section

### Pyaudio installation

#### Windows

1. check your python version with `python -V`
2. Download the wheel on this site <https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio>
3. Choose version that matches your python version for example I use python 3.9 so I will select `PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`
4. Choose `PyAudio‑0.2.11‑cp39‑cp39‑win32.whl` if you use 32 bit, or `PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl` for 64 bit
5. Then go to your downloads folder
6. And install it with pip

* For 64 bit `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`
* For 32 bit `pip install PyAudio‑0.2.11‑cp39‑cp39‑win32.whl`

#### Linux

1. `sudo apt-get install python3-pyaudio`

## Configuration

To configure the bot you have to create config.ini file. If you don't know how you can take a look at [example.config.ini](https://github.com/xNetcat/prebot/blob/main/example.config.ini)

### WIT.AI

* ACCESS_TOKEN - Go to your Wit.ai app Management > Settings and obtain the Client Access Token
* CONFIDENCE_TRESHOLD - The higher you set your Confidence Threshold, the more accurate that Predict’s labeling will be. For example, a threshold of `0.05 is equal to a 95%` confidence threshold.

### SPEECH_RECOGNITION

* INPUT_DEVICE_INDEX - Is an integer that represents an Virtual audio cable speakers. If `device_index` is unspecified, the default microphone is used as the audio source
* OUTPUT_DEVICE_INDEX - Is an integer that represents an Virtual audio cable microphone. If `device_index` is unspecified, the default microphone is used as the audio source
* ADJUST_FOR_AMBIENT_NOISE - Intended to calibrate the energy threshold with the ambient energy level
* LANGUAGE - The recognition language is determined by language, an RFC5646 language tag like `en-US` or `en-GB`
* NAMES - List of names that people call you

### OTHER

* DEBUG - Enables debugging options
* NEVER_PREPROCESS_FILES - Convert files from data/responses to `.wav` format. Works with most of the commonly used formats
* KEEP_PROCESSED_FILES - Don't delete files after preprocessing

## Wit.ai training

1. Go to [Wit.ai](https://wit.ai/).
2. Create a new Wit.ai app:
    1. Enter a name e.g. _Lessons_
    2. Select **Your language**
    3. Select **Open** or **Private** for visibility
    4. Click **Create**.
3. Add an utterance:
    1. Make sure you are on the **Train Your App** page by selecting **Understanding** from the left-hand menu.
    2. Type _Are you here Elon?_ into the **Utterance** text box.
    3. Label an entity in the utterance by highlighting _Elon_ with your mouse and select `wit/contact` as the Entity type.
4. Add an intent
    1. Click on the **Intent** dropdown.
    2. Enter _presence_check_ as the name of your new Intent.
    3. Click **Create Intent**.
5. Submit your first utterance by clicking **Train and Validate**. The training should start within a few seconds - you can see the training status in the top right.

![Training gif](https://raw.githubusercontent.com/xNetcat/prebot/main/docs/wit_training.gif)

Replace _Elon_ with _your name_
