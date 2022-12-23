import requests


class TextToSpeech:
	API_URL = ""
	PATH_TO_AUDIO = ""
	COUNTER = 0

	def __init__(self,):
		self.API_URL = "http://v2.nutq.uz/api/v1/cabinet/gen/?text="
		self.PATH_TO_AUDIO = "audios/"

	def to_speech(self, text):
		text = text.replace(" ", "%20")
		response = requests.get(self.API_URL + text)
		try:
			with open(self.PATH_TO_AUDIO + f'audio{self.COUNTER}.mp3', "wb") as f:
				f.write(response.content)
			self.COUNTER += 1
			return True
		except:
			print("Error has occured!")
			return False

# Usage:
# tts = TextToSpeech()
# tts.to_speech("Salom Dunyo!")