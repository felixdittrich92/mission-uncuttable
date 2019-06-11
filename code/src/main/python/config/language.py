from lxml import objectify
from lxml import etree
from .resources import Resources

class Language:
    current = None
    __de = None
    languages = []
    def __init__(self, language=None):
        for name, path in dict(Resources.strings).items():
            Language.languages.append(name)
            setattr(Language, name, objectify.fromstring(etree.tostring(etree.parse(path))))
            setattr(Language, "__" + name, etree.parse(path).getroot())
        if language is None:
            language = "de"
            print("No language")

        Language.current = getattr(Language, language)
        Language.__current = getattr(Language, "__" + language)

    def sub(text):
        sub = Language.__current.findtext(text)
        if sub is None:
            return text
        else:
            return sub

    def set_language(lang):
        if Language.hasattr(lang) and lang in Language.languages:
            Language.current = getattr(Language, lang)
