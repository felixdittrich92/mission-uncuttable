from lxml import objectify, etree
from .resources import Resources


class Language:
    current = None
    languages = []

    def __init__(self, language=None):
        for name, path in dict(Resources.strings).items():
            Language.languages.append(name)
            setattr(Language, name, objectify.fromstring(etree.tostring(etree.parse(path))))
        if language is None:
            language = "de"
            print("No language")

        Language.current = getattr(Language, language)

    @staticmethod
    def set_language(lang):
        if Language.hasattr(lang) and lang in Language.languages:
            Language.current = getattr(Language, lang)
