import requests


class TextToSpeech:
    API_URL = "http://v2.nutq.uz/api/v1/cabinet/gen/?text="
    PATH_TO_AUDIO = "audios/"
    COUNTER = 0

    def to_speech(self, text):
        text = text.replace(" ", "%20")
        response = requests.get(self.API_URL + text)
        try:
            with open(self.PATH_TO_AUDIO + f'audio{self.COUNTER}.mp3', "wb") as f:
                f.write(response.content)
            self.COUNTER += 1
            return self.PATH_TO_AUDIO + f'audio{self.COUNTER - 1}.mp3'
        except:
            print("Network error!")

# Usage:
# tts = TextToSpeech()
# tts.to_speech("Salom Dunyo!")
