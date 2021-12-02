

from googletrans import Translator



def translate_string(text, from_lang, to_lang):
    translator = Translator()
    result = translator.translate(text=text, dest=to_lang, src=from_lang)
    return result.text





print(translate_string('Ботинки для мальчика Uovo', from_lang='ru', to_lang='en'))

