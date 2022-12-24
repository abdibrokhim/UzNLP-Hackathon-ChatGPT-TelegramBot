import os
import json
from deep_translator import GoogleTranslator



#pip install deep_translator


translator = GoogleTranslator(source='auto', target='en')


print(translator.translate("Bizning darsimizga xush kelibsiz!"))