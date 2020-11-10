# speech recognition
import speech_recognition
from wit import Wit

# audio manipulation
from pydub import AudioSegment
import pyaudio
import wave

# Standard Library
import os
import sys
import random

# logging
import logging


class Bot:
    def __init__(
        self,
        output_device_index=None,
        input_device_index=None,
        adjust_for_ambient_noise=False,
        language="en-US",
        wit_access_token=None,  # required
        confidence_treshold=0.90,
        names=None,  # required
    ):
        self.stop_listening = None
        self.language = language
        self.confidence_treshold = confidence_treshold
        self.output_device_index = output_device_index
        self.recognizer = speech_recognition.Recognizer()
        logging.info("Initialized recogninzer")

        if wit_access_token is None:
            raise ValueError("Wit.ai access token is needed for bot to operate")
        else:
            self.client = Wit(wit_access_token)

        if names is None:
            raise ValueError("You have to provide comma separated list of names")
        else:
            try:
                self.names = names.split(",")
            except ValueError as e:
                logging.error(e)
                raise ValueError("You have to provide comma separated list of names")

        if output_device_index:
            self.microphone = speech_recognition.Microphone(
                device_index=input_device_index
            )
        else:
            self.microphone = speech_recognition.Microphone()
        logging.info("Initialized microphone")

        if adjust_for_ambient_noise == True:
            # we only need to calibrate once, before we start listening
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)

    # function to convert all files to .wav format
    def preprocess_files(self, keep_files=True):
        logging.info("Preprocessing files")
        responses = os.listdir("resources/responses")
        responses.remove(".gitkeep")  # ignore .gitkeep file
        for response in responses:
            logging.info(f"Processing {response}")
            files = os.listdir(f"resources/responses/{response}")
            for file in files:
                file_extension = file.split(".")[-1]

                # don't convert wav files
                if file_extension != "wav":
                    logging.debug(f"Processing {file} in {response}")
                    audio = AudioSegment.from_file(
                        f"resources/responses/{response}/{file}", file_extension
                    )
                    audio.export(
                        f"resources/responses/{response}/{file[:-len(file_extension)]}wav",
                        format="wav",
                    )

                    # remove converted files
                    if keep_files == False:
                        os.remove(f"resources/responses/{response}/{file}")
                else:
                    logging.debug(f"File {file} is already .wav, not processing")

    # start listening in the background
    def start(self):
        # `stop_listening` is now a function that, when called, stops background listening
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, self._listener_callback
        )
        logging.info("Successfully started bot")

    # stops listening in background but does not exit the bot
    def stop(self):
        if self.stop_listening != None:
            self.stop_listening()
            logging.info("Bot has been stopped")
        else:
            logging.info("Looks like bot wasn't started, so we are not stopping it")

    # plays random response from .wav file in resources/responses/{response}
    def play_response(self, directory):
        CHUNK = 1024

        files = os.listdir(f"resources/responses/{directory}")

        # select random .wav file from directory
        wf = wave.open(f"resources/responses/{directory}/{random.choice(files)}", "rb")

        # instantiate PyAudio
        paudio = pyaudio.PyAudio()

        # open stream
        stream = paudio.open(
            format=paudio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            input_device_index=self.output_device_index,
            output=True,
        )

        # read data
        data = wf.readframes(CHUNK)

        # play stream
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)

        # close stream
        stream.stop_stream()
        stream.close()
        paudio.terminate()

    # callback for audio listening
    def _listener_callback(self, recognizer, audio):
        logging.info("Processing audio")

        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            recognized_text = recognizer.recognize_google(audio, language=self.language)

            # wit.ai json response
            wit_response = self.client.message(recognized_text)

            # check if we have text in response
            # if not then something probably broke
            if wit_response["text"]:
                # check if wit.ai detected something
                if len(wit_response["intents"]) <= 0:
                    # no intent was detected, unrecognized text is saved to .txt file
                    logging.warning(
                        "Couldn't detect intent in the message, saving the unrecognized text"
                    )
                    with open("unrecognized-text.txt", "a", encoding="utf-8") as file:
                        file.write(f"{wit_response['text']}\n")
                        file.close()
                else:

                    # first intent from the response
                    wit_intent = wit_response["intents"][0]

                    # wit.ai entities detected in response
                    wit_entities = wit_response["entities"]
                    logging.debug(f"Found possible intent: {str(wit_intent)}")

                    # check if we are confident enough to continue
                    if wit_intent["confidence"] < self.confidence_treshold:
                        logging.info(
                            f"Ignoring response as it does not meets the specified treshold {wit_intent['confidence']} < {self.confidence_treshold} "
                        )
                    else:
                        # this if statement to check for intent
                        # and play correct response
                        if (
                            wit_intent["name"] == "presence_check"
                            or wit_intent["name"] == "question_asked"
                        ):
                            # check if wit_entities is not an empty dict
                            if wit_entities != {}:
                                wit_contacts = wit_entities["wit$contact:contact"]
                                # code below we check if the text contains the users name
                                # if not then we simply ignore it
                                if len(wit_contacts) > 0:
                                    for entity in wit_contacts:
                                        # check if detected entity is in names array
                                        if entity["body"] in self.names:
                                            if (
                                                entity["confidence"]
                                                < self.confidence_treshold
                                            ):
                                                logging.info(
                                                    f"Ignoring intent as it does not meets specified treshold {wit_intent['confidence']} < {self.confidence_treshold} "
                                                )
                                            else:
                                                # finally after all checks pass play response from .wav file
                                                # in the resources directory
                                                logging.info(
                                                    "Found intent that meets our criteria, playing response"
                                                )
                                                self.play_response(wit_intent["name"])
                                        else:
                                            logging.info(
                                                "Didn't find user name in response, ignoring"
                                            )
                            else:
                                logging.info(
                                    "Response does not contain any contacts, ignoring"
                                )
                        else:
                            logging.warning(
                                f"This intent is not supported as of now, check back later. Intent name: {wit_intent['name']}"
                            )
            else:
                logging.info("Wit.ai response had no text, ignoring")

        except speech_recognition.UnknownValueError:
            logging.warning("Google Speech Recognition could not understand audio")
        except speech_recognition.RequestError as e:
            logging.error(
                f"Could not request results from Google Speech Recognition service; {e}"
            )
