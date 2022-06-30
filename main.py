from imutils.video import VideoStream
from utils.voice import VoiceEmitter
from utils.horoscope import HoroscopeParser
import face_recognition
import logging
import imutils
import pickle
import json
import time
import sys
import os

SETTINGS_PATH = 'settings.json'


class StreamWorker:
    def __init__(self, settings_path):
        logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout),
                                      logging.FileHandler(filename="VideoStream.log", encoding='utf-8', mode='a+')],
                            format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                            datefmt="%m/%d/%Y %I:%M:%S",
                            level=logging.INFO)
        logging.info('Began initialization')

        with open(settings_path, encoding="utf-8") as json_file:
            settings = json.load(json_file)
        self.__timeout = settings['timeout']
        self._shutdown_message = settings['shutdown_message']
        self._stream_error_message = settings['stream_error_message']
        logging.info('Settings read')

        with open(settings['encodings_path'], "rb") as file:
            self.__data = pickle.loads(file.read())
        logging.info('Encodings read')

        self.__parser = HoroscopeParser(settings['horoscope_channel'], settings['horoscope_error_message'],
                                        settings['tg_api_id'], settings['tg_api_hash'])
        logging.info('Api requesting configured')

        self.__emitter = VoiceEmitter(settings['greetings_list'], settings['unknown_name'],
                                      settings['replace_symbol'], settings['prophecies_list'])
        self.__emitter.play_message(settings['startup_message'])
        logging.info('Text-to-speech initialized')

        src = 0
        if os.name == 'nt':
            src = 0
        self.__vs = VideoStream(src=src).start()
        logging.info('Video stream capture started')

    def process_frame(self, frame):
        boxes = face_recognition.face_locations(frame)
        encodings = face_recognition.face_encodings(frame, boxes)
        if boxes is not None and len(boxes) != 0:
            logging.info(f'got {len(boxes)} faces')
        for encoding in encodings:
            matches = face_recognition.compare_faces(self.__data["encodings"], encoding)
            if True in matches:
                matched = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matched:
                    name = self.__data["names"][i]
                    counts[tuple(name)] = counts.get(tuple(name), 0) + 1
                name = max(counts, key=counts.get)
                self.__emitter.play_greeting(name[0])
                logging.info(f'recognized {name[0]}')
                self.__emitter.play_message(self.__parser.request_horoscope(name[1]))
            else:
                self.__emitter.play_greeting(None)
                logging.info('Unknown person appeared')

    def process_stream(self):
        time.sleep(2.0)
        logging.info('Began face recognition loop')
        while True:
            try:
                frame = self.__vs.read()
                self.process_frame(imutils.resize(frame, width=500))
                time.sleep(self.__timeout)
            except KeyboardInterrupt:
                self.__emitter.play_message(self._shutdown_message)
                logging.info('Stopped face recognition loop')
                break
            except Exception as ex:
                self.__emitter.play_message(self._stream_error_message)
                logging.error(f'Exception happened during face recognition loop: {ex}')
                break


if __name__ == "__main__":
    butler = StreamWorker(SETTINGS_PATH)
    butler.process_stream()
