"""
This file enumerates all supported languages.
It is important to only edit this in utf-8, as the names contain many unicode
characters.
"""

__author__ = "Noah Hummel, Hannes Leutloff"


from enum import Enum


babel_languages = {
    "zu": "isiZulu",
    "zh": "中文",
    "zgh": "ⵜⴰⵎⴰⵣⵉⵖⵜ",
    "yue": "粵語",
    "yo": "Èdè Yorùbá",
    "yi": "ייִדיש",
    "yav": "nuasue",
    "xog": "Olusoga",
    "wae": "Walser",
    "vun": "Kyivunjo",
    "vo": "Volapük",
    "vi": "Tiếng Việt",
    "vai": "ꕙꔤ",
    "uz": "o‘zbek",
    "ur": "اردو",
    "uk": "українська",
    "ug": "ئۇيغۇرچە",
    "tzm": "Tamaziɣt n laṭlaṣ",
    "twq": "Tasawaq senni",
    "tr": "Türkçe",
    "to": "lea fakatonga",
    "tk": "türkmençe",
    "ti": "ትግርኛ",
    "th": "ไทย",
    "teo": "Kiteso",
    "te": "తెలుగు",
    "ta": "தமிழ்",
    "sw": "Kiswahili",
    "sv": "svenska",
    "sr": "српски",
    "sq": "shqip",
    "so": "Soomaali",
    "sn": "chiShona",
    "smn": "anarâškielâ",
    "sl": "slovenščina",
    "sk": "slovenčina",
    "si": "සිංහල",
    "shi": "ⵜⴰⵛⵍⵃⵉⵜ",
    "sg": "Sängö",
    "ses": "Koyraboro senni",
    "seh": "sena",
    "se": "davvisámegiella",
    "sbp": "Ishisangu",
    "saq": "Kisampur",
    "sah": "саха тыла",
    "rwk": "Kiruwa",
    "rw": "Kinyarwanda",
    "ru": "русский",
    "rof": "Kihorombo",
    "ro": "română",
    "rn": "Ikirundi",
    "rm": "rumantsch",
    "qu": "Runasimi",
    "pt": "português",
    "ps": "پښتو",
    "prg": "prūsiskan",
    "pl": "polski",
    "pa": "ਪੰਜਾਬੀ",
    "os": "ирон",
    "or": "ଓଡ଼ିଆ",
    "om": "Oromoo",
    "nyn": "Runyankore",
    "nus": "Thok Nath",
    "nnh": "Shwóŋò ngiembɔɔn",
    "nn": "nynorsk",
    "nmg": "Kwasio",
    "nl": "Nederlands",
    "ne": "नेपाली",
    "nd": "isiNdebele",
    "nb": "norsk bokmål",
    "naq": "Khoekhoegowab",
    "mzn": "مازرونی",
    "my": "ဗမာ",
    "mua": "MUNDAŊ",
    "mt": "Malti",
    "ms": "Bahasa Melayu",
    "mr": "मराठी",
    "mn": "монгол",
    "ml": "മലയാളം",
    "mk": "македонски",
    "mgo": "metaʼ",
    "mgh": "Makua",
    "mg": "Malagasy",
    "mfe": "kreol morisien",
    "mer": "Kĩmĩrũ",
    "mas": "Maa",
    "lv": "latviešu",
    "luy": "Luluhia",
    "luo": "Dholuo",
    "lu": "Tshiluba",
    "lt": "lietuvių",
    "lrc": "لۊری شومالی",
    "lo": "ລາວ",
    "ln": "lingála",
    "lkt": "Lakȟólʼiyapi",
    "lg": "Luganda",
    "lb": "Lëtzebuergesch",
    "lag": "Kɨlaangi",
    "ky": "кыргызча",
    "kw": "kernewek",
    "ksh": "Kölsch",
    "ksf": "rikpa",
    "ksb": "Kishambaa",
    "ks": "کٲشُر",
    "kok": "कोंकणी",
    "ko": "한국어",
    "kn": "ಕನ್ನಡ",
    "km": "ខ្មែរ",
    "kln": "Kalenjin",
    "kl": "kalaallisut",
    "kkj": "kakɔ",
    "kk": "қазақ тілі",
    "ki": "Gikuyu",
    "khq": "Koyra ciini",
    "kea": "kabuverdianu",
    "kde": "Chimakonde",
    "kam": "Kikamba",
    "kab": "Taqbaylit",
    "ka": "ქართული",
    "jmc": "Kimachame",
    "jgo": "Ndaꞌa",
    "ja": "日本語",
    "it": "italiano",
    "is": "íslenska",
    "ii": "ꆈꌠꉙ",
    "ig": "Igbo",
    "id": "Indonesia",
    "hy": "հայերեն",
    "hu": "magyar",
    "hsb": "hornjoserbšćina",
    "hr": "hrvatski",
    "hi": "हिन्दी",
    "he": "עברית",
    "haw": "ʻŌlelo Hawaiʻi",
    "ha": "Hausa",
    "gv": "Gaelg",
    "guz": "Ekegusii",
    "gu": "ગુજરાતી",
    "gsw": "Schwiizertüütsch",
    "gl": "galego",
    "gd": "Gàidhlig",
    "ga": "Gaeilge",
    "fy": "West-Frysk",
    "fur": "furlan",
    "fr": "français",
    "fo": "føroyskt",
    "fil": "Filipino",
    "fi": "suomi",
    "ff": "Pulaar",
    "fa": "فارسی",
    "ewo": "ewondo",
    "eu": "euskara",
    "et": "eesti",
    "es": "español",
    "eo": "esperanto",
    "en": "English",
    "el": "Ελληνικά",
    "ee": "Eʋegbe",
    "ebu": "Kĩembu",
    "dz": "རྫོང་ཁ",
    "dyo": "joola",
    "dua": "duálá",
    "dsb": "dolnoserbšćina",
    "dje": "Zarmaciine",
    "de": "Deutsch",
    "dav": "Kitaita",
    "da": "dansk",
    "cy": "Cymraeg",
    "cu": "церковнослове́нскїй",
    "cs": "čeština",
    "ckb": "کوردیی ناوەندی",
    "chr": "ᏣᎳᎩ",
    "cgg": "Rukiga",
    "ce": "нохчийн",
    "ca": "català",
    "bs": "bosanski",
    "brx": "बड़ो",
    "br": "brezhoneg",
    "bo": "བོད་སྐད་",
    "bn": "বাংলা",
    "bm": "bamanakan",
    "bg": "български",
    "bez": "Hibena",
    "bem": "Ichibemba",
    "be": "беларуская",
    "bas": "Ɓàsàa",
    "az": "azərbaycan dili",
    "ast": "asturianu",
    "asa": "Kipare",
    "as": "অসমীয়া",
    "ar": "العربية",
    "am": "አማርኛ",
    "ak": "Akan",
    "agq": "Aghem",
    "af": "Afrikaans"
}

BabelLanguage = Enum(value='BabelLanguage', names=babel_languages)


def is_language(lang):
    return any((lang == i.name for i in BabelLanguage))


def language_exists(short_tag: str) -> bool:
    return short_tag in babel_languages
