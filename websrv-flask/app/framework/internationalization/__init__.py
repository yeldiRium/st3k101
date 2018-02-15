from flask.ext.babel import lazy_gettext


_ = lambda msg: str(lazy_gettext(msg))

HTTP_LANGUAGE_TAGS = {
    "aa": {
        "english": "Afar",
        "native": "Afaraf"
    },
    "aar": {
        "english": "Afar",
        "native": "Afaraf"
    },
    "ab": {
        "english": "Abkhazian",
        "native": "Abkhazian"
    },
    "abk": {
        "english": "Abkhazian",
        "native": "Abkhazian"
    },
    "ace": {
        "english": "Achinese",
        "native": "Achinese"
    },
    "ach": {
        "english": "Acoli",
        "native": "Acoli"
    },
    "ada": {
        "english": "Adangme",
        "native": "Adangme"
    },
    "ady": {
        "english": "Adygei",
        "native": "Adygei"
    },
    "ae": {
        "english": "Avestan",
        "native": "Avesta"
    },
    "af": {
        "english": "Afrikaans",
        "native": "Afrikaans"
    },
    "afa": {
        "english": "Afro-Asiatic Languages",
        "native": "Afro-Asiatic Languages"
    },
    "afh": {
        "english": "Afrihili",
        "native": "Afrihili"
    },
    "afr": {
        "english": "Afrikaans",
        "native": "Afrikaans"
    },
    "ain": {
        "english": "Ainu",
        "native": "Ainu"
    },
    "ak": {
        "english": "Akan",
        "native": "Akan"
    },
    "aka": {
        "english": "Akan",
        "native": "Akan"
    },
    "akk": {
        "english": "Akkadian",
        "native": "Akkadian"
    },
    "alb": {
        "english": "Albanian",
        "native": "Shqip"
    },
    "ale": {
        "english": "Aleut",
        "native": "Aleut"
    },
    "alg": {
        "english": "Algonquian Languages",
        "native": "Algonquian Languages"
    },
    "alt": {
        "english": "Southern Altai",
        "native": "Southern Altai"
    },
    "am": {
        "english": "Amharic",
        "native": "\u12a0\u121b\u122d\u129b"
    },
    "amh": {
        "english": "Amharic",
        "native": "\u12a0\u121b\u122d\u129b"
    },
    "an": {
        "english": "Aragonese",
        "native": "Aragon\u00e9s"
    },
    "ang": {
        "english": "English Old (ca.450-1100)",
        "native": "English Old (ca.450-1100)"
    },
    "anp": {
        "english": "Angika",
        "native": "Angika"
    },
    "apa": {
        "english": "Apache Languages",
        "native": "Apache Languages"
    },
    "ar": {
        "english": "Arabic",
        "native": "\u0627\u0644\u0639\u0631\u0628\u064a\u0629"
    },
    "ara": {
        "english": "Arabic",
        "native": "\u0627\u0644\u0639\u0631\u0628\u064a\u0629"
    },
    "arc": {
        "english": "Imperial Aramaic (700-300 BCE)",
        "native": "Imperial Aramaic (700-300 BCE)"
    },
    "arg": {
        "english": "Aragonese",
        "native": "Aragon\u00e9s"
    },
    "arm": {
        "english": "Armenian",
        "native": "\u0540\u0561\u0575\u0565\u0580\u0565\u0576"
    },
    "arn": {
        "english": "Mapuche",
        "native": "Mapuche"
    },
    "arp": {
        "english": "Arapaho",
        "native": "Arapaho"
    },
    "art": {
        "english": "Artificial Languages",
        "native": "Artificial Languages"
    },
    "arw": {
        "english": "Arawak",
        "native": "Arawak"
    },
    "as": {
        "english": "Assamese",
        "native": "\u0985\u09b8\u09ae\u09c0\u09af\u09bc\u09be"
    },
    "asm": {
        "english": "Assamese",
        "native": "\u0985\u09b8\u09ae\u09c0\u09af\u09bc\u09be"
    },
    "ast": {
        "english": "Asturian",
        "native": "Asturian"
    },
    "ath": {
        "english": "Athapascan Languages",
        "native": "Athapascan Languages"
    },
    "aus": {
        "english": "Australian Languages",
        "native": "Australian Languages"
    },
    "av": {
        "english": "Avaric",
        "native": "\u0430\u0432\u0430\u0440 \u043c\u0430\u0446\u04c0"
    },
    "ava": {
        "english": "Avaric",
        "native": "\u0430\u0432\u0430\u0440 \u043c\u0430\u0446\u04c0"
    },
    "ave": {
        "english": "Avestan",
        "native": "Avesta"
    },
    "awa": {
        "english": "Awadhi",
        "native": "Awadhi"
    },
    "ay": {
        "english": "Aymara",
        "native": "Aymar Aru"
    },
    "aym": {
        "english": "Aymara",
        "native": "Aymar Aru"
    },
    "az": {
        "english": "Azerbaijani",
        "native": "Az\u0259rbaycan Dili"
    },
    "aze": {
        "english": "Azerbaijani",
        "native": "Az\u0259rbaycan Dili"
    },
    "ba": {
        "english": "Bashkir",
        "native": "\u0431\u0430\u0448\u04a1\u043e\u0440\u0442 \u0442\u0435\u043b\u0435"
    },
    "bad": {
        "english": "Banda Languages",
        "native": "Banda Languages"
    },
    "bai": {
        "english": "Bamileke Languages",
        "native": "Bamileke Languages"
    },
    "bak": {
        "english": "Bashkir",
        "native": "\u0431\u0430\u0448\u04a1\u043e\u0440\u0442 \u0442\u0435\u043b\u0435"
    },
    "bal": {
        "english": "Baluchi",
        "native": "Baluchi"
    },
    "bam": {
        "english": "Bambara",
        "native": "Bamanankan"
    },
    "ban": {
        "english": "Balinese",
        "native": "Balinese"
    },
    "baq": {
        "english": "Basque",
        "native": "Euskara"
    },
    "bas": {
        "english": "Basa",
        "native": "Basa"
    },
    "bat": {
        "english": "Baltic Languages",
        "native": "Baltic Languages"
    },
    "be": {
        "english": "Belarusian",
        "native": "\u0411\u0435\u043b\u0430\u0440\u0443\u0441\u043a\u0430\u044f"
    },
    "bej": {
        "english": "Bedawiyet",
        "native": "Bedawiyet"
    },
    "bel": {
        "english": "Belarusian",
        "native": "\u0411\u0435\u043b\u0430\u0440\u0443\u0441\u043a\u0430\u044f"
    },
    "bem": {
        "english": "Bemba",
        "native": "Bemba"
    },
    "ben": {
        "english": "Bengali",
        "native": "\u09ac\u09be\u0982\u09b2\u09be"
    },
    "ber": {
        "english": "Berber Languages",
        "native": "Berber Languages"
    },
    "bg": {
        "english": "Bulgarian",
        "native": "\u0431\u044a\u043b\u0433\u0430\u0440\u0441\u043a\u0438 \u0435\u0437\u0438\u043a"
    },
    "bh": {
        "english": "Bihari Languages",
        "native": "Bihari Languages"
    },
    "bho": {
        "english": "Bhojpuri",
        "native": "Bhojpuri"
    },
    "bi": {
        "english": "Bislama",
        "native": "Bislama"
    },
    "bih": {
        "english": "Bihari Languages",
        "native": "Bihari Languages"
    },
    "bik": {
        "english": "Bikol",
        "native": "Bikol"
    },
    "bin": {
        "english": "Bini",
        "native": "Bini"
    },
    "bis": {
        "english": "Bislama",
        "native": "Bislama"
    },
    "bla": {
        "english": "Siksika",
        "native": "Siksika"
    },
    "bm": {
        "english": "Bambara",
        "native": "Bamanankan"
    },
    "bn": {
        "english": "Bengali",
        "native": "\u09ac\u09be\u0982\u09b2\u09be"
    },
    "bnt": {
        "english": "Bantu (Other)",
        "native": "Bantu (Other)"
    },
    "bo": {
        "english": "Tibetan",
        "native": "Tibetan"
    },
    "bod": {
        "english": "Tibetan",
        "native": "Tibetan"
    },
    "bos": {
        "english": "Bosnian",
        "native": "Bosanski Jezik"
    },
    "br": {
        "english": "Breton",
        "native": "Brezhoneg"
    },
    "bra": {
        "english": "Braj",
        "native": "Braj"
    },
    "bre": {
        "english": "Breton",
        "native": "Brezhoneg"
    },
    "bs": {
        "english": "Bosnian",
        "native": "Bosanski Jezik"
    },
    "btk": {
        "english": "Batak Languages",
        "native": "Batak Languages"
    },
    "bua": {
        "english": "Buriat",
        "native": "Buriat"
    },
    "bug": {
        "english": "Buginese",
        "native": "Buginese"
    },
    "bul": {
        "english": "Bulgarian",
        "native": "\u0431\u044a\u043b\u0433\u0430\u0440\u0441\u043a\u0438 \u0435\u0437\u0438\u043a"
    },
    "bur": {
        "english": "Burmese",
        "native": "\u1017\u1019\u102c\u1005\u102c"
    },
    "byn": {
        "english": "Bilin",
        "native": "Bilin"
    },
    "ca": {
        "english": "Catalan",
        "native": "Catal\u00e0"
    },
    "cad": {
        "english": "Caddo",
        "native": "Caddo"
    },
    "cai": {
        "english": "Central American Indian Languages",
        "native": "Central American Indian Languages"
    },
    "car": {
        "english": "Galibi Carib",
        "native": "Galibi Carib"
    },
    "cat": {
        "english": "Catalan",
        "native": "Catal\u00e0"
    },
    "cau": {
        "english": "Caucasian Languages",
        "native": "Caucasian Languages"
    },
    "ce": {
        "english": "Chechen",
        "native": "\u043d\u043e\u0445\u0447\u0438\u0439\u043d \u043c\u043e\u0442\u0442"
    },
    "ceb": {
        "english": "Cebuano",
        "native": "Cebuano"
    },
    "cel": {
        "english": "Celtic Languages",
        "native": "Celtic Languages"
    },
    "ces": {
        "english": "Czech",
        "native": "\u010desky"
    },
    "ch": {
        "english": "Chamorro",
        "native": "Chamoru"
    },
    "cha": {
        "english": "Chamorro",
        "native": "Chamoru"
    },
    "chb": {
        "english": "Chibcha",
        "native": "Chibcha"
    },
    "che": {
        "english": "Chechen",
        "native": "\u043d\u043e\u0445\u0447\u0438\u0439\u043d \u043c\u043e\u0442\u0442"
    },
    "chg": {
        "english": "Chagatai",
        "native": "Chagatai"
    },
    "chi": {
        "english": "Chinese",
        "native": "\u4e2d\u6587 (Zh\u014dngw\u00e9n)"
    },
    "chk": {
        "english": "Chuukese",
        "native": "Chuukese"
    },
    "chm": {
        "english": "Mari",
        "native": "Mari"
    },
    "chn": {
        "english": "Chinook Jargon",
        "native": "Chinook Jargon"
    },
    "cho": {
        "english": "Choctaw",
        "native": "Choctaw"
    },
    "chp": {
        "english": "Chipewyan",
        "native": "Chipewyan"
    },
    "chr": {
        "english": "Cherokee",
        "native": "Cherokee"
    },
    "chu": {
        "english": "Church Slavic",
        "native": "Church Slavic"
    },
    "chv": {
        "english": "Chuvash",
        "native": "\u0447\u04d1\u0432\u0430\u0448 \u0447\u04d7\u043b\u0445\u0438"
    },
    "chy": {
        "english": "Cheyenne",
        "native": "Cheyenne"
    },
    "cmc": {
        "english": "Chamic Languages",
        "native": "Chamic Languages"
    },
    "co": {
        "english": "Corsican",
        "native": "Corsu"
    },
    "cop": {
        "english": "Coptic",
        "native": "Coptic"
    },
    "cor": {
        "english": "Cornish",
        "native": "Kernewek"
    },
    "cos": {
        "english": "Corsican",
        "native": "Corsu"
    },
    "cpe": {
        "english": "Creoles And Pidgins",
        "native": "Creoles And Pidgins"
    },
    "cpf": {
        "english": "Creoles And Pidgins",
        "native": "Creoles And Pidgins"
    },
    "cpp": {
        "english": "Creoles And Pidgins",
        "native": "Creoles And Pidgins"
    },
    "cr": {
        "english": "Cree",
        "native": "\u14c0\u1426\u1403\u152d\u140d\u140f\u1423"
    },
    "cre": {
        "english": "Cree",
        "native": "\u14c0\u1426\u1403\u152d\u140d\u140f\u1423"
    },
    "crh": {
        "english": "Crimean Tatar",
        "native": "Crimean Tatar"
    },
    "crp": {
        "english": "Creoles And Pidgins",
        "native": "Creoles And Pidgins"
    },
    "cs": {
        "english": "Czech",
        "native": "\u010desky"
    },
    "csb": {
        "english": "Kashubian",
        "native": "Kashubian"
    },
    "cu": {
        "english": "Church Slavic",
        "native": "Church Slavic"
    },
    "cus": {
        "english": "Cushitic Languages",
        "native": "Cushitic Languages"
    },
    "cv": {
        "english": "Chuvash",
        "native": "\u0447\u04d1\u0432\u0430\u0448 \u0447\u04d7\u043b\u0445\u0438"
    },
    "cy": {
        "english": "Welsh",
        "native": "Cymraeg"
    },
    "cym": {
        "english": "Welsh",
        "native": "Cymraeg"
    },
    "cze": {
        "english": "Czech",
        "native": "\u010desky"
    },
    "da": {
        "english": "Danish",
        "native": "Dansk"
    },
    "dak": {
        "english": "Dakota",
        "native": "Dakota"
    },
    "dan": {
        "english": "Danish",
        "native": "Dansk"
    },
    "dar": {
        "english": "Dargwa",
        "native": "Dargwa"
    },
    "day": {
        "english": "Land Dayak Languages",
        "native": "Land Dayak Languages"
    },
    "de": {
        "english": "German",
        "native": "Deutsch"
    },
    "del": {
        "english": "Delaware",
        "native": "Delaware"
    },
    "den": {
        "english": "Slave (Athapascan)",
        "native": "Slave (Athapascan)"
    },
    "deu": {
        "english": "German",
        "native": "Deutsch"
    },
    "dgr": {
        "english": "Dogrib",
        "native": "Dogrib"
    },
    "din": {
        "english": "Dinka",
        "native": "Dinka"
    },
    "div": {
        "english": "Dhivehi",
        "native": "Dhivehi"
    },
    "doi": {
        "english": "Dogri",
        "native": "Dogri"
    },
    "dra": {
        "english": "Dravidian Languages",
        "native": "Dravidian Languages"
    },
    "dsb": {
        "english": "Lower Sorbian",
        "native": "Lower Sorbian"
    },
    "dua": {
        "english": "Duala",
        "native": "Duala"
    },
    "dum": {
        "english": "Dutch Middle (ca.1050-1350)",
        "native": "Dutch Middle (ca.1050-1350)"
    },
    "dut": {
        "english": "Dutch",
        "native": "Dutch"
    },
    "dv": {
        "english": "Dhivehi",
        "native": "Dhivehi"
    },
    "dyu": {
        "english": "Dyula",
        "native": "Dyula"
    },
    "dz": {
        "english": "Dzongkha",
        "native": "Dzongkha"
    },
    "dzo": {
        "english": "Dzongkha",
        "native": "Dzongkha"
    },
    "ee": {
        "english": "Ewe",
        "native": "E\u028begbe"
    },
    "efi": {
        "english": "Efik",
        "native": "Efik"
    },
    "egy": {
        "english": "Egyptian (Ancient)",
        "native": "Egyptian (Ancient)"
    },
    "eka": {
        "english": "Ekajuk",
        "native": "Ekajuk"
    },
    "el": {
        "english": "Greek Modern (1453-)",
        "native": "Greek Modern (1453-)"
    },
    "ell": {
        "english": "Greek Modern (1453-)",
        "native": "Greek Modern (1453-)"
    },
    "elx": {
        "english": "Elamite",
        "native": "Elamite"
    },
    "en": {
        "english": "English",
        "native": "English"
    },
    "eng": {
        "english": "English",
        "native": "English"
    },
    "enm": {
        "english": "English Middle (1100-1500)",
        "native": "English Middle (1100-1500)"
    },
    "eo": {
        "english": "Esperanto",
        "native": "Esperanto"
    },
    "epo": {
        "english": "Esperanto",
        "native": "Esperanto"
    },
    "es": {
        "english": "Castilian",
        "native": "Castellano"
    },
    "est": {
        "english": "Estonian",
        "native": "Eesti"
    },
    "et": {
        "english": "Estonian",
        "native": "Eesti"
    },
    "eu": {
        "english": "Basque",
        "native": "Euskara"
    },
    "eus": {
        "english": "Basque",
        "native": "Euskara"
    },
    "ewe": {
        "english": "Ewe",
        "native": "E\u028begbe"
    },
    "ewo": {
        "english": "Ewondo",
        "native": "Ewondo"
    },
    "fa": {
        "english": "Persian",
        "native": "\u0641\u0627\u0631\u0633\u06cc"
    },
    "fan": {
        "english": "Fang",
        "native": "Fang"
    },
    "fao": {
        "english": "Faroese",
        "native": "F\u00f8royskt"
    },
    "fas": {
        "english": "Persian",
        "native": "\u0641\u0627\u0631\u0633\u06cc"
    },
    "fat": {
        "english": "Fanti",
        "native": "Fanti"
    },
    "ff": {
        "english": "Fulah",
        "native": "Fulah"
    },
    "fi": {
        "english": "Finnish",
        "native": "Suomen Kieli"
    },
    "fij": {
        "english": "Fijian",
        "native": "Vosa Vakaviti"
    },
    "fil": {
        "english": "Filipino",
        "native": "Filipino"
    },
    "fin": {
        "english": "Finnish",
        "native": "Suomen Kieli"
    },
    "fiu": {
        "english": "Finno-Ugrian Languages",
        "native": "Finno-Ugrian Languages"
    },
    "fj": {
        "english": "Fijian",
        "native": "Vosa Vakaviti"
    },
    "fo": {
        "english": "Faroese",
        "native": "F\u00f8royskt"
    },
    "fon": {
        "english": "Fon",
        "native": "Fon"
    },
    "fr": {
        "english": "French",
        "native": "Fran\u00e7ais"
    },
    "fra": {
        "english": "French",
        "native": "Fran\u00e7ais"
    },
    "fre": {
        "english": "French",
        "native": "Fran\u00e7ais"
    },
    "frm": {
        "english": "French Middle (ca.1400-1600)",
        "native": "French Middle (ca.1400-1600)"
    },
    "fro": {
        "english": "French Old (842-ca.1400)",
        "native": "French Old (842-ca.1400)"
    },
    "frr": {
        "english": "Northern Frisian",
        "native": "Northern Frisian"
    },
    "frs": {
        "english": "Eastern Frisian",
        "native": "Eastern Frisian"
    },
    "fry": {
        "english": "Western Frisian",
        "native": "Frysk"
    },
    "ful": {
        "english": "Fulah",
        "native": "Fulah"
    },
    "fur": {
        "english": "Friulian",
        "native": "Friulian"
    },
    "fy": {
        "english": "Western Frisian",
        "native": "Frysk"
    },
    "ga": {
        "english": "Irish",
        "native": "Gaeilge"
    },
    "gaa": {
        "english": "Ga",
        "native": "Ga"
    },
    "gay": {
        "english": "Gayo",
        "native": "Gayo"
    },
    "gba": {
        "english": "Gbaya",
        "native": "Gbaya"
    },
    "gd": {
        "english": "Gaelic",
        "native": "Gaelic"
    },
    "gem": {
        "english": "Germanic Languages",
        "native": "Germanic Languages"
    },
    "geo": {
        "english": "Georgian",
        "native": "\u10e5\u10d0\u10e0\u10d7\u10e3\u10da\u10d8"
    },
    "ger": {
        "english": "German",
        "native": "Deutsch"
    },
    "gez": {
        "english": "Geez",
        "native": "Geez"
    },
    "gil": {
        "english": "Gilbertese",
        "native": "Gilbertese"
    },
    "gl": {
        "english": "Galician",
        "native": "Galego"
    },
    "gla": {
        "english": "Gaelic",
        "native": "Gaelic"
    },
    "gle": {
        "english": "Irish",
        "native": "Gaeilge"
    },
    "glg": {
        "english": "Galician",
        "native": "Galego"
    },
    "glv": {
        "english": "Manx",
        "native": "Gaelg"
    },
    "gmh": {
        "english": "German Middle High (ca.1050-1500)",
        "native": "German Middle High (ca.1050-1500)"
    },
    "gn": {
        "english": "Guarani",
        "native": "Guarani"
    },
    "goh": {
        "english": "German Old High (ca.750-1050)",
        "native": "German Old High (ca.750-1050)"
    },
    "gon": {
        "english": "Gondi",
        "native": "Gondi"
    },
    "gor": {
        "english": "Gorontalo",
        "native": "Gorontalo"
    },
    "got": {
        "english": "Gothic",
        "native": "Gothic"
    },
    "grb": {
        "english": "Grebo",
        "native": "Grebo"
    },
    "grc": {
        "english": "Greek Ancient (to 1453)",
        "native": "Greek Ancient (to 1453)"
    },
    "gre": {
        "english": "Greek Modern (1453-)",
        "native": "Greek Modern (1453-)"
    },
    "grn": {
        "english": "Guarani",
        "native": "Guarani"
    },
    "gsw": {
        "english": "Alemannic",
        "native": "Alemannic"
    },
    "gu": {
        "english": "Gujarati",
        "native": "\u0a97\u0ac1\u0a9c\u0ab0\u0abe\u0aa4\u0ac0"
    },
    "guj": {
        "english": "Gujarati",
        "native": "\u0a97\u0ac1\u0a9c\u0ab0\u0abe\u0aa4\u0ac0"
    },
    "gv": {
        "english": "Manx",
        "native": "Gaelg"
    },
    "gwi": {
        "english": "Gwich'in",
        "native": "Gwich'in"
    },
    "ha": {
        "english": "Hausa",
        "native": "Hausa"
    },
    "hai": {
        "english": "Haida",
        "native": "Haida"
    },
    "hat": {
        "english": "Haitian",
        "native": "Krey\u00f2l Ayisyen"
    },
    "hau": {
        "english": "Hausa",
        "native": "Hausa"
    },
    "haw": {
        "english": "Hawaiian",
        "native": "Hawaiian"
    },
    "he": {
        "english": "Hebrew",
        "native": "Hebrew"
    },
    "heb": {
        "english": "Hebrew",
        "native": "Hebrew"
    },
    "her": {
        "english": "Herero",
        "native": "Otjiherero"
    },
    "hi": {
        "english": "Hindi",
        "native": "\u0939\u093f\u0902\u0926\u0940"
    },
    "hil": {
        "english": "Hiligaynon",
        "native": "Hiligaynon"
    },
    "him": {
        "english": "Himachali Languages",
        "native": "Himachali Languages"
    },
    "hin": {
        "english": "Hindi",
        "native": "\u0939\u093f\u0902\u0926\u0940"
    },
    "hit": {
        "english": "Hittite",
        "native": "Hittite"
    },
    "hmn": {
        "english": "Hmong",
        "native": "Hmong"
    },
    "hmo": {
        "english": "Hiri Motu",
        "native": "Hiri Motu"
    },
    "ho": {
        "english": "Hiri Motu",
        "native": "Hiri Motu"
    },
    "hr": {
        "english": "Croatian",
        "native": "Hrvatski"
    },
    "hrv": {
        "english": "Croatian",
        "native": "Hrvatski"
    },
    "hsb": {
        "english": "Upper Sorbian",
        "native": "Upper Sorbian"
    },
    "ht": {
        "english": "Haitian",
        "native": "Krey\u00f2l Ayisyen"
    },
    "hu": {
        "english": "Hungarian",
        "native": "Magyar"
    },
    "hun": {
        "english": "Hungarian",
        "native": "Magyar"
    },
    "hup": {
        "english": "Hupa",
        "native": "Hupa"
    },
    "hy": {
        "english": "Armenian",
        "native": "\u0540\u0561\u0575\u0565\u0580\u0565\u0576"
    },
    "hye": {
        "english": "Armenian",
        "native": "\u0540\u0561\u0575\u0565\u0580\u0565\u0576"
    },
    "hz": {
        "english": "Herero",
        "native": "Otjiherero"
    },
    "ia": {
        "english": "Interlingua (International Auxiliary Language Association)",
        "native": "Interlingua (International Auxiliary Language Association)"
    },
    "iba": {
        "english": "Iban",
        "native": "Iban"
    },
    "ibo": {
        "english": "Igbo",
        "native": "As\u1ee5s\u1ee5 Igbo"
    },
    "ice": {
        "english": "Icelandic",
        "native": "\u00cdslenska"
    },
    "id": {
        "english": "Indonesian",
        "native": "Bahasa Indonesia"
    },
    "ido": {
        "english": "Ido",
        "native": "Ido"
    },
    "ie": {
        "english": "Interlingue",
        "native": "Interlingue"
    },
    "ig": {
        "english": "Igbo",
        "native": "As\u1ee5s\u1ee5 Igbo"
    },
    "ii": {
        "english": "Nuosu",
        "native": "Nuosu"
    },
    "iii": {
        "english": "Nuosu",
        "native": "Nuosu"
    },
    "ijo": {
        "english": "Ijo Languages",
        "native": "Ijo Languages"
    },
    "ik": {
        "english": "Inupiaq",
        "native": "I\u00f1upiaq"
    },
    "iku": {
        "english": "Inuktitut",
        "native": "\u1403\u14c4\u1483\u144e\u1450\u1466"
    },
    "ile": {
        "english": "Interlingue",
        "native": "Interlingue"
    },
    "ilo": {
        "english": "Iloko",
        "native": "Iloko"
    },
    "ina": {
        "english": "Interlingua (International Auxiliary Language Association)",
        "native": "Interlingua (International Auxiliary Language Association)"
    },
    "inc": {
        "english": "Indic Languages",
        "native": "Indic Languages"
    },
    "ind": {
        "english": "Indonesian",
        "native": "Bahasa Indonesia"
    },
    "ine": {
        "english": "Indo-European Languages",
        "native": "Indo-European Languages"
    },
    "inh": {
        "english": "Ingush",
        "native": "Ingush"
    },
    "io": {
        "english": "Ido",
        "native": "Ido"
    },
    "ipk": {
        "english": "Inupiaq",
        "native": "I\u00f1upiaq"
    },
    "ira": {
        "english": "Iranian Languages",
        "native": "Iranian Languages"
    },
    "iro": {
        "english": "Iroquoian Languages",
        "native": "Iroquoian Languages"
    },
    "is": {
        "english": "Icelandic",
        "native": "\u00cdslenska"
    },
    "isl": {
        "english": "Icelandic",
        "native": "\u00cdslenska"
    },
    "it": {
        "english": "Italian",
        "native": "Italiano"
    },
    "ita": {
        "english": "Italian",
        "native": "Italiano"
    },
    "iu": {
        "english": "Inuktitut",
        "native": "\u1403\u14c4\u1483\u144e\u1450\u1466"
    },
    "ja": {
        "english": "Japanese",
        "native": "\u65e5\u672c\u8a9e (\u306b\u307b\u3093\u3054\uff0f\u306b\u3063\u307d\u3093\u3054)"
    },
    "jav": {
        "english": "Javanese",
        "native": "Basa Jawa"
    },
    "jbo": {
        "english": "Lojban",
        "native": "Lojban"
    },
    "jpn": {
        "english": "Japanese",
        "native": "\u65e5\u672c\u8a9e (\u306b\u307b\u3093\u3054\uff0f\u306b\u3063\u307d\u3093\u3054)"
    },
    "jpr": {
        "english": "Judeo-Persian",
        "native": "Judeo-Persian"
    },
    "jrb": {
        "english": "Judeo-Arabic",
        "native": "Judeo-Arabic"
    },
    "jv": {
        "english": "Javanese",
        "native": "Basa Jawa"
    },
    "ka": {
        "english": "Georgian",
        "native": "\u10e5\u10d0\u10e0\u10d7\u10e3\u10da\u10d8"
    },
    "kaa": {
        "english": "Kara-Kalpak",
        "native": "Kara-Kalpak"
    },
    "kab": {
        "english": "Kabyle",
        "native": "Kabyle"
    },
    "kac": {
        "english": "Jingpho",
        "native": "Jingpho"
    },
    "kal": {
        "english": "Greenlandic",
        "native": "Greenlandic"
    },
    "kam": {
        "english": "Kamba",
        "native": "Kamba"
    },
    "kan": {
        "english": "Kannada",
        "native": "\u0c95\u0ca8\u0ccd\u0ca8\u0ca1"
    },
    "kar": {
        "english": "Karen Languages",
        "native": "Karen Languages"
    },
    "kas": {
        "english": "Kashmiri",
        "native": "\u0643\u0634\u0645\u064a\u0631\u064a\u200e"
    },
    "kat": {
        "english": "Georgian",
        "native": "\u10e5\u10d0\u10e0\u10d7\u10e3\u10da\u10d8"
    },
    "kau": {
        "english": "Kanuri",
        "native": "Kanuri"
    },
    "kaw": {
        "english": "Kawi",
        "native": "Kawi"
    },
    "kaz": {
        "english": "Kazakh",
        "native": "\u049a\u0430\u0437\u0430\u049b \u0442\u0456\u043b\u0456"
    },
    "kbd": {
        "english": "Kabardian",
        "native": "Kabardian"
    },
    "kg": {
        "english": "Kongo",
        "native": "KiKongo"
    },
    "kha": {
        "english": "Khasi",
        "native": "Khasi"
    },
    "khi": {
        "english": "Khoisan Languages",
        "native": "Khoisan Languages"
    },
    "khm": {
        "english": "Central Khmer",
        "native": "Central Khmer"
    },
    "kho": {
        "english": "Khotanese",
        "native": "Khotanese"
    },
    "ki": {
        "english": "Gikuyu",
        "native": "Gikuyu"
    },
    "kik": {
        "english": "Gikuyu",
        "native": "Gikuyu"
    },
    "kin": {
        "english": "Kinyarwanda",
        "native": "Ikinyarwanda"
    },
    "kir": {
        "english": "Kirghiz",
        "native": "Kirghiz"
    },
    "kj": {
        "english": "Kuanyama",
        "native": "Kuanyama"
    },
    "kk": {
        "english": "Kazakh",
        "native": "\u049a\u0430\u0437\u0430\u049b \u0442\u0456\u043b\u0456"
    },
    "kl": {
        "english": "Greenlandic",
        "native": "Greenlandic"
    },
    "km": {
        "english": "Central Khmer",
        "native": "Central Khmer"
    },
    "kmb": {
        "english": "Kimbundu",
        "native": "Kimbundu"
    },
    "kn": {
        "english": "Kannada",
        "native": "\u0c95\u0ca8\u0ccd\u0ca8\u0ca1"
    },
    "ko": {
        "english": "Korean",
        "native": "\uc870\uc120\ub9d0 (\u671d\u9bae\u8a9e)"
    },
    "kok": {
        "english": "Konkani",
        "native": "Konkani"
    },
    "kom": {
        "english": "Komi",
        "native": "\u043a\u043e\u043c\u0438 \u043a\u044b\u0432"
    },
    "kon": {
        "english": "Kongo",
        "native": "KiKongo"
    },
    "kor": {
        "english": "Korean",
        "native": "\uc870\uc120\ub9d0 (\u671d\u9bae\u8a9e)"
    },
    "kos": {
        "english": "Kosraean",
        "native": "Kosraean"
    },
    "kpe": {
        "english": "Kpelle",
        "native": "Kpelle"
    },
    "kr": {
        "english": "Kanuri",
        "native": "Kanuri"
    },
    "krc": {
        "english": "Karachay-Balkar",
        "native": "Karachay-Balkar"
    },
    "krl": {
        "english": "Karelian",
        "native": "Karelian"
    },
    "kro": {
        "english": "Kru Languages",
        "native": "Kru Languages"
    },
    "kru": {
        "english": "Kurukh",
        "native": "Kurukh"
    },
    "ks": {
        "english": "Kashmiri",
        "native": "\u0643\u0634\u0645\u064a\u0631\u064a\u200e"
    },
    "ku": {
        "english": "Kurdish",
        "native": "Kurd\u00ee"
    },
    "kua": {
        "english": "Kuanyama",
        "native": "Kuanyama"
    },
    "kum": {
        "english": "Kumyk",
        "native": "Kumyk"
    },
    "kur": {
        "english": "Kurdish",
        "native": "Kurd\u00ee"
    },
    "kut": {
        "english": "Kutenai",
        "native": "Kutenai"
    },
    "kv": {
        "english": "Komi",
        "native": "\u043a\u043e\u043c\u0438 \u043a\u044b\u0432"
    },
    "kw": {
        "english": "Cornish",
        "native": "Kernewek"
    },
    "ky": {
        "english": "Kirghiz",
        "native": "Kirghiz"
    },
    "la": {
        "english": "Latin",
        "native": "Latine"
    },
    "lad": {
        "english": "Ladino",
        "native": "Ladino"
    },
    "lah": {
        "english": "Lahnda",
        "native": "Lahnda"
    },
    "lam": {
        "english": "Lamba",
        "native": "Lamba"
    },
    "lao": {
        "english": "Lao",
        "native": "\u0e9e\u0eb2\u0eaa\u0eb2\u0ea5\u0eb2\u0ea7"
    },
    "lat": {
        "english": "Latin",
        "native": "Latine"
    },
    "lav": {
        "english": "Latvian",
        "native": "Latvie\u0161u Valoda"
    },
    "lb": {
        "english": "Letzeburgesch",
        "native": "Letzeburgesch"
    },
    "lez": {
        "english": "Lezghian",
        "native": "Lezghian"
    },
    "lg": {
        "english": "Ganda",
        "native": "Ganda"
    },
    "li": {
        "english": "Limburgan",
        "native": "Limburgan"
    },
    "lim": {
        "english": "Limburgan",
        "native": "Limburgan"
    },
    "lin": {
        "english": "Lingala",
        "native": "Ling\u00e1la"
    },
    "lit": {
        "english": "Lithuanian",
        "native": "Lietuvi\u0173 Kalba"
    },
    "ln": {
        "english": "Lingala",
        "native": "Ling\u00e1la"
    },
    "lo": {
        "english": "Lao",
        "native": "\u0e9e\u0eb2\u0eaa\u0eb2\u0ea5\u0eb2\u0ea7"
    },
    "lol": {
        "english": "Mongo",
        "native": "Mongo"
    },
    "loz": {
        "english": "Lozi",
        "native": "Lozi"
    },
    "lt": {
        "english": "Lithuanian",
        "native": "Lietuvi\u0173 Kalba"
    },
    "ltz": {
        "english": "Letzeburgesch",
        "native": "Letzeburgesch"
    },
    "lu": {
        "english": "Luba-Katanga",
        "native": ""
    },
    "lua": {
        "english": "Luba-Lulua",
        "native": "Luba-Lulua"
    },
    "lub": {
        "english": "Luba-Katanga",
        "native": ""
    },
    "lug": {
        "english": "Ganda",
        "native": "Ganda"
    },
    "lui": {
        "english": "Luiseno",
        "native": "Luiseno"
    },
    "lun": {
        "english": "Lunda",
        "native": "Lunda"
    },
    "luo": {
        "english": "Luo (Kenya And Tanzania)",
        "native": "Luo (Kenya And Tanzania)"
    },
    "lus": {
        "english": "Lushai",
        "native": "Lushai"
    },
    "lv": {
        "english": "Latvian",
        "native": "Latvie\u0161u Valoda"
    },
    "mac": {
        "english": "Macedonian",
        "native": "\u043c\u0430\u043a\u0435\u0434\u043e\u043d\u0441\u043a\u0438 \u0458\u0430\u0437\u0438\u043a"
    },
    "mad": {
        "english": "Madurese",
        "native": "Madurese"
    },
    "mag": {
        "english": "Magahi",
        "native": "Magahi"
    },
    "mah": {
        "english": "Marshallese",
        "native": "Kajin M\u0327aje\u013c"
    },
    "mai": {
        "english": "Maithili",
        "native": "Maithili"
    },
    "mak": {
        "english": "Makasar",
        "native": "Makasar"
    },
    "mal": {
        "english": "Malayalam",
        "native": "\u0d2e\u0d32\u0d2f\u0d3e\u0d33\u0d02"
    },
    "man": {
        "english": "Mandingo",
        "native": "Mandingo"
    },
    "mao": {
        "english": "Maori",
        "native": "Maori"
    },
    "map": {
        "english": "Austronesian Languages",
        "native": "Austronesian Languages"
    },
    "mar": {
        "english": "Marathi",
        "native": "Marathi"
    },
    "mas": {
        "english": "Masai",
        "native": "Masai"
    },
    "may": {
        "english": "Malay",
        "native": "Bahasa Melayu"
    },
    "mdf": {
        "english": "Moksha",
        "native": "Moksha"
    },
    "mdr": {
        "english": "Mandar",
        "native": "Mandar"
    },
    "men": {
        "english": "Mende",
        "native": "Mende"
    },
    "mg": {
        "english": "Malagasy",
        "native": "Malagasy Fiteny"
    },
    "mga": {
        "english": "Irish Middle (900-1200)",
        "native": "Irish Middle (900-1200)"
    },
    "mh": {
        "english": "Marshallese",
        "native": "Kajin M\u0327aje\u013c"
    },
    "mi": {
        "english": "Maori",
        "native": "Maori"
    },
    "mic": {
        "english": "Mi'kmaq",
        "native": "Mi'kmaq"
    },
    "min": {
        "english": "Minangkabau",
        "native": "Minangkabau"
    },
    "mis": {
        "english": "Uncoded Languages",
        "native": "Uncoded Languages"
    },
    "mk": {
        "english": "Macedonian",
        "native": "\u043c\u0430\u043a\u0435\u0434\u043e\u043d\u0441\u043a\u0438 \u0458\u0430\u0437\u0438\u043a"
    },
    "mkd": {
        "english": "Macedonian",
        "native": "\u043c\u0430\u043a\u0435\u0434\u043e\u043d\u0441\u043a\u0438 \u0458\u0430\u0437\u0438\u043a"
    },
    "mkh": {
        "english": "Mon-Khmer Languages",
        "native": "Mon-Khmer Languages"
    },
    "ml": {
        "english": "Malayalam",
        "native": "\u0d2e\u0d32\u0d2f\u0d3e\u0d33\u0d02"
    },
    "mlg": {
        "english": "Malagasy",
        "native": "Malagasy Fiteny"
    },
    "mlt": {
        "english": "Maltese",
        "native": "Malti"
    },
    "mn": {
        "english": "Mongolian",
        "native": "\u043c\u043e\u043d\u0433\u043e\u043b"
    },
    "mnc": {
        "english": "Manchu",
        "native": "Manchu"
    },
    "mni": {
        "english": "Manipuri",
        "native": "Manipuri"
    },
    "mno": {
        "english": "Manobo Languages",
        "native": "Manobo Languages"
    },
    "moh": {
        "english": "Mohawk",
        "native": "Mohawk"
    },
    "mon": {
        "english": "Mongolian",
        "native": "\u043c\u043e\u043d\u0433\u043e\u043b"
    },
    "mos": {
        "english": "Mossi",
        "native": "Mossi"
    },
    "mr": {
        "english": "Marathi",
        "native": "Marathi"
    },
    "mri": {
        "english": "Maori",
        "native": "Maori"
    },
    "ms": {
        "english": "Malay",
        "native": "Bahasa Melayu"
    },
    "msa": {
        "english": "Malay",
        "native": "Bahasa Melayu"
    },
    "mt": {
        "english": "Maltese",
        "native": "Malti"
    },
    "mul": {
        "english": "Multiple Languages",
        "native": "Multiple Languages"
    },
    "mun": {
        "english": "Munda Languages",
        "native": "Munda Languages"
    },
    "mus": {
        "english": "Creek",
        "native": "Creek"
    },
    "mwl": {
        "english": "Mirandese",
        "native": "Mirandese"
    },
    "mwr": {
        "english": "Marwari",
        "native": "Marwari"
    },
    "my": {
        "english": "Burmese",
        "native": "\u1017\u1019\u102c\u1005\u102c"
    },
    "mya": {
        "english": "Burmese",
        "native": "\u1017\u1019\u102c\u1005\u102c"
    },
    "myn": {
        "english": "Mayan Languages",
        "native": "Mayan Languages"
    },
    "myv": {
        "english": "Erzya",
        "native": "Erzya"
    },
    "na": {
        "english": "Nauru",
        "native": "Ekakair\u0169 Naoero"
    },
    "nah": {
        "english": "Nahuatl Languages",
        "native": "Nahuatl Languages"
    },
    "nai": {
        "english": "North American Indian Languages",
        "native": "North American Indian Languages"
    },
    "nap": {
        "english": "Neapolitan",
        "native": "Neapolitan"
    },
    "nau": {
        "english": "Nauru",
        "native": "Ekakair\u0169 Naoero"
    },
    "nav": {
        "english": "Navaho",
        "native": "Navaho"
    },
    "nb": {
        "english": "Bokm\u00e5l",
        "native": "Bokm\u00e5l"
    },
    "nbl": {
        "english": "Ndebele",
        "native": "Ndebele"
    },
    "nd": {
        "english": "Ndebele",
        "native": "Ndebele"
    },
    "nde": {
        "english": "Ndebele",
        "native": "Ndebele"
    },
    "ndo": {
        "english": "Ndonga",
        "native": "Owambo"
    },
    "nds": {
        "english": "Low",
        "native": "Low"
    },
    "ne": {
        "english": "Nepali",
        "native": "\u0928\u0947\u092a\u093e\u0932\u0940"
    },
    "nep": {
        "english": "Nepali",
        "native": "\u0928\u0947\u092a\u093e\u0932\u0940"
    },
    "new": {
        "english": "Nepal Bhasa",
        "native": "Nepal Bhasa"
    },
    "ng": {
        "english": "Ndonga",
        "native": "Owambo"
    },
    "nia": {
        "english": "Nias",
        "native": "Nias"
    },
    "nic": {
        "english": "Niger-Kordofanian Languages",
        "native": "Niger-Kordofanian Languages"
    },
    "niu": {
        "english": "Niuean",
        "native": "Niuean"
    },
    "nl": {
        "english": "Dutch",
        "native": "Dutch"
    },
    "nld": {
        "english": "Dutch",
        "native": "Dutch"
    },
    "nn": {
        "english": "Norwegian",
        "native": "Norwegian"
    },
    "nno": {
        "english": "Norwegian",
        "native": "Norwegian"
    },
    "no": {
        "english": "Norwegian",
        "native": "Norsk"
    },
    "nob": {
        "english": "Bokm\u00e5l",
        "native": "Bokm\u00e5l"
    },
    "nog": {
        "english": "Nogai",
        "native": "Nogai"
    },
    "non": {
        "english": "Norse",
        "native": "Norse"
    },
    "nor": {
        "english": "Norwegian",
        "native": "Norsk"
    },
    "nqo": {
        "english": "N'Ko",
        "native": "N'Ko"
    },
    "nr": {
        "english": "Ndebele",
        "native": "Ndebele"
    },
    "nso": {
        "english": "Northern Sotho",
        "native": "Northern Sotho"
    },
    "nub": {
        "english": "Nubian Languages",
        "native": "Nubian Languages"
    },
    "nv": {
        "english": "Navaho",
        "native": "Navaho"
    },
    "nwc": {
        "english": "Classical Nepal Bhasa",
        "native": "Classical Nepal Bhasa"
    },
    "ny": {
        "english": "Chewa",
        "native": "ChiChe\u0175a"
    },
    "nya": {
        "english": "Chewa",
        "native": "ChiChe\u0175a"
    },
    "nym": {
        "english": "Nyamwezi",
        "native": "Nyamwezi"
    },
    "nyn": {
        "english": "Nyankole",
        "native": "Nyankole"
    },
    "nyo": {
        "english": "Nyoro",
        "native": "Nyoro"
    },
    "nzi": {
        "english": "Nzima",
        "native": "Nzima"
    },
    "oc": {
        "english": "Occitan (post 1500)",
        "native": "Occitan (post 1500)"
    },
    "oci": {
        "english": "Occitan (post 1500)",
        "native": "Occitan (post 1500)"
    },
    "oj": {
        "english": "Ojibwa",
        "native": "Ojibwa"
    },
    "oji": {
        "english": "Ojibwa",
        "native": "Ojibwa"
    },
    "om": {
        "english": "Oromo",
        "native": "Afaan Oromoo"
    },
    "or": {
        "english": "Oriya",
        "native": "\u0b13\u0b21\u0b3c\u0b3f\u0b06"
    },
    "ori": {
        "english": "Oriya",
        "native": "\u0b13\u0b21\u0b3c\u0b3f\u0b06"
    },
    "orm": {
        "english": "Oromo",
        "native": "Afaan Oromoo"
    },
    "os": {
        "english": "Ossetian",
        "native": "Ossetian"
    },
    "osa": {
        "english": "Osage",
        "native": "Osage"
    },
    "oss": {
        "english": "Ossetian",
        "native": "Ossetian"
    },
    "ota": {
        "english": "Turkish Ottoman (1500-1928)",
        "native": "Turkish Ottoman (1500-1928)"
    },
    "oto": {
        "english": "Otomian Languages",
        "native": "Otomian Languages"
    },
    "pa": {
        "english": "Panjabi",
        "native": "Panjabi"
    },
    "paa": {
        "english": "Papuan Languages",
        "native": "Papuan Languages"
    },
    "pag": {
        "english": "Pangasinan",
        "native": "Pangasinan"
    },
    "pal": {
        "english": "Pahlavi",
        "native": "Pahlavi"
    },
    "pam": {
        "english": "Kapampangan",
        "native": "Kapampangan"
    },
    "pan": {
        "english": "Panjabi",
        "native": "Panjabi"
    },
    "pap": {
        "english": "Papiamento",
        "native": "Papiamento"
    },
    "pau": {
        "english": "Palauan",
        "native": "Palauan"
    },
    "peo": {
        "english": "Persian Old (ca.600-400 B.C.)",
        "native": "Persian Old (ca.600-400 B.C.)"
    },
    "per": {
        "english": "Persian",
        "native": "\u0641\u0627\u0631\u0633\u06cc"
    },
    "phi": {
        "english": "Philippine Languages",
        "native": "Philippine Languages"
    },
    "phn": {
        "english": "Phoenician",
        "native": "Phoenician"
    },
    "pi": {
        "english": "Pali",
        "native": "Pali"
    },
    "pl": {
        "english": "Polish",
        "native": "Polski"
    },
    "pli": {
        "english": "Pali",
        "native": "Pali"
    },
    "pol": {
        "english": "Polish",
        "native": "Polski"
    },
    "pon": {
        "english": "Pohnpeian",
        "native": "Pohnpeian"
    },
    "por": {
        "english": "Portuguese",
        "native": "Portugu\u00eas"
    },
    "pra": {
        "english": "Prakrit Languages",
        "native": "Prakrit Languages"
    },
    "pro": {
        "english": "Proven\u00e7al Old (to 1500)",
        "native": "Proven\u00e7al Old (to 1500)"
    },
    "ps": {
        "english": "Pashto",
        "native": "Pashto"
    },
    "pt": {
        "english": "Portuguese",
        "native": "Portugu\u00eas"
    },
    "pus": {
        "english": "Pashto",
        "native": "Pashto"
    },
    "qaa-qtz": {
        "english": "Reserved For Local Use",
        "native": "Reserved For Local Use"
    },
    "qu": {
        "english": "Quechua",
        "native": "Kichwa"
    },
    "que": {
        "english": "Quechua",
        "native": "Kichwa"
    },
    "raj": {
        "english": "Rajasthani",
        "native": "Rajasthani"
    },
    "rap": {
        "english": "Rapanui",
        "native": "Rapanui"
    },
    "rar": {
        "english": "Cook Islands Maori",
        "native": "Cook Islands Maori"
    },
    "rm": {
        "english": "Romansh",
        "native": "Rumantsch Grischun"
    },
    "rn": {
        "english": "Rundi",
        "native": "Rundi"
    },
    "ro": {
        "english": "Moldavian",
        "native": "Moldavian"
    },
    "roa": {
        "english": "Romance Languages",
        "native": "Romance Languages"
    },
    "roh": {
        "english": "Romansh",
        "native": "Rumantsch Grischun"
    },
    "rom": {
        "english": "Romany",
        "native": "Romany"
    },
    "ron": {
        "english": "Moldavian",
        "native": "Moldavian"
    },
    "ru": {
        "english": "Russian",
        "native": "\u0440\u0443\u0441\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a"
    },
    "rum": {
        "english": "Moldavian",
        "native": "Moldavian"
    },
    "run": {
        "english": "Rundi",
        "native": "Rundi"
    },
    "rup": {
        "english": "Aromanian",
        "native": "Aromanian"
    },
    "rus": {
        "english": "Russian",
        "native": "\u0440\u0443\u0441\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a"
    },
    "rw": {
        "english": "Kinyarwanda",
        "native": "Ikinyarwanda"
    },
    "sa": {
        "english": "Sanskrit",
        "native": "Sanskrit"
    },
    "sad": {
        "english": "Sandawe",
        "native": "Sandawe"
    },
    "sag": {
        "english": "Sango",
        "native": "Y\u00e2ng\u00e2 T\u00ee S\u00e4ng\u00f6"
    },
    "sah": {
        "english": "Yakut",
        "native": "Yakut"
    },
    "sai": {
        "english": "South American Indian (Other)",
        "native": "South American Indian (Other)"
    },
    "sal": {
        "english": "Salishan Languages",
        "native": "Salishan Languages"
    },
    "sam": {
        "english": "Samaritan Aramaic",
        "native": "Samaritan Aramaic"
    },
    "san": {
        "english": "Sanskrit",
        "native": "Sanskrit"
    },
    "sas": {
        "english": "Sasak",
        "native": "Sasak"
    },
    "sat": {
        "english": "Santali",
        "native": "Santali"
    },
    "sc": {
        "english": "Sardinian",
        "native": "Sardu"
    },
    "scn": {
        "english": "Sicilian",
        "native": "Sicilian"
    },
    "sco": {
        "english": "Scots",
        "native": "Scots"
    },
    "sd": {
        "english": "Sindhi",
        "native": "\u0633\u0646\u068c\u064a\u060c \u0633\u0646\u062f\u06be\u06cc\u200e"
    },
    "se": {
        "english": "Northern Sami",
        "native": "Davvis\u00e1megiella"
    },
    "sel": {
        "english": "Selkup",
        "native": "Selkup"
    },
    "sem": {
        "english": "Semitic Languages",
        "native": "Semitic Languages"
    },
    "sg": {
        "english": "Sango",
        "native": "Y\u00e2ng\u00e2 T\u00ee S\u00e4ng\u00f6"
    },
    "sga": {
        "english": "Irish Old (to 900)",
        "native": "Irish Old (to 900)"
    },
    "sgn": {
        "english": "Sign Languages",
        "native": "Sign Languages"
    },
    "shn": {
        "english": "Shan",
        "native": "Shan"
    },
    "si": {
        "english": "Sinhala",
        "native": "Sinhala"
    },
    "sid": {
        "english": "Sidamo",
        "native": "Sidamo"
    },
    "sin": {
        "english": "Sinhala",
        "native": "Sinhala"
    },
    "sio": {
        "english": "Siouan Languages",
        "native": "Siouan Languages"
    },
    "sit": {
        "english": "Sino-Tibetan Languages",
        "native": "Sino-Tibetan Languages"
    },
    "sk": {
        "english": "Slovak",
        "native": "Sloven\u010dina"
    },
    "sl": {
        "english": "Slovenian",
        "native": "Slovenian"
    },
    "sla": {
        "english": "Slavic Languages",
        "native": "Slavic Languages"
    },
    "slk": {
        "english": "Slovak",
        "native": "Sloven\u010dina"
    },
    "slo": {
        "english": "Slovak",
        "native": "Sloven\u010dina"
    },
    "slv": {
        "english": "Slovenian",
        "native": "Slovenian"
    },
    "sm": {
        "english": "Samoan",
        "native": "Gagana Faa Samoa"
    },
    "sma": {
        "english": "Southern Sami",
        "native": "Southern Sami"
    },
    "sme": {
        "english": "Northern Sami",
        "native": "Davvis\u00e1megiella"
    },
    "smi": {
        "english": "Sami Languages",
        "native": "Sami Languages"
    },
    "smj": {
        "english": "Lule Sami",
        "native": "Lule Sami"
    },
    "smn": {
        "english": "Inari Sami",
        "native": "Inari Sami"
    },
    "smo": {
        "english": "Samoan",
        "native": "Gagana Faa Samoa"
    },
    "sms": {
        "english": "Skolt Sami",
        "native": "Skolt Sami"
    },
    "sn": {
        "english": "Shona",
        "native": "ChiShona"
    },
    "sna": {
        "english": "Shona",
        "native": "ChiShona"
    },
    "snd": {
        "english": "Sindhi",
        "native": "\u0633\u0646\u068c\u064a\u060c \u0633\u0646\u062f\u06be\u06cc\u200e"
    },
    "snk": {
        "english": "Soninke",
        "native": "Soninke"
    },
    "so": {
        "english": "Somali",
        "native": "Af Soomaali"
    },
    "sog": {
        "english": "Sogdian",
        "native": "Sogdian"
    },
    "som": {
        "english": "Somali",
        "native": "Af Soomaali"
    },
    "son": {
        "english": "Songhai Languages",
        "native": "Songhai Languages"
    },
    "sot": {
        "english": "Sotho",
        "native": "Sotho"
    },
    "spa": {
        "english": "Castilian",
        "native": "Castellano"
    },
    "sq": {
        "english": "Albanian",
        "native": "Shqip"
    },
    "sqi": {
        "english": "Albanian",
        "native": "Shqip"
    },
    "sr": {
        "english": "Serbian",
        "native": "\u0441\u0440\u043f\u0441\u043a\u0438 \u0458\u0435\u0437\u0438\u043a"
    },
    "srd": {
        "english": "Sardinian",
        "native": "Sardu"
    },
    "srn": {
        "english": "Sranan Tongo",
        "native": "Sranan Tongo"
    },
    "srp": {
        "english": "Serbian",
        "native": "\u0441\u0440\u043f\u0441\u043a\u0438 \u0458\u0435\u0437\u0438\u043a"
    },
    "srr": {
        "english": "Serer",
        "native": "Serer"
    },
    "ss": {
        "english": "Swati",
        "native": "SiSwati"
    },
    "ssa": {
        "english": "Nilo-Saharan Languages",
        "native": "Nilo-Saharan Languages"
    },
    "ssw": {
        "english": "Swati",
        "native": "SiSwati"
    },
    "st": {
        "english": "Sotho",
        "native": "Sotho"
    },
    "su": {
        "english": "Sundanese",
        "native": "Basa Sunda"
    },
    "suk": {
        "english": "Sukuma",
        "native": "Sukuma"
    },
    "sun": {
        "english": "Sundanese",
        "native": "Basa Sunda"
    },
    "sus": {
        "english": "Susu",
        "native": "Susu"
    },
    "sux": {
        "english": "Sumerian",
        "native": "Sumerian"
    },
    "sv": {
        "english": "Swedish",
        "native": "Svenska"
    },
    "sw": {
        "english": "Swahili",
        "native": "Kiswahili"
    },
    "swa": {
        "english": "Swahili",
        "native": "Kiswahili"
    },
    "swe": {
        "english": "Swedish",
        "native": "Svenska"
    },
    "syc": {
        "english": "Classical Syriac",
        "native": "Classical Syriac"
    },
    "syr": {
        "english": "Syriac",
        "native": "Syriac"
    },
    "ta": {
        "english": "Tamil",
        "native": "\u0ba4\u0bae\u0bbf\u0bb4\u0bcd"
    },
    "tah": {
        "english": "Tahitian",
        "native": "Reo Tahiti"
    },
    "tai": {
        "english": "Tai Languages",
        "native": "Tai Languages"
    },
    "tam": {
        "english": "Tamil",
        "native": "\u0ba4\u0bae\u0bbf\u0bb4\u0bcd"
    },
    "tat": {
        "english": "Tatar",
        "native": "Tatar\u00e7a"
    },
    "te": {
        "english": "Telugu",
        "native": "\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41"
    },
    "tel": {
        "english": "Telugu",
        "native": "\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41"
    },
    "tem": {
        "english": "Timne",
        "native": "Timne"
    },
    "ter": {
        "english": "Tereno",
        "native": "Tereno"
    },
    "tet": {
        "english": "Tetum",
        "native": "Tetum"
    },
    "tg": {
        "english": "Tajik",
        "native": "To\u011fik\u012b"
    },
    "tgk": {
        "english": "Tajik",
        "native": "To\u011fik\u012b"
    },
    "tgl": {
        "english": "Tagalog",
        "native": "Wikang Tagalog"
    },
    "th": {
        "english": "Thai",
        "native": "\u0e44\u0e17\u0e22"
    },
    "tha": {
        "english": "Thai",
        "native": "\u0e44\u0e17\u0e22"
    },
    "ti": {
        "english": "Tigrinya",
        "native": "\u1275\u130d\u122d\u129b"
    },
    "tib": {
        "english": "Tibetan",
        "native": "Tibetan"
    },
    "tig": {
        "english": "Tigre",
        "native": "Tigre"
    },
    "tir": {
        "english": "Tigrinya",
        "native": "\u1275\u130d\u122d\u129b"
    },
    "tiv": {
        "english": "Tiv",
        "native": "Tiv"
    },
    "tk": {
        "english": "Turkmen",
        "native": "T\u00fcrkmen"
    },
    "tkl": {
        "english": "Tokelau",
        "native": "Tokelau"
    },
    "tl": {
        "english": "Tagalog",
        "native": "Wikang Tagalog"
    },
    "tlh": {
        "english": "Klingon",
        "native": "Klingon"
    },
    "tli": {
        "english": "Tlingit",
        "native": "Tlingit"
    },
    "tmh": {
        "english": "Tamashek",
        "native": "Tamashek"
    },
    "tn": {
        "english": "Tswana",
        "native": "Setswana"
    },
    "to": {
        "english": "Tonga (Tonga Islands)",
        "native": "Faka Tonga"
    },
    "tog": {
        "english": "Tonga (Nyasa)",
        "native": "Tonga (Nyasa)"
    },
    "ton": {
        "english": "Tonga (Tonga Islands)",
        "native": "Faka Tonga"
    },
    "tpi": {
        "english": "Tok Pisin",
        "native": "Tok Pisin"
    },
    "tr": {
        "english": "Turkish",
        "native": "T\u00fcrk\u00e7e"
    },
    "ts": {
        "english": "Tsonga",
        "native": "Xitsonga"
    },
    "tsi": {
        "english": "Tsimshian",
        "native": "Tsimshian"
    },
    "tsn": {
        "english": "Tswana",
        "native": "Setswana"
    },
    "tso": {
        "english": "Tsonga",
        "native": "Xitsonga"
    },
    "tt": {
        "english": "Tatar",
        "native": "Tatar\u00e7a"
    },
    "tuk": {
        "english": "Turkmen",
        "native": "T\u00fcrkmen"
    },
    "tum": {
        "english": "Tumbuka",
        "native": "Tumbuka"
    },
    "tup": {
        "english": "Tupi Languages",
        "native": "Tupi Languages"
    },
    "tur": {
        "english": "Turkish",
        "native": "T\u00fcrk\u00e7e"
    },
    "tut": {
        "english": "Altaic Languages",
        "native": "Altaic Languages"
    },
    "tvl": {
        "english": "Tuvalu",
        "native": "Tuvalu"
    },
    "tw": {
        "english": "Twi",
        "native": "Twi"
    },
    "twi": {
        "english": "Twi",
        "native": "Twi"
    },
    "ty": {
        "english": "Tahitian",
        "native": "Reo Tahiti"
    },
    "tyv": {
        "english": "Tuvinian",
        "native": "Tuvinian"
    },
    "udm": {
        "english": "Udmurt",
        "native": "Udmurt"
    },
    "ug": {
        "english": "Uighur",
        "native": "Uighur"
    },
    "uga": {
        "english": "Ugaritic",
        "native": "Ugaritic"
    },
    "uig": {
        "english": "Uighur",
        "native": "Uighur"
    },
    "uk": {
        "english": "Ukrainian",
        "native": "\u0443\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430"
    },
    "ukr": {
        "english": "Ukrainian",
        "native": "\u0443\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430"
    },
    "umb": {
        "english": "Umbundu",
        "native": "Umbundu"
    },
    "und": {
        "english": "Undetermined",
        "native": "Undetermined"
    },
    "ur": {
        "english": "Urdu",
        "native": "\u0627\u0631\u062f\u0648"
    },
    "urd": {
        "english": "Urdu",
        "native": "\u0627\u0631\u062f\u0648"
    },
    "uz": {
        "english": "Uzbek",
        "native": "Zbek"
    },
    "uzb": {
        "english": "Uzbek",
        "native": "Zbek"
    },
    "vai": {
        "english": "Vai",
        "native": "Vai"
    },
    "ve": {
        "english": "Venda",
        "native": "Tshiven\u1e13a"
    },
    "ven": {
        "english": "Venda",
        "native": "Tshiven\u1e13a"
    },
    "vi": {
        "english": "Vietnamese",
        "native": "Ti\u1ebfng Vi\u1ec7t"
    },
    "vie": {
        "english": "Vietnamese",
        "native": "Ti\u1ebfng Vi\u1ec7t"
    },
    "vo": {
        "english": "Volap\u00fck",
        "native": "Volap\u00fck"
    },
    "vol": {
        "english": "Volap\u00fck",
        "native": "Volap\u00fck"
    },
    "vot": {
        "english": "Votic",
        "native": "Votic"
    },
    "wa": {
        "english": "Walloon",
        "native": "Walon"
    },
    "wak": {
        "english": "Wakashan Languages",
        "native": "Wakashan Languages"
    },
    "wal": {
        "english": "Walamo",
        "native": "Walamo"
    },
    "war": {
        "english": "Waray",
        "native": "Waray"
    },
    "was": {
        "english": "Washo",
        "native": "Washo"
    },
    "wel": {
        "english": "Welsh",
        "native": "Cymraeg"
    },
    "wen": {
        "english": "Sorbian Languages",
        "native": "Sorbian Languages"
    },
    "wln": {
        "english": "Walloon",
        "native": "Walon"
    },
    "wo": {
        "english": "Wolof",
        "native": "Wollof"
    },
    "wol": {
        "english": "Wolof",
        "native": "Wollof"
    },
    "xal": {
        "english": "Kalmyk",
        "native": "Kalmyk"
    },
    "xh": {
        "english": "Xhosa",
        "native": "IsiXhosa"
    },
    "xho": {
        "english": "Xhosa",
        "native": "IsiXhosa"
    },
    "yao": {
        "english": "Yao",
        "native": "Yao"
    },
    "yap": {
        "english": "Yapese",
        "native": "Yapese"
    },
    "yi": {
        "english": "Yiddish",
        "native": "\u05d9\u05d9\u05b4\u05d3\u05d9\u05e9"
    },
    "yid": {
        "english": "Yiddish",
        "native": "\u05d9\u05d9\u05b4\u05d3\u05d9\u05e9"
    },
    "yo": {
        "english": "Yoruba",
        "native": "Yor\u00f9b\u00e1"
    },
    "yor": {
        "english": "Yoruba",
        "native": "Yor\u00f9b\u00e1"
    },
    "ypk": {
        "english": "Yupik Languages",
        "native": "Yupik Languages"
    },
    "za": {
        "english": "Chuang",
        "native": "Chuang"
    },
    "zap": {
        "english": "Zapotec",
        "native": "Zapotec"
    },
    "zbl": {
        "english": "Bliss",
        "native": "Bliss"
    },
    "zen": {
        "english": "Zenaga",
        "native": "Zenaga"
    },
    "zgh": {
        "english": "Standard Moroccan Tamazight",
        "native": "Standard Moroccan Tamazight"
    },
    "zh": {
        "english": "Chinese",
        "native": "\u4e2d\u6587 (Zh\u014dngw\u00e9n)"
    },
    "zha": {
        "english": "Chuang",
        "native": "Chuang"
    },
    "zho": {
        "english": "Chinese",
        "native": "\u4e2d\u6587 (Zh\u014dngw\u00e9n)"
    },
    "znd": {
        "english": "Zande Languages",
        "native": "Zande Languages"
    },
    "zu": {
        "english": "Zulu",
        "native": "Zulu"
    },
    "zul": {
        "english": "Zulu",
        "native": "Zulu"
    },
    "zun": {
        "english": "Zuni",
        "native": "Zuni"
    },
    "zxx": {
        "english": "No Linguistic Content",
        "native": "No Linguistic Content"
    },
    "zza": {
        "english": "Dimili",
        "native": "Dimili"
    }
}

COUNTRY_INFO_BY_ISO_ALPHA2 = {
    "AD": {
        "alpha-2": "AD",
        "alpha-3": "AND",
        "country-code": "020",
        "iso_3166-2": "ISO 3166-2:AD",
        "name": "Andorra",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "AE": {
        "alpha-2": "AE",
        "alpha-3": "ARE",
        "country-code": "784",
        "iso_3166-2": "ISO 3166-2:AE",
        "name": "United Arab Emirates",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "AF": {
        "alpha-2": "AF",
        "alpha-3": "AFG",
        "country-code": "004",
        "iso_3166-2": "ISO 3166-2:AF",
        "name": "Afghanistan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "AG": {
        "alpha-2": "AG",
        "alpha-3": "ATG",
        "country-code": "028",
        "iso_3166-2": "ISO 3166-2:AG",
        "name": "Antigua and Barbuda",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "AI": {
        "alpha-2": "AI",
        "alpha-3": "AIA",
        "country-code": "660",
        "iso_3166-2": "ISO 3166-2:AI",
        "name": "Anguilla",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "AL": {
        "alpha-2": "AL",
        "alpha-3": "ALB",
        "country-code": "008",
        "iso_3166-2": "ISO 3166-2:AL",
        "name": "Albania",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "AM": {
        "alpha-2": "AM",
        "alpha-3": "ARM",
        "country-code": "051",
        "iso_3166-2": "ISO 3166-2:AM",
        "name": "Armenia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "AO": {
        "alpha-2": "AO",
        "alpha-3": "AGO",
        "country-code": "024",
        "iso_3166-2": "ISO 3166-2:AO",
        "name": "Angola",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "AQ": {
        "alpha-2": "AQ",
        "alpha-3": "ATA",
        "country-code": "010",
        "iso_3166-2": "ISO 3166-2:AQ",
        "name": "Antarctica",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "AR": {
        "alpha-2": "AR",
        "alpha-3": "ARG",
        "country-code": "032",
        "iso_3166-2": "ISO 3166-2:AR",
        "name": "Argentina",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "AS": {
        "alpha-2": "AS",
        "alpha-3": "ASM",
        "country-code": "016",
        "iso_3166-2": "ISO 3166-2:AS",
        "name": "American Samoa",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "AT": {
        "alpha-2": "AT",
        "alpha-3": "AUT",
        "country-code": "040",
        "iso_3166-2": "ISO 3166-2:AT",
        "name": "Austria",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "AU": {
        "alpha-2": "AU",
        "alpha-3": "AUS",
        "country-code": "036",
        "iso_3166-2": "ISO 3166-2:AU",
        "name": "Australia",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Australia and New Zealand",
        "sub-region-code": "053"
    },
    "AW": {
        "alpha-2": "AW",
        "alpha-3": "ABW",
        "country-code": "533",
        "iso_3166-2": "ISO 3166-2:AW",
        "name": "Aruba",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "AX": {
        "alpha-2": "AX",
        "alpha-3": "ALA",
        "country-code": "248",
        "iso_3166-2": "ISO 3166-2:AX",
        "name": "\u00c5land Islands",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "AZ": {
        "alpha-2": "AZ",
        "alpha-3": "AZE",
        "country-code": "031",
        "iso_3166-2": "ISO 3166-2:AZ",
        "name": "Azerbaijan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "BA": {
        "alpha-2": "BA",
        "alpha-3": "BIH",
        "country-code": "070",
        "iso_3166-2": "ISO 3166-2:BA",
        "name": "Bosnia and Herzegovina",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "BB": {
        "alpha-2": "BB",
        "alpha-3": "BRB",
        "country-code": "052",
        "iso_3166-2": "ISO 3166-2:BB",
        "name": "Barbados",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "BD": {
        "alpha-2": "BD",
        "alpha-3": "BGD",
        "country-code": "050",
        "iso_3166-2": "ISO 3166-2:BD",
        "name": "Bangladesh",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "BE": {
        "alpha-2": "BE",
        "alpha-3": "BEL",
        "country-code": "056",
        "iso_3166-2": "ISO 3166-2:BE",
        "name": "Belgium",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "BF": {
        "alpha-2": "BF",
        "alpha-3": "BFA",
        "country-code": "854",
        "iso_3166-2": "ISO 3166-2:BF",
        "name": "Burkina Faso",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "BG": {
        "alpha-2": "BG",
        "alpha-3": "BGR",
        "country-code": "100",
        "iso_3166-2": "ISO 3166-2:BG",
        "name": "Bulgaria",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "BH": {
        "alpha-2": "BH",
        "alpha-3": "BHR",
        "country-code": "048",
        "iso_3166-2": "ISO 3166-2:BH",
        "name": "Bahrain",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "BI": {
        "alpha-2": "BI",
        "alpha-3": "BDI",
        "country-code": "108",
        "iso_3166-2": "ISO 3166-2:BI",
        "name": "Burundi",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "BJ": {
        "alpha-2": "BJ",
        "alpha-3": "BEN",
        "country-code": "204",
        "iso_3166-2": "ISO 3166-2:BJ",
        "name": "Benin",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "BL": {
        "alpha-2": "BL",
        "alpha-3": "BLM",
        "country-code": "652",
        "iso_3166-2": "ISO 3166-2:BL",
        "name": "Saint Barth\u00e9lemy",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "BM": {
        "alpha-2": "BM",
        "alpha-3": "BMU",
        "country-code": "060",
        "iso_3166-2": "ISO 3166-2:BM",
        "name": "Bermuda",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Northern America",
        "sub-region-code": "021"
    },
    "BN": {
        "alpha-2": "BN",
        "alpha-3": "BRN",
        "country-code": "096",
        "iso_3166-2": "ISO 3166-2:BN",
        "name": "Brunei Darussalam",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "BO": {
        "alpha-2": "BO",
        "alpha-3": "BOL",
        "country-code": "068",
        "iso_3166-2": "ISO 3166-2:BO",
        "name": "Bolivia (Plurinational State of)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "BQ": {
        "alpha-2": "BQ",
        "alpha-3": "BES",
        "country-code": "535",
        "iso_3166-2": "ISO 3166-2:BQ",
        "name": "Bonaire, Sint Eustatius and Saba",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "BR": {
        "alpha-2": "BR",
        "alpha-3": "BRA",
        "country-code": "076",
        "iso_3166-2": "ISO 3166-2:BR",
        "name": "Brazil",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "BS": {
        "alpha-2": "BS",
        "alpha-3": "BHS",
        "country-code": "044",
        "iso_3166-2": "ISO 3166-2:BS",
        "name": "Bahamas",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "BT": {
        "alpha-2": "BT",
        "alpha-3": "BTN",
        "country-code": "064",
        "iso_3166-2": "ISO 3166-2:BT",
        "name": "Bhutan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "BV": {
        "alpha-2": "BV",
        "alpha-3": "BVT",
        "country-code": "074",
        "iso_3166-2": "ISO 3166-2:BV",
        "name": "Bouvet Island",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "BW": {
        "alpha-2": "BW",
        "alpha-3": "BWA",
        "country-code": "072",
        "iso_3166-2": "ISO 3166-2:BW",
        "name": "Botswana",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Southern Africa",
        "sub-region-code": "018"
    },
    "BY": {
        "alpha-2": "BY",
        "alpha-3": "BLR",
        "country-code": "112",
        "iso_3166-2": "ISO 3166-2:BY",
        "name": "Belarus",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "BZ": {
        "alpha-2": "BZ",
        "alpha-3": "BLZ",
        "country-code": "084",
        "iso_3166-2": "ISO 3166-2:BZ",
        "name": "Belize",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "CA": {
        "alpha-2": "CA",
        "alpha-3": "CAN",
        "country-code": "124",
        "iso_3166-2": "ISO 3166-2:CA",
        "name": "Canada",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Northern America",
        "sub-region-code": "021"
    },
    "CC": {
        "alpha-2": "CC",
        "alpha-3": "CCK",
        "country-code": "166",
        "iso_3166-2": "ISO 3166-2:CC",
        "name": "Cocos (Keeling) Islands",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "CD": {
        "alpha-2": "CD",
        "alpha-3": "COD",
        "country-code": "180",
        "iso_3166-2": "ISO 3166-2:CD",
        "name": "Congo (Democratic Republic of the)",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "CF": {
        "alpha-2": "CF",
        "alpha-3": "CAF",
        "country-code": "140",
        "iso_3166-2": "ISO 3166-2:CF",
        "name": "Central African Republic",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "CG": {
        "alpha-2": "CG",
        "alpha-3": "COG",
        "country-code": "178",
        "iso_3166-2": "ISO 3166-2:CG",
        "name": "Congo",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "CH": {
        "alpha-2": "CH",
        "alpha-3": "CHE",
        "country-code": "756",
        "iso_3166-2": "ISO 3166-2:CH",
        "name": "Switzerland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "CI": {
        "alpha-2": "CI",
        "alpha-3": "CIV",
        "country-code": "384",
        "iso_3166-2": "ISO 3166-2:CI",
        "name": "C\u00f4te d'Ivoire",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "CK": {
        "alpha-2": "CK",
        "alpha-3": "COK",
        "country-code": "184",
        "iso_3166-2": "ISO 3166-2:CK",
        "name": "Cook Islands",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "CL": {
        "alpha-2": "CL",
        "alpha-3": "CHL",
        "country-code": "152",
        "iso_3166-2": "ISO 3166-2:CL",
        "name": "Chile",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "CM": {
        "alpha-2": "CM",
        "alpha-3": "CMR",
        "country-code": "120",
        "iso_3166-2": "ISO 3166-2:CM",
        "name": "Cameroon",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "CN": {
        "alpha-2": "CN",
        "alpha-3": "CHN",
        "country-code": "156",
        "iso_3166-2": "ISO 3166-2:CN",
        "name": "China",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "CO": {
        "alpha-2": "CO",
        "alpha-3": "COL",
        "country-code": "170",
        "iso_3166-2": "ISO 3166-2:CO",
        "name": "Colombia",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "CR": {
        "alpha-2": "CR",
        "alpha-3": "CRI",
        "country-code": "188",
        "iso_3166-2": "ISO 3166-2:CR",
        "name": "Costa Rica",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "CU": {
        "alpha-2": "CU",
        "alpha-3": "CUB",
        "country-code": "192",
        "iso_3166-2": "ISO 3166-2:CU",
        "name": "Cuba",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "CV": {
        "alpha-2": "CV",
        "alpha-3": "CPV",
        "country-code": "132",
        "iso_3166-2": "ISO 3166-2:CV",
        "name": "Cabo Verde",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "CW": {
        "alpha-2": "CW",
        "alpha-3": "CUW",
        "country-code": "531",
        "iso_3166-2": "ISO 3166-2:CW",
        "name": "Cura\u00e7ao",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "CX": {
        "alpha-2": "CX",
        "alpha-3": "CXR",
        "country-code": "162",
        "iso_3166-2": "ISO 3166-2:CX",
        "name": "Christmas Island",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "CY": {
        "alpha-2": "CY",
        "alpha-3": "CYP",
        "country-code": "196",
        "iso_3166-2": "ISO 3166-2:CY",
        "name": "Cyprus",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "CZ": {
        "alpha-2": "CZ",
        "alpha-3": "CZE",
        "country-code": "203",
        "iso_3166-2": "ISO 3166-2:CZ",
        "name": "Czech Republic",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "DE": {
        "alpha-2": "DE",
        "alpha-3": "DEU",
        "country-code": "276",
        "iso_3166-2": "ISO 3166-2:DE",
        "name": "Germany",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "DJ": {
        "alpha-2": "DJ",
        "alpha-3": "DJI",
        "country-code": "262",
        "iso_3166-2": "ISO 3166-2:DJ",
        "name": "Djibouti",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "DK": {
        "alpha-2": "DK",
        "alpha-3": "DNK",
        "country-code": "208",
        "iso_3166-2": "ISO 3166-2:DK",
        "name": "Denmark",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "DM": {
        "alpha-2": "DM",
        "alpha-3": "DMA",
        "country-code": "212",
        "iso_3166-2": "ISO 3166-2:DM",
        "name": "Dominica",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "DO": {
        "alpha-2": "DO",
        "alpha-3": "DOM",
        "country-code": "214",
        "iso_3166-2": "ISO 3166-2:DO",
        "name": "Dominican Republic",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "DZ": {
        "alpha-2": "DZ",
        "alpha-3": "DZA",
        "country-code": "012",
        "iso_3166-2": "ISO 3166-2:DZ",
        "name": "Algeria",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "EC": {
        "alpha-2": "EC",
        "alpha-3": "ECU",
        "country-code": "218",
        "iso_3166-2": "ISO 3166-2:EC",
        "name": "Ecuador",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "EE": {
        "alpha-2": "EE",
        "alpha-3": "EST",
        "country-code": "233",
        "iso_3166-2": "ISO 3166-2:EE",
        "name": "Estonia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "EG": {
        "alpha-2": "EG",
        "alpha-3": "EGY",
        "country-code": "818",
        "iso_3166-2": "ISO 3166-2:EG",
        "name": "Egypt",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "EH": {
        "alpha-2": "EH",
        "alpha-3": "ESH",
        "country-code": "732",
        "iso_3166-2": "ISO 3166-2:EH",
        "name": "Western Sahara",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "ER": {
        "alpha-2": "ER",
        "alpha-3": "ERI",
        "country-code": "232",
        "iso_3166-2": "ISO 3166-2:ER",
        "name": "Eritrea",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "ES": {
        "alpha-2": "ES",
        "alpha-3": "ESP",
        "country-code": "724",
        "iso_3166-2": "ISO 3166-2:ES",
        "name": "Spain",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "ET": {
        "alpha-2": "ET",
        "alpha-3": "ETH",
        "country-code": "231",
        "iso_3166-2": "ISO 3166-2:ET",
        "name": "Ethiopia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "FI": {
        "alpha-2": "FI",
        "alpha-3": "FIN",
        "country-code": "246",
        "iso_3166-2": "ISO 3166-2:FI",
        "name": "Finland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "FJ": {
        "alpha-2": "FJ",
        "alpha-3": "FJI",
        "country-code": "242",
        "iso_3166-2": "ISO 3166-2:FJ",
        "name": "Fiji",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Melanesia",
        "sub-region-code": "054"
    },
    "FK": {
        "alpha-2": "FK",
        "alpha-3": "FLK",
        "country-code": "238",
        "iso_3166-2": "ISO 3166-2:FK",
        "name": "Falkland Islands (Malvinas)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "FM": {
        "alpha-2": "FM",
        "alpha-3": "FSM",
        "country-code": "583",
        "iso_3166-2": "ISO 3166-2:FM",
        "name": "Micronesia (Federated States of)",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "FO": {
        "alpha-2": "FO",
        "alpha-3": "FRO",
        "country-code": "234",
        "iso_3166-2": "ISO 3166-2:FO",
        "name": "Faroe Islands",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "FR": {
        "alpha-2": "FR",
        "alpha-3": "FRA",
        "country-code": "250",
        "iso_3166-2": "ISO 3166-2:FR",
        "name": "France",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "GA": {
        "alpha-2": "GA",
        "alpha-3": "GAB",
        "country-code": "266",
        "iso_3166-2": "ISO 3166-2:GA",
        "name": "Gabon",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "GB": {
        "alpha-2": "GB",
        "alpha-3": "GBR",
        "country-code": "826",
        "iso_3166-2": "ISO 3166-2:GB",
        "name": "United Kingdom of Great Britain and Northern Ireland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "GD": {
        "alpha-2": "GD",
        "alpha-3": "GRD",
        "country-code": "308",
        "iso_3166-2": "ISO 3166-2:GD",
        "name": "Grenada",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "GE": {
        "alpha-2": "GE",
        "alpha-3": "GEO",
        "country-code": "268",
        "iso_3166-2": "ISO 3166-2:GE",
        "name": "Georgia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "GF": {
        "alpha-2": "GF",
        "alpha-3": "GUF",
        "country-code": "254",
        "iso_3166-2": "ISO 3166-2:GF",
        "name": "French Guiana",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "GG": {
        "alpha-2": "GG",
        "alpha-3": "GGY",
        "country-code": "831",
        "iso_3166-2": "ISO 3166-2:GG",
        "name": "Guernsey",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "GH": {
        "alpha-2": "GH",
        "alpha-3": "GHA",
        "country-code": "288",
        "iso_3166-2": "ISO 3166-2:GH",
        "name": "Ghana",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "GI": {
        "alpha-2": "GI",
        "alpha-3": "GIB",
        "country-code": "292",
        "iso_3166-2": "ISO 3166-2:GI",
        "name": "Gibraltar",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "GL": {
        "alpha-2": "GL",
        "alpha-3": "GRL",
        "country-code": "304",
        "iso_3166-2": "ISO 3166-2:GL",
        "name": "Greenland",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Northern America",
        "sub-region-code": "021"
    },
    "GM": {
        "alpha-2": "GM",
        "alpha-3": "GMB",
        "country-code": "270",
        "iso_3166-2": "ISO 3166-2:GM",
        "name": "Gambia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "GN": {
        "alpha-2": "GN",
        "alpha-3": "GIN",
        "country-code": "324",
        "iso_3166-2": "ISO 3166-2:GN",
        "name": "Guinea",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "GP": {
        "alpha-2": "GP",
        "alpha-3": "GLP",
        "country-code": "312",
        "iso_3166-2": "ISO 3166-2:GP",
        "name": "Guadeloupe",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "GQ": {
        "alpha-2": "GQ",
        "alpha-3": "GNQ",
        "country-code": "226",
        "iso_3166-2": "ISO 3166-2:GQ",
        "name": "Equatorial Guinea",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "GR": {
        "alpha-2": "GR",
        "alpha-3": "GRC",
        "country-code": "300",
        "iso_3166-2": "ISO 3166-2:GR",
        "name": "Greece",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "GS": {
        "alpha-2": "GS",
        "alpha-3": "SGS",
        "country-code": "239",
        "iso_3166-2": "ISO 3166-2:GS",
        "name": "South Georgia and the South Sandwich Islands",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "GT": {
        "alpha-2": "GT",
        "alpha-3": "GTM",
        "country-code": "320",
        "iso_3166-2": "ISO 3166-2:GT",
        "name": "Guatemala",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "GU": {
        "alpha-2": "GU",
        "alpha-3": "GUM",
        "country-code": "316",
        "iso_3166-2": "ISO 3166-2:GU",
        "name": "Guam",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "GW": {
        "alpha-2": "GW",
        "alpha-3": "GNB",
        "country-code": "624",
        "iso_3166-2": "ISO 3166-2:GW",
        "name": "Guinea-Bissau",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "GY": {
        "alpha-2": "GY",
        "alpha-3": "GUY",
        "country-code": "328",
        "iso_3166-2": "ISO 3166-2:GY",
        "name": "Guyana",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "HK": {
        "alpha-2": "HK",
        "alpha-3": "HKG",
        "country-code": "344",
        "iso_3166-2": "ISO 3166-2:HK",
        "name": "Hong Kong",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "HM": {
        "alpha-2": "HM",
        "alpha-3": "HMD",
        "country-code": "334",
        "iso_3166-2": "ISO 3166-2:HM",
        "name": "Heard Island and McDonald Islands",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "HN": {
        "alpha-2": "HN",
        "alpha-3": "HND",
        "country-code": "340",
        "iso_3166-2": "ISO 3166-2:HN",
        "name": "Honduras",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "HR": {
        "alpha-2": "HR",
        "alpha-3": "HRV",
        "country-code": "191",
        "iso_3166-2": "ISO 3166-2:HR",
        "name": "Croatia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "HT": {
        "alpha-2": "HT",
        "alpha-3": "HTI",
        "country-code": "332",
        "iso_3166-2": "ISO 3166-2:HT",
        "name": "Haiti",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "HU": {
        "alpha-2": "HU",
        "alpha-3": "HUN",
        "country-code": "348",
        "iso_3166-2": "ISO 3166-2:HU",
        "name": "Hungary",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "ID": {
        "alpha-2": "ID",
        "alpha-3": "IDN",
        "country-code": "360",
        "iso_3166-2": "ISO 3166-2:ID",
        "name": "Indonesia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "IE": {
        "alpha-2": "IE",
        "alpha-3": "IRL",
        "country-code": "372",
        "iso_3166-2": "ISO 3166-2:IE",
        "name": "Ireland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "IL": {
        "alpha-2": "IL",
        "alpha-3": "ISR",
        "country-code": "376",
        "iso_3166-2": "ISO 3166-2:IL",
        "name": "Israel",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "IM": {
        "alpha-2": "IM",
        "alpha-3": "IMN",
        "country-code": "833",
        "iso_3166-2": "ISO 3166-2:IM",
        "name": "Isle of Man",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "IN": {
        "alpha-2": "IN",
        "alpha-3": "IND",
        "country-code": "356",
        "iso_3166-2": "ISO 3166-2:IN",
        "name": "India",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "IO": {
        "alpha-2": "IO",
        "alpha-3": "IOT",
        "country-code": "086",
        "iso_3166-2": "ISO 3166-2:IO",
        "name": "British Indian Ocean Territory",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "IQ": {
        "alpha-2": "IQ",
        "alpha-3": "IRQ",
        "country-code": "368",
        "iso_3166-2": "ISO 3166-2:IQ",
        "name": "Iraq",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "IR": {
        "alpha-2": "IR",
        "alpha-3": "IRN",
        "country-code": "364",
        "iso_3166-2": "ISO 3166-2:IR",
        "name": "Iran (Islamic Republic of)",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "IS": {
        "alpha-2": "IS",
        "alpha-3": "ISL",
        "country-code": "352",
        "iso_3166-2": "ISO 3166-2:IS",
        "name": "Iceland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "IT": {
        "alpha-2": "IT",
        "alpha-3": "ITA",
        "country-code": "380",
        "iso_3166-2": "ISO 3166-2:IT",
        "name": "Italy",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "JE": {
        "alpha-2": "JE",
        "alpha-3": "JEY",
        "country-code": "832",
        "iso_3166-2": "ISO 3166-2:JE",
        "name": "Jersey",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "JM": {
        "alpha-2": "JM",
        "alpha-3": "JAM",
        "country-code": "388",
        "iso_3166-2": "ISO 3166-2:JM",
        "name": "Jamaica",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "JO": {
        "alpha-2": "JO",
        "alpha-3": "JOR",
        "country-code": "400",
        "iso_3166-2": "ISO 3166-2:JO",
        "name": "Jordan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "JP": {
        "alpha-2": "JP",
        "alpha-3": "JPN",
        "country-code": "392",
        "iso_3166-2": "ISO 3166-2:JP",
        "name": "Japan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "KE": {
        "alpha-2": "KE",
        "alpha-3": "KEN",
        "country-code": "404",
        "iso_3166-2": "ISO 3166-2:KE",
        "name": "Kenya",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "KG": {
        "alpha-2": "KG",
        "alpha-3": "KGZ",
        "country-code": "417",
        "iso_3166-2": "ISO 3166-2:KG",
        "name": "Kyrgyzstan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Central Asia",
        "sub-region-code": "143"
    },
    "KH": {
        "alpha-2": "KH",
        "alpha-3": "KHM",
        "country-code": "116",
        "iso_3166-2": "ISO 3166-2:KH",
        "name": "Cambodia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "KI": {
        "alpha-2": "KI",
        "alpha-3": "KIR",
        "country-code": "296",
        "iso_3166-2": "ISO 3166-2:KI",
        "name": "Kiribati",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "KM": {
        "alpha-2": "KM",
        "alpha-3": "COM",
        "country-code": "174",
        "iso_3166-2": "ISO 3166-2:KM",
        "name": "Comoros",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "KN": {
        "alpha-2": "KN",
        "alpha-3": "KNA",
        "country-code": "659",
        "iso_3166-2": "ISO 3166-2:KN",
        "name": "Saint Kitts and Nevis",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "KP": {
        "alpha-2": "KP",
        "alpha-3": "PRK",
        "country-code": "408",
        "iso_3166-2": "ISO 3166-2:KP",
        "name": "Korea (Democratic People's Republic of)",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "KR": {
        "alpha-2": "KR",
        "alpha-3": "KOR",
        "country-code": "410",
        "iso_3166-2": "ISO 3166-2:KR",
        "name": "Korea (Republic of)",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "KW": {
        "alpha-2": "KW",
        "alpha-3": "KWT",
        "country-code": "414",
        "iso_3166-2": "ISO 3166-2:KW",
        "name": "Kuwait",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "KY": {
        "alpha-2": "KY",
        "alpha-3": "CYM",
        "country-code": "136",
        "iso_3166-2": "ISO 3166-2:KY",
        "name": "Cayman Islands",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "KZ": {
        "alpha-2": "KZ",
        "alpha-3": "KAZ",
        "country-code": "398",
        "iso_3166-2": "ISO 3166-2:KZ",
        "name": "Kazakhstan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Central Asia",
        "sub-region-code": "143"
    },
    "LA": {
        "alpha-2": "LA",
        "alpha-3": "LAO",
        "country-code": "418",
        "iso_3166-2": "ISO 3166-2:LA",
        "name": "Lao People's Democratic Republic",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "LB": {
        "alpha-2": "LB",
        "alpha-3": "LBN",
        "country-code": "422",
        "iso_3166-2": "ISO 3166-2:LB",
        "name": "Lebanon",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "LC": {
        "alpha-2": "LC",
        "alpha-3": "LCA",
        "country-code": "662",
        "iso_3166-2": "ISO 3166-2:LC",
        "name": "Saint Lucia",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "LI": {
        "alpha-2": "LI",
        "alpha-3": "LIE",
        "country-code": "438",
        "iso_3166-2": "ISO 3166-2:LI",
        "name": "Liechtenstein",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "LK": {
        "alpha-2": "LK",
        "alpha-3": "LKA",
        "country-code": "144",
        "iso_3166-2": "ISO 3166-2:LK",
        "name": "Sri Lanka",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "LR": {
        "alpha-2": "LR",
        "alpha-3": "LBR",
        "country-code": "430",
        "iso_3166-2": "ISO 3166-2:LR",
        "name": "Liberia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "LS": {
        "alpha-2": "LS",
        "alpha-3": "LSO",
        "country-code": "426",
        "iso_3166-2": "ISO 3166-2:LS",
        "name": "Lesotho",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Southern Africa",
        "sub-region-code": "018"
    },
    "LT": {
        "alpha-2": "LT",
        "alpha-3": "LTU",
        "country-code": "440",
        "iso_3166-2": "ISO 3166-2:LT",
        "name": "Lithuania",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "LU": {
        "alpha-2": "LU",
        "alpha-3": "LUX",
        "country-code": "442",
        "iso_3166-2": "ISO 3166-2:LU",
        "name": "Luxembourg",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "LV": {
        "alpha-2": "LV",
        "alpha-3": "LVA",
        "country-code": "428",
        "iso_3166-2": "ISO 3166-2:LV",
        "name": "Latvia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "LY": {
        "alpha-2": "LY",
        "alpha-3": "LBY",
        "country-code": "434",
        "iso_3166-2": "ISO 3166-2:LY",
        "name": "Libya",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "MA": {
        "alpha-2": "MA",
        "alpha-3": "MAR",
        "country-code": "504",
        "iso_3166-2": "ISO 3166-2:MA",
        "name": "Morocco",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "MC": {
        "alpha-2": "MC",
        "alpha-3": "MCO",
        "country-code": "492",
        "iso_3166-2": "ISO 3166-2:MC",
        "name": "Monaco",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "MD": {
        "alpha-2": "MD",
        "alpha-3": "MDA",
        "country-code": "498",
        "iso_3166-2": "ISO 3166-2:MD",
        "name": "Moldova (Republic of)",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "ME": {
        "alpha-2": "ME",
        "alpha-3": "MNE",
        "country-code": "499",
        "iso_3166-2": "ISO 3166-2:ME",
        "name": "Montenegro",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "MF": {
        "alpha-2": "MF",
        "alpha-3": "MAF",
        "country-code": "663",
        "iso_3166-2": "ISO 3166-2:MF",
        "name": "Saint Martin (French part)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "MG": {
        "alpha-2": "MG",
        "alpha-3": "MDG",
        "country-code": "450",
        "iso_3166-2": "ISO 3166-2:MG",
        "name": "Madagascar",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "MH": {
        "alpha-2": "MH",
        "alpha-3": "MHL",
        "country-code": "584",
        "iso_3166-2": "ISO 3166-2:MH",
        "name": "Marshall Islands",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "MK": {
        "alpha-2": "MK",
        "alpha-3": "MKD",
        "country-code": "807",
        "iso_3166-2": "ISO 3166-2:MK",
        "name": "Macedonia (the former Yugoslav Republic of)",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "ML": {
        "alpha-2": "ML",
        "alpha-3": "MLI",
        "country-code": "466",
        "iso_3166-2": "ISO 3166-2:ML",
        "name": "Mali",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "MM": {
        "alpha-2": "MM",
        "alpha-3": "MMR",
        "country-code": "104",
        "iso_3166-2": "ISO 3166-2:MM",
        "name": "Myanmar",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "MN": {
        "alpha-2": "MN",
        "alpha-3": "MNG",
        "country-code": "496",
        "iso_3166-2": "ISO 3166-2:MN",
        "name": "Mongolia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "MO": {
        "alpha-2": "MO",
        "alpha-3": "MAC",
        "country-code": "446",
        "iso_3166-2": "ISO 3166-2:MO",
        "name": "Macao",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "MP": {
        "alpha-2": "MP",
        "alpha-3": "MNP",
        "country-code": "580",
        "iso_3166-2": "ISO 3166-2:MP",
        "name": "Northern Mariana Islands",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "MQ": {
        "alpha-2": "MQ",
        "alpha-3": "MTQ",
        "country-code": "474",
        "iso_3166-2": "ISO 3166-2:MQ",
        "name": "Martinique",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "MR": {
        "alpha-2": "MR",
        "alpha-3": "MRT",
        "country-code": "478",
        "iso_3166-2": "ISO 3166-2:MR",
        "name": "Mauritania",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "MS": {
        "alpha-2": "MS",
        "alpha-3": "MSR",
        "country-code": "500",
        "iso_3166-2": "ISO 3166-2:MS",
        "name": "Montserrat",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "MT": {
        "alpha-2": "MT",
        "alpha-3": "MLT",
        "country-code": "470",
        "iso_3166-2": "ISO 3166-2:MT",
        "name": "Malta",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "MU": {
        "alpha-2": "MU",
        "alpha-3": "MUS",
        "country-code": "480",
        "iso_3166-2": "ISO 3166-2:MU",
        "name": "Mauritius",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "MV": {
        "alpha-2": "MV",
        "alpha-3": "MDV",
        "country-code": "462",
        "iso_3166-2": "ISO 3166-2:MV",
        "name": "Maldives",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "MW": {
        "alpha-2": "MW",
        "alpha-3": "MWI",
        "country-code": "454",
        "iso_3166-2": "ISO 3166-2:MW",
        "name": "Malawi",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "MX": {
        "alpha-2": "MX",
        "alpha-3": "MEX",
        "country-code": "484",
        "iso_3166-2": "ISO 3166-2:MX",
        "name": "Mexico",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "MY": {
        "alpha-2": "MY",
        "alpha-3": "MYS",
        "country-code": "458",
        "iso_3166-2": "ISO 3166-2:MY",
        "name": "Malaysia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "MZ": {
        "alpha-2": "MZ",
        "alpha-3": "MOZ",
        "country-code": "508",
        "iso_3166-2": "ISO 3166-2:MZ",
        "name": "Mozambique",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "NA": {
        "alpha-2": "NA",
        "alpha-3": "NAM",
        "country-code": "516",
        "iso_3166-2": "ISO 3166-2:NA",
        "name": "Namibia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Southern Africa",
        "sub-region-code": "018"
    },
    "NC": {
        "alpha-2": "NC",
        "alpha-3": "NCL",
        "country-code": "540",
        "iso_3166-2": "ISO 3166-2:NC",
        "name": "New Caledonia",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Melanesia",
        "sub-region-code": "054"
    },
    "NE": {
        "alpha-2": "NE",
        "alpha-3": "NER",
        "country-code": "562",
        "iso_3166-2": "ISO 3166-2:NE",
        "name": "Niger",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "NF": {
        "alpha-2": "NF",
        "alpha-3": "NFK",
        "country-code": "574",
        "iso_3166-2": "ISO 3166-2:NF",
        "name": "Norfolk Island",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Australia and New Zealand",
        "sub-region-code": "053"
    },
    "NG": {
        "alpha-2": "NG",
        "alpha-3": "NGA",
        "country-code": "566",
        "iso_3166-2": "ISO 3166-2:NG",
        "name": "Nigeria",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "NI": {
        "alpha-2": "NI",
        "alpha-3": "NIC",
        "country-code": "558",
        "iso_3166-2": "ISO 3166-2:NI",
        "name": "Nicaragua",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "NL": {
        "alpha-2": "NL",
        "alpha-3": "NLD",
        "country-code": "528",
        "iso_3166-2": "ISO 3166-2:NL",
        "name": "Netherlands",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "NO": {
        "alpha-2": "NO",
        "alpha-3": "NOR",
        "country-code": "578",
        "iso_3166-2": "ISO 3166-2:NO",
        "name": "Norway",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "NP": {
        "alpha-2": "NP",
        "alpha-3": "NPL",
        "country-code": "524",
        "iso_3166-2": "ISO 3166-2:NP",
        "name": "Nepal",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "NR": {
        "alpha-2": "NR",
        "alpha-3": "NRU",
        "country-code": "520",
        "iso_3166-2": "ISO 3166-2:NR",
        "name": "Nauru",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "NU": {
        "alpha-2": "NU",
        "alpha-3": "NIU",
        "country-code": "570",
        "iso_3166-2": "ISO 3166-2:NU",
        "name": "Niue",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "NZ": {
        "alpha-2": "NZ",
        "alpha-3": "NZL",
        "country-code": "554",
        "iso_3166-2": "ISO 3166-2:NZ",
        "name": "New Zealand",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Australia and New Zealand",
        "sub-region-code": "053"
    },
    "OM": {
        "alpha-2": "OM",
        "alpha-3": "OMN",
        "country-code": "512",
        "iso_3166-2": "ISO 3166-2:OM",
        "name": "Oman",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "PA": {
        "alpha-2": "PA",
        "alpha-3": "PAN",
        "country-code": "591",
        "iso_3166-2": "ISO 3166-2:PA",
        "name": "Panama",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "PE": {
        "alpha-2": "PE",
        "alpha-3": "PER",
        "country-code": "604",
        "iso_3166-2": "ISO 3166-2:PE",
        "name": "Peru",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "PF": {
        "alpha-2": "PF",
        "alpha-3": "PYF",
        "country-code": "258",
        "iso_3166-2": "ISO 3166-2:PF",
        "name": "French Polynesia",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "PG": {
        "alpha-2": "PG",
        "alpha-3": "PNG",
        "country-code": "598",
        "iso_3166-2": "ISO 3166-2:PG",
        "name": "Papua New Guinea",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Melanesia",
        "sub-region-code": "054"
    },
    "PH": {
        "alpha-2": "PH",
        "alpha-3": "PHL",
        "country-code": "608",
        "iso_3166-2": "ISO 3166-2:PH",
        "name": "Philippines",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "PK": {
        "alpha-2": "PK",
        "alpha-3": "PAK",
        "country-code": "586",
        "iso_3166-2": "ISO 3166-2:PK",
        "name": "Pakistan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "PL": {
        "alpha-2": "PL",
        "alpha-3": "POL",
        "country-code": "616",
        "iso_3166-2": "ISO 3166-2:PL",
        "name": "Poland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "PM": {
        "alpha-2": "PM",
        "alpha-3": "SPM",
        "country-code": "666",
        "iso_3166-2": "ISO 3166-2:PM",
        "name": "Saint Pierre and Miquelon",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Northern America",
        "sub-region-code": "021"
    },
    "PN": {
        "alpha-2": "PN",
        "alpha-3": "PCN",
        "country-code": "612",
        "iso_3166-2": "ISO 3166-2:PN",
        "name": "Pitcairn",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "PR": {
        "alpha-2": "PR",
        "alpha-3": "PRI",
        "country-code": "630",
        "iso_3166-2": "ISO 3166-2:PR",
        "name": "Puerto Rico",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "PS": {
        "alpha-2": "PS",
        "alpha-3": "PSE",
        "country-code": "275",
        "iso_3166-2": "ISO 3166-2:PS",
        "name": "Palestine, State of",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "PT": {
        "alpha-2": "PT",
        "alpha-3": "PRT",
        "country-code": "620",
        "iso_3166-2": "ISO 3166-2:PT",
        "name": "Portugal",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "PW": {
        "alpha-2": "PW",
        "alpha-3": "PLW",
        "country-code": "585",
        "iso_3166-2": "ISO 3166-2:PW",
        "name": "Palau",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "PY": {
        "alpha-2": "PY",
        "alpha-3": "PRY",
        "country-code": "600",
        "iso_3166-2": "ISO 3166-2:PY",
        "name": "Paraguay",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "QA": {
        "alpha-2": "QA",
        "alpha-3": "QAT",
        "country-code": "634",
        "iso_3166-2": "ISO 3166-2:QA",
        "name": "Qatar",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "RE": {
        "alpha-2": "RE",
        "alpha-3": "REU",
        "country-code": "638",
        "iso_3166-2": "ISO 3166-2:RE",
        "name": "R\u00e9union",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "RO": {
        "alpha-2": "RO",
        "alpha-3": "ROU",
        "country-code": "642",
        "iso_3166-2": "ISO 3166-2:RO",
        "name": "Romania",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "RS": {
        "alpha-2": "RS",
        "alpha-3": "SRB",
        "country-code": "688",
        "iso_3166-2": "ISO 3166-2:RS",
        "name": "Serbia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "RU": {
        "alpha-2": "RU",
        "alpha-3": "RUS",
        "country-code": "643",
        "iso_3166-2": "ISO 3166-2:RU",
        "name": "Russian Federation",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "RW": {
        "alpha-2": "RW",
        "alpha-3": "RWA",
        "country-code": "646",
        "iso_3166-2": "ISO 3166-2:RW",
        "name": "Rwanda",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "SA": {
        "alpha-2": "SA",
        "alpha-3": "SAU",
        "country-code": "682",
        "iso_3166-2": "ISO 3166-2:SA",
        "name": "Saudi Arabia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "SB": {
        "alpha-2": "SB",
        "alpha-3": "SLB",
        "country-code": "090",
        "iso_3166-2": "ISO 3166-2:SB",
        "name": "Solomon Islands",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Melanesia",
        "sub-region-code": "054"
    },
    "SC": {
        "alpha-2": "SC",
        "alpha-3": "SYC",
        "country-code": "690",
        "iso_3166-2": "ISO 3166-2:SC",
        "name": "Seychelles",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "SD": {
        "alpha-2": "SD",
        "alpha-3": "SDN",
        "country-code": "729",
        "iso_3166-2": "ISO 3166-2:SD",
        "name": "Sudan",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "SE": {
        "alpha-2": "SE",
        "alpha-3": "SWE",
        "country-code": "752",
        "iso_3166-2": "ISO 3166-2:SE",
        "name": "Sweden",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "SG": {
        "alpha-2": "SG",
        "alpha-3": "SGP",
        "country-code": "702",
        "iso_3166-2": "ISO 3166-2:SG",
        "name": "Singapore",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "SH": {
        "alpha-2": "SH",
        "alpha-3": "SHN",
        "country-code": "654",
        "iso_3166-2": "ISO 3166-2:SH",
        "name": "Saint Helena, Ascension and Tristan da Cunha",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "SI": {
        "alpha-2": "SI",
        "alpha-3": "SVN",
        "country-code": "705",
        "iso_3166-2": "ISO 3166-2:SI",
        "name": "Slovenia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "SJ": {
        "alpha-2": "SJ",
        "alpha-3": "SJM",
        "country-code": "744",
        "iso_3166-2": "ISO 3166-2:SJ",
        "name": "Svalbard and Jan Mayen",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "SK": {
        "alpha-2": "SK",
        "alpha-3": "SVK",
        "country-code": "703",
        "iso_3166-2": "ISO 3166-2:SK",
        "name": "Slovakia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "SL": {
        "alpha-2": "SL",
        "alpha-3": "SLE",
        "country-code": "694",
        "iso_3166-2": "ISO 3166-2:SL",
        "name": "Sierra Leone",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "SM": {
        "alpha-2": "SM",
        "alpha-3": "SMR",
        "country-code": "674",
        "iso_3166-2": "ISO 3166-2:SM",
        "name": "San Marino",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "SN": {
        "alpha-2": "SN",
        "alpha-3": "SEN",
        "country-code": "686",
        "iso_3166-2": "ISO 3166-2:SN",
        "name": "Senegal",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "SO": {
        "alpha-2": "SO",
        "alpha-3": "SOM",
        "country-code": "706",
        "iso_3166-2": "ISO 3166-2:SO",
        "name": "Somalia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "SR": {
        "alpha-2": "SR",
        "alpha-3": "SUR",
        "country-code": "740",
        "iso_3166-2": "ISO 3166-2:SR",
        "name": "Suriname",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "SS": {
        "alpha-2": "SS",
        "alpha-3": "SSD",
        "country-code": "728",
        "iso_3166-2": "ISO 3166-2:SS",
        "name": "South Sudan",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "ST": {
        "alpha-2": "ST",
        "alpha-3": "STP",
        "country-code": "678",
        "iso_3166-2": "ISO 3166-2:ST",
        "name": "Sao Tome and Principe",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "SV": {
        "alpha-2": "SV",
        "alpha-3": "SLV",
        "country-code": "222",
        "iso_3166-2": "ISO 3166-2:SV",
        "name": "El Salvador",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "SX": {
        "alpha-2": "SX",
        "alpha-3": "SXM",
        "country-code": "534",
        "iso_3166-2": "ISO 3166-2:SX",
        "name": "Sint Maarten (Dutch part)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "SY": {
        "alpha-2": "SY",
        "alpha-3": "SYR",
        "country-code": "760",
        "iso_3166-2": "ISO 3166-2:SY",
        "name": "Syrian Arab Republic",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "SZ": {
        "alpha-2": "SZ",
        "alpha-3": "SWZ",
        "country-code": "748",
        "iso_3166-2": "ISO 3166-2:SZ",
        "name": "Swaziland",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Southern Africa",
        "sub-region-code": "018"
    },
    "TC": {
        "alpha-2": "TC",
        "alpha-3": "TCA",
        "country-code": "796",
        "iso_3166-2": "ISO 3166-2:TC",
        "name": "Turks and Caicos Islands",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "TD": {
        "alpha-2": "TD",
        "alpha-3": "TCD",
        "country-code": "148",
        "iso_3166-2": "ISO 3166-2:TD",
        "name": "Chad",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "TF": {
        "alpha-2": "TF",
        "alpha-3": "ATF",
        "country-code": "260",
        "iso_3166-2": "ISO 3166-2:TF",
        "name": "French Southern Territories",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "TG": {
        "alpha-2": "TG",
        "alpha-3": "TGO",
        "country-code": "768",
        "iso_3166-2": "ISO 3166-2:TG",
        "name": "Togo",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "TH": {
        "alpha-2": "TH",
        "alpha-3": "THA",
        "country-code": "764",
        "iso_3166-2": "ISO 3166-2:TH",
        "name": "Thailand",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "TJ": {
        "alpha-2": "TJ",
        "alpha-3": "TJK",
        "country-code": "762",
        "iso_3166-2": "ISO 3166-2:TJ",
        "name": "Tajikistan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Central Asia",
        "sub-region-code": "143"
    },
    "TK": {
        "alpha-2": "TK",
        "alpha-3": "TKL",
        "country-code": "772",
        "iso_3166-2": "ISO 3166-2:TK",
        "name": "Tokelau",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "TL": {
        "alpha-2": "TL",
        "alpha-3": "TLS",
        "country-code": "626",
        "iso_3166-2": "ISO 3166-2:TL",
        "name": "Timor-Leste",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "TM": {
        "alpha-2": "TM",
        "alpha-3": "TKM",
        "country-code": "795",
        "iso_3166-2": "ISO 3166-2:TM",
        "name": "Turkmenistan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Central Asia",
        "sub-region-code": "143"
    },
    "TN": {
        "alpha-2": "TN",
        "alpha-3": "TUN",
        "country-code": "788",
        "iso_3166-2": "ISO 3166-2:TN",
        "name": "Tunisia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "TO": {
        "alpha-2": "TO",
        "alpha-3": "TON",
        "country-code": "776",
        "iso_3166-2": "ISO 3166-2:TO",
        "name": "Tonga",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "TR": {
        "alpha-2": "TR",
        "alpha-3": "TUR",
        "country-code": "792",
        "iso_3166-2": "ISO 3166-2:TR",
        "name": "Turkey",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "TT": {
        "alpha-2": "TT",
        "alpha-3": "TTO",
        "country-code": "780",
        "iso_3166-2": "ISO 3166-2:TT",
        "name": "Trinidad and Tobago",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "TV": {
        "alpha-2": "TV",
        "alpha-3": "TUV",
        "country-code": "798",
        "iso_3166-2": "ISO 3166-2:TV",
        "name": "Tuvalu",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "TW": {
        "alpha-2": "TW",
        "alpha-3": "TWN",
        "country-code": "158",
        "iso_3166-2": "ISO 3166-2:TW",
        "name": "Taiwan, Province of China",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "TZ": {
        "alpha-2": "TZ",
        "alpha-3": "TZA",
        "country-code": "834",
        "iso_3166-2": "ISO 3166-2:TZ",
        "name": "Tanzania, United Republic of",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "UA": {
        "alpha-2": "UA",
        "alpha-3": "UKR",
        "country-code": "804",
        "iso_3166-2": "ISO 3166-2:UA",
        "name": "Ukraine",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "UG": {
        "alpha-2": "UG",
        "alpha-3": "UGA",
        "country-code": "800",
        "iso_3166-2": "ISO 3166-2:UG",
        "name": "Uganda",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "UM": {
        "alpha-2": "UM",
        "alpha-3": "UMI",
        "country-code": "581",
        "iso_3166-2": "ISO 3166-2:UM",
        "name": "United States Minor Outlying Islands",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "US": {
        "alpha-2": "US",
        "alpha-3": "USA",
        "country-code": "840",
        "iso_3166-2": "ISO 3166-2:US",
        "name": "United States of America",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Northern America",
        "sub-region-code": "021"
    },
    "UY": {
        "alpha-2": "UY",
        "alpha-3": "URY",
        "country-code": "858",
        "iso_3166-2": "ISO 3166-2:UY",
        "name": "Uruguay",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "UZ": {
        "alpha-2": "UZ",
        "alpha-3": "UZB",
        "country-code": "860",
        "iso_3166-2": "ISO 3166-2:UZ",
        "name": "Uzbekistan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Central Asia",
        "sub-region-code": "143"
    },
    "VA": {
        "alpha-2": "VA",
        "alpha-3": "VAT",
        "country-code": "336",
        "iso_3166-2": "ISO 3166-2:VA",
        "name": "Holy See",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "VC": {
        "alpha-2": "VC",
        "alpha-3": "VCT",
        "country-code": "670",
        "iso_3166-2": "ISO 3166-2:VC",
        "name": "Saint Vincent and the Grenadines",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "VE": {
        "alpha-2": "VE",
        "alpha-3": "VEN",
        "country-code": "862",
        "iso_3166-2": "ISO 3166-2:VE",
        "name": "Venezuela (Bolivarian Republic of)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "VG": {
        "alpha-2": "VG",
        "alpha-3": "VGB",
        "country-code": "092",
        "iso_3166-2": "ISO 3166-2:VG",
        "name": "Virgin Islands (British)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "VI": {
        "alpha-2": "VI",
        "alpha-3": "VIR",
        "country-code": "850",
        "iso_3166-2": "ISO 3166-2:VI",
        "name": "Virgin Islands (U.S.)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "VN": {
        "alpha-2": "VN",
        "alpha-3": "VNM",
        "country-code": "704",
        "iso_3166-2": "ISO 3166-2:VN",
        "name": "Viet Nam",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "VU": {
        "alpha-2": "VU",
        "alpha-3": "VUT",
        "country-code": "548",
        "iso_3166-2": "ISO 3166-2:VU",
        "name": "Vanuatu",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Melanesia",
        "sub-region-code": "054"
    },
    "WF": {
        "alpha-2": "WF",
        "alpha-3": "WLF",
        "country-code": "876",
        "iso_3166-2": "ISO 3166-2:WF",
        "name": "Wallis and Futuna",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "WS": {
        "alpha-2": "WS",
        "alpha-3": "WSM",
        "country-code": "882",
        "iso_3166-2": "ISO 3166-2:WS",
        "name": "Samoa",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "YE": {
        "alpha-2": "YE",
        "alpha-3": "YEM",
        "country-code": "887",
        "iso_3166-2": "ISO 3166-2:YE",
        "name": "Yemen",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "YT": {
        "alpha-2": "YT",
        "alpha-3": "MYT",
        "country-code": "175",
        "iso_3166-2": "ISO 3166-2:YT",
        "name": "Mayotte",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "ZA": {
        "alpha-2": "ZA",
        "alpha-3": "ZAF",
        "country-code": "710",
        "iso_3166-2": "ISO 3166-2:ZA",
        "name": "South Africa",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Southern Africa",
        "sub-region-code": "018"
    },
    "ZM": {
        "alpha-2": "ZM",
        "alpha-3": "ZMB",
        "country-code": "894",
        "iso_3166-2": "ISO 3166-2:ZM",
        "name": "Zambia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "ZW": {
        "alpha-2": "ZW",
        "alpha-3": "ZWE",
        "country-code": "716",
        "iso_3166-2": "ISO 3166-2:ZW",
        "name": "Zimbabwe",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    }
}

COUNTRY_INFO_BY_NAME = {
    "Afghanistan": {
        "alpha-2": "AF",
        "alpha-3": "AFG",
        "country-code": "004",
        "iso_3166-2": "ISO 3166-2:AF",
        "name": "Afghanistan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "Albania": {
        "alpha-2": "AL",
        "alpha-3": "ALB",
        "country-code": "008",
        "iso_3166-2": "ISO 3166-2:AL",
        "name": "Albania",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Algeria": {
        "alpha-2": "DZ",
        "alpha-3": "DZA",
        "country-code": "012",
        "iso_3166-2": "ISO 3166-2:DZ",
        "name": "Algeria",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "American Samoa": {
        "alpha-2": "AS",
        "alpha-3": "ASM",
        "country-code": "016",
        "iso_3166-2": "ISO 3166-2:AS",
        "name": "American Samoa",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "Andorra": {
        "alpha-2": "AD",
        "alpha-3": "AND",
        "country-code": "020",
        "iso_3166-2": "ISO 3166-2:AD",
        "name": "Andorra",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Angola": {
        "alpha-2": "AO",
        "alpha-3": "AGO",
        "country-code": "024",
        "iso_3166-2": "ISO 3166-2:AO",
        "name": "Angola",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "Anguilla": {
        "alpha-2": "AI",
        "alpha-3": "AIA",
        "country-code": "660",
        "iso_3166-2": "ISO 3166-2:AI",
        "name": "Anguilla",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Antarctica": {
        "alpha-2": "AQ",
        "alpha-3": "ATA",
        "country-code": "010",
        "iso_3166-2": "ISO 3166-2:AQ",
        "name": "Antarctica",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "Antigua and Barbuda": {
        "alpha-2": "AG",
        "alpha-3": "ATG",
        "country-code": "028",
        "iso_3166-2": "ISO 3166-2:AG",
        "name": "Antigua and Barbuda",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Argentina": {
        "alpha-2": "AR",
        "alpha-3": "ARG",
        "country-code": "032",
        "iso_3166-2": "ISO 3166-2:AR",
        "name": "Argentina",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Armenia": {
        "alpha-2": "AM",
        "alpha-3": "ARM",
        "country-code": "051",
        "iso_3166-2": "ISO 3166-2:AM",
        "name": "Armenia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Aruba": {
        "alpha-2": "AW",
        "alpha-3": "ABW",
        "country-code": "533",
        "iso_3166-2": "ISO 3166-2:AW",
        "name": "Aruba",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Australia": {
        "alpha-2": "AU",
        "alpha-3": "AUS",
        "country-code": "036",
        "iso_3166-2": "ISO 3166-2:AU",
        "name": "Australia",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Australia and New Zealand",
        "sub-region-code": "053"
    },
    "Austria": {
        "alpha-2": "AT",
        "alpha-3": "AUT",
        "country-code": "040",
        "iso_3166-2": "ISO 3166-2:AT",
        "name": "Austria",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "Azerbaijan": {
        "alpha-2": "AZ",
        "alpha-3": "AZE",
        "country-code": "031",
        "iso_3166-2": "ISO 3166-2:AZ",
        "name": "Azerbaijan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Bahamas": {
        "alpha-2": "BS",
        "alpha-3": "BHS",
        "country-code": "044",
        "iso_3166-2": "ISO 3166-2:BS",
        "name": "Bahamas",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Bahrain": {
        "alpha-2": "BH",
        "alpha-3": "BHR",
        "country-code": "048",
        "iso_3166-2": "ISO 3166-2:BH",
        "name": "Bahrain",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Bangladesh": {
        "alpha-2": "BD",
        "alpha-3": "BGD",
        "country-code": "050",
        "iso_3166-2": "ISO 3166-2:BD",
        "name": "Bangladesh",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "Barbados": {
        "alpha-2": "BB",
        "alpha-3": "BRB",
        "country-code": "052",
        "iso_3166-2": "ISO 3166-2:BB",
        "name": "Barbados",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Belarus": {
        "alpha-2": "BY",
        "alpha-3": "BLR",
        "country-code": "112",
        "iso_3166-2": "ISO 3166-2:BY",
        "name": "Belarus",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "Belgium": {
        "alpha-2": "BE",
        "alpha-3": "BEL",
        "country-code": "056",
        "iso_3166-2": "ISO 3166-2:BE",
        "name": "Belgium",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "Belize": {
        "alpha-2": "BZ",
        "alpha-3": "BLZ",
        "country-code": "084",
        "iso_3166-2": "ISO 3166-2:BZ",
        "name": "Belize",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "Benin": {
        "alpha-2": "BJ",
        "alpha-3": "BEN",
        "country-code": "204",
        "iso_3166-2": "ISO 3166-2:BJ",
        "name": "Benin",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Bermuda": {
        "alpha-2": "BM",
        "alpha-3": "BMU",
        "country-code": "060",
        "iso_3166-2": "ISO 3166-2:BM",
        "name": "Bermuda",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Northern America",
        "sub-region-code": "021"
    },
    "Bhutan": {
        "alpha-2": "BT",
        "alpha-3": "BTN",
        "country-code": "064",
        "iso_3166-2": "ISO 3166-2:BT",
        "name": "Bhutan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "Bolivia (Plurinational State of)": {
        "alpha-2": "BO",
        "alpha-3": "BOL",
        "country-code": "068",
        "iso_3166-2": "ISO 3166-2:BO",
        "name": "Bolivia (Plurinational State of)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Bonaire, Sint Eustatius and Saba": {
        "alpha-2": "BQ",
        "alpha-3": "BES",
        "country-code": "535",
        "iso_3166-2": "ISO 3166-2:BQ",
        "name": "Bonaire, Sint Eustatius and Saba",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Bosnia and Herzegovina": {
        "alpha-2": "BA",
        "alpha-3": "BIH",
        "country-code": "070",
        "iso_3166-2": "ISO 3166-2:BA",
        "name": "Bosnia and Herzegovina",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Botswana": {
        "alpha-2": "BW",
        "alpha-3": "BWA",
        "country-code": "072",
        "iso_3166-2": "ISO 3166-2:BW",
        "name": "Botswana",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Southern Africa",
        "sub-region-code": "018"
    },
    "Bouvet Island": {
        "alpha-2": "BV",
        "alpha-3": "BVT",
        "country-code": "074",
        "iso_3166-2": "ISO 3166-2:BV",
        "name": "Bouvet Island",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "Brazil": {
        "alpha-2": "BR",
        "alpha-3": "BRA",
        "country-code": "076",
        "iso_3166-2": "ISO 3166-2:BR",
        "name": "Brazil",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "British Indian Ocean Territory": {
        "alpha-2": "IO",
        "alpha-3": "IOT",
        "country-code": "086",
        "iso_3166-2": "ISO 3166-2:IO",
        "name": "British Indian Ocean Territory",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "Brunei Darussalam": {
        "alpha-2": "BN",
        "alpha-3": "BRN",
        "country-code": "096",
        "iso_3166-2": "ISO 3166-2:BN",
        "name": "Brunei Darussalam",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Bulgaria": {
        "alpha-2": "BG",
        "alpha-3": "BGR",
        "country-code": "100",
        "iso_3166-2": "ISO 3166-2:BG",
        "name": "Bulgaria",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "Burkina Faso": {
        "alpha-2": "BF",
        "alpha-3": "BFA",
        "country-code": "854",
        "iso_3166-2": "ISO 3166-2:BF",
        "name": "Burkina Faso",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Burundi": {
        "alpha-2": "BI",
        "alpha-3": "BDI",
        "country-code": "108",
        "iso_3166-2": "ISO 3166-2:BI",
        "name": "Burundi",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Cabo Verde": {
        "alpha-2": "CV",
        "alpha-3": "CPV",
        "country-code": "132",
        "iso_3166-2": "ISO 3166-2:CV",
        "name": "Cabo Verde",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Cambodia": {
        "alpha-2": "KH",
        "alpha-3": "KHM",
        "country-code": "116",
        "iso_3166-2": "ISO 3166-2:KH",
        "name": "Cambodia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Cameroon": {
        "alpha-2": "CM",
        "alpha-3": "CMR",
        "country-code": "120",
        "iso_3166-2": "ISO 3166-2:CM",
        "name": "Cameroon",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "Canada": {
        "alpha-2": "CA",
        "alpha-3": "CAN",
        "country-code": "124",
        "iso_3166-2": "ISO 3166-2:CA",
        "name": "Canada",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Northern America",
        "sub-region-code": "021"
    },
    "Cayman Islands": {
        "alpha-2": "KY",
        "alpha-3": "CYM",
        "country-code": "136",
        "iso_3166-2": "ISO 3166-2:KY",
        "name": "Cayman Islands",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Central African Republic": {
        "alpha-2": "CF",
        "alpha-3": "CAF",
        "country-code": "140",
        "iso_3166-2": "ISO 3166-2:CF",
        "name": "Central African Republic",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "Chad": {
        "alpha-2": "TD",
        "alpha-3": "TCD",
        "country-code": "148",
        "iso_3166-2": "ISO 3166-2:TD",
        "name": "Chad",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "Chile": {
        "alpha-2": "CL",
        "alpha-3": "CHL",
        "country-code": "152",
        "iso_3166-2": "ISO 3166-2:CL",
        "name": "Chile",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "China": {
        "alpha-2": "CN",
        "alpha-3": "CHN",
        "country-code": "156",
        "iso_3166-2": "ISO 3166-2:CN",
        "name": "China",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "Christmas Island": {
        "alpha-2": "CX",
        "alpha-3": "CXR",
        "country-code": "162",
        "iso_3166-2": "ISO 3166-2:CX",
        "name": "Christmas Island",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "Cocos (Keeling) Islands": {
        "alpha-2": "CC",
        "alpha-3": "CCK",
        "country-code": "166",
        "iso_3166-2": "ISO 3166-2:CC",
        "name": "Cocos (Keeling) Islands",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "Colombia": {
        "alpha-2": "CO",
        "alpha-3": "COL",
        "country-code": "170",
        "iso_3166-2": "ISO 3166-2:CO",
        "name": "Colombia",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Comoros": {
        "alpha-2": "KM",
        "alpha-3": "COM",
        "country-code": "174",
        "iso_3166-2": "ISO 3166-2:KM",
        "name": "Comoros",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Congo": {
        "alpha-2": "CG",
        "alpha-3": "COG",
        "country-code": "178",
        "iso_3166-2": "ISO 3166-2:CG",
        "name": "Congo",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "Congo (Democratic Republic of the)": {
        "alpha-2": "CD",
        "alpha-3": "COD",
        "country-code": "180",
        "iso_3166-2": "ISO 3166-2:CD",
        "name": "Congo (Democratic Republic of the)",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "Cook Islands": {
        "alpha-2": "CK",
        "alpha-3": "COK",
        "country-code": "184",
        "iso_3166-2": "ISO 3166-2:CK",
        "name": "Cook Islands",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "Costa Rica": {
        "alpha-2": "CR",
        "alpha-3": "CRI",
        "country-code": "188",
        "iso_3166-2": "ISO 3166-2:CR",
        "name": "Costa Rica",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "Croatia": {
        "alpha-2": "HR",
        "alpha-3": "HRV",
        "country-code": "191",
        "iso_3166-2": "ISO 3166-2:HR",
        "name": "Croatia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Cuba": {
        "alpha-2": "CU",
        "alpha-3": "CUB",
        "country-code": "192",
        "iso_3166-2": "ISO 3166-2:CU",
        "name": "Cuba",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Cura\u00e7ao": {
        "alpha-2": "CW",
        "alpha-3": "CUW",
        "country-code": "531",
        "iso_3166-2": "ISO 3166-2:CW",
        "name": "Cura\u00e7ao",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Cyprus": {
        "alpha-2": "CY",
        "alpha-3": "CYP",
        "country-code": "196",
        "iso_3166-2": "ISO 3166-2:CY",
        "name": "Cyprus",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Czech Republic": {
        "alpha-2": "CZ",
        "alpha-3": "CZE",
        "country-code": "203",
        "iso_3166-2": "ISO 3166-2:CZ",
        "name": "Czech Republic",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "C\u00f4te d'Ivoire": {
        "alpha-2": "CI",
        "alpha-3": "CIV",
        "country-code": "384",
        "iso_3166-2": "ISO 3166-2:CI",
        "name": "C\u00f4te d'Ivoire",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Denmark": {
        "alpha-2": "DK",
        "alpha-3": "DNK",
        "country-code": "208",
        "iso_3166-2": "ISO 3166-2:DK",
        "name": "Denmark",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Djibouti": {
        "alpha-2": "DJ",
        "alpha-3": "DJI",
        "country-code": "262",
        "iso_3166-2": "ISO 3166-2:DJ",
        "name": "Djibouti",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Dominica": {
        "alpha-2": "DM",
        "alpha-3": "DMA",
        "country-code": "212",
        "iso_3166-2": "ISO 3166-2:DM",
        "name": "Dominica",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Dominican Republic": {
        "alpha-2": "DO",
        "alpha-3": "DOM",
        "country-code": "214",
        "iso_3166-2": "ISO 3166-2:DO",
        "name": "Dominican Republic",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Ecuador": {
        "alpha-2": "EC",
        "alpha-3": "ECU",
        "country-code": "218",
        "iso_3166-2": "ISO 3166-2:EC",
        "name": "Ecuador",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Egypt": {
        "alpha-2": "EG",
        "alpha-3": "EGY",
        "country-code": "818",
        "iso_3166-2": "ISO 3166-2:EG",
        "name": "Egypt",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "El Salvador": {
        "alpha-2": "SV",
        "alpha-3": "SLV",
        "country-code": "222",
        "iso_3166-2": "ISO 3166-2:SV",
        "name": "El Salvador",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "Equatorial Guinea": {
        "alpha-2": "GQ",
        "alpha-3": "GNQ",
        "country-code": "226",
        "iso_3166-2": "ISO 3166-2:GQ",
        "name": "Equatorial Guinea",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "Eritrea": {
        "alpha-2": "ER",
        "alpha-3": "ERI",
        "country-code": "232",
        "iso_3166-2": "ISO 3166-2:ER",
        "name": "Eritrea",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Estonia": {
        "alpha-2": "EE",
        "alpha-3": "EST",
        "country-code": "233",
        "iso_3166-2": "ISO 3166-2:EE",
        "name": "Estonia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Ethiopia": {
        "alpha-2": "ET",
        "alpha-3": "ETH",
        "country-code": "231",
        "iso_3166-2": "ISO 3166-2:ET",
        "name": "Ethiopia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Falkland Islands (Malvinas)": {
        "alpha-2": "FK",
        "alpha-3": "FLK",
        "country-code": "238",
        "iso_3166-2": "ISO 3166-2:FK",
        "name": "Falkland Islands (Malvinas)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Faroe Islands": {
        "alpha-2": "FO",
        "alpha-3": "FRO",
        "country-code": "234",
        "iso_3166-2": "ISO 3166-2:FO",
        "name": "Faroe Islands",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Fiji": {
        "alpha-2": "FJ",
        "alpha-3": "FJI",
        "country-code": "242",
        "iso_3166-2": "ISO 3166-2:FJ",
        "name": "Fiji",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Melanesia",
        "sub-region-code": "054"
    },
    "Finland": {
        "alpha-2": "FI",
        "alpha-3": "FIN",
        "country-code": "246",
        "iso_3166-2": "ISO 3166-2:FI",
        "name": "Finland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "France": {
        "alpha-2": "FR",
        "alpha-3": "FRA",
        "country-code": "250",
        "iso_3166-2": "ISO 3166-2:FR",
        "name": "France",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "French Guiana": {
        "alpha-2": "GF",
        "alpha-3": "GUF",
        "country-code": "254",
        "iso_3166-2": "ISO 3166-2:GF",
        "name": "French Guiana",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "French Polynesia": {
        "alpha-2": "PF",
        "alpha-3": "PYF",
        "country-code": "258",
        "iso_3166-2": "ISO 3166-2:PF",
        "name": "French Polynesia",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "French Southern Territories": {
        "alpha-2": "TF",
        "alpha-3": "ATF",
        "country-code": "260",
        "iso_3166-2": "ISO 3166-2:TF",
        "name": "French Southern Territories",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "Gabon": {
        "alpha-2": "GA",
        "alpha-3": "GAB",
        "country-code": "266",
        "iso_3166-2": "ISO 3166-2:GA",
        "name": "Gabon",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "Gambia": {
        "alpha-2": "GM",
        "alpha-3": "GMB",
        "country-code": "270",
        "iso_3166-2": "ISO 3166-2:GM",
        "name": "Gambia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Georgia": {
        "alpha-2": "GE",
        "alpha-3": "GEO",
        "country-code": "268",
        "iso_3166-2": "ISO 3166-2:GE",
        "name": "Georgia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Germany": {
        "alpha-2": "DE",
        "alpha-3": "DEU",
        "country-code": "276",
        "iso_3166-2": "ISO 3166-2:DE",
        "name": "Germany",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "Ghana": {
        "alpha-2": "GH",
        "alpha-3": "GHA",
        "country-code": "288",
        "iso_3166-2": "ISO 3166-2:GH",
        "name": "Ghana",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Gibraltar": {
        "alpha-2": "GI",
        "alpha-3": "GIB",
        "country-code": "292",
        "iso_3166-2": "ISO 3166-2:GI",
        "name": "Gibraltar",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Greece": {
        "alpha-2": "GR",
        "alpha-3": "GRC",
        "country-code": "300",
        "iso_3166-2": "ISO 3166-2:GR",
        "name": "Greece",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Greenland": {
        "alpha-2": "GL",
        "alpha-3": "GRL",
        "country-code": "304",
        "iso_3166-2": "ISO 3166-2:GL",
        "name": "Greenland",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Northern America",
        "sub-region-code": "021"
    },
    "Grenada": {
        "alpha-2": "GD",
        "alpha-3": "GRD",
        "country-code": "308",
        "iso_3166-2": "ISO 3166-2:GD",
        "name": "Grenada",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Guadeloupe": {
        "alpha-2": "GP",
        "alpha-3": "GLP",
        "country-code": "312",
        "iso_3166-2": "ISO 3166-2:GP",
        "name": "Guadeloupe",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Guam": {
        "alpha-2": "GU",
        "alpha-3": "GUM",
        "country-code": "316",
        "iso_3166-2": "ISO 3166-2:GU",
        "name": "Guam",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "Guatemala": {
        "alpha-2": "GT",
        "alpha-3": "GTM",
        "country-code": "320",
        "iso_3166-2": "ISO 3166-2:GT",
        "name": "Guatemala",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "Guernsey": {
        "alpha-2": "GG",
        "alpha-3": "GGY",
        "country-code": "831",
        "iso_3166-2": "ISO 3166-2:GG",
        "name": "Guernsey",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Guinea": {
        "alpha-2": "GN",
        "alpha-3": "GIN",
        "country-code": "324",
        "iso_3166-2": "ISO 3166-2:GN",
        "name": "Guinea",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Guinea-Bissau": {
        "alpha-2": "GW",
        "alpha-3": "GNB",
        "country-code": "624",
        "iso_3166-2": "ISO 3166-2:GW",
        "name": "Guinea-Bissau",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Guyana": {
        "alpha-2": "GY",
        "alpha-3": "GUY",
        "country-code": "328",
        "iso_3166-2": "ISO 3166-2:GY",
        "name": "Guyana",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Haiti": {
        "alpha-2": "HT",
        "alpha-3": "HTI",
        "country-code": "332",
        "iso_3166-2": "ISO 3166-2:HT",
        "name": "Haiti",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Heard Island and McDonald Islands": {
        "alpha-2": "HM",
        "alpha-3": "HMD",
        "country-code": "334",
        "iso_3166-2": "ISO 3166-2:HM",
        "name": "Heard Island and McDonald Islands",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "Holy See": {
        "alpha-2": "VA",
        "alpha-3": "VAT",
        "country-code": "336",
        "iso_3166-2": "ISO 3166-2:VA",
        "name": "Holy See",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Honduras": {
        "alpha-2": "HN",
        "alpha-3": "HND",
        "country-code": "340",
        "iso_3166-2": "ISO 3166-2:HN",
        "name": "Honduras",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "Hong Kong": {
        "alpha-2": "HK",
        "alpha-3": "HKG",
        "country-code": "344",
        "iso_3166-2": "ISO 3166-2:HK",
        "name": "Hong Kong",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "Hungary": {
        "alpha-2": "HU",
        "alpha-3": "HUN",
        "country-code": "348",
        "iso_3166-2": "ISO 3166-2:HU",
        "name": "Hungary",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "Iceland": {
        "alpha-2": "IS",
        "alpha-3": "ISL",
        "country-code": "352",
        "iso_3166-2": "ISO 3166-2:IS",
        "name": "Iceland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "India": {
        "alpha-2": "IN",
        "alpha-3": "IND",
        "country-code": "356",
        "iso_3166-2": "ISO 3166-2:IN",
        "name": "India",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "Indonesia": {
        "alpha-2": "ID",
        "alpha-3": "IDN",
        "country-code": "360",
        "iso_3166-2": "ISO 3166-2:ID",
        "name": "Indonesia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Iran (Islamic Republic of)": {
        "alpha-2": "IR",
        "alpha-3": "IRN",
        "country-code": "364",
        "iso_3166-2": "ISO 3166-2:IR",
        "name": "Iran (Islamic Republic of)",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "Iraq": {
        "alpha-2": "IQ",
        "alpha-3": "IRQ",
        "country-code": "368",
        "iso_3166-2": "ISO 3166-2:IQ",
        "name": "Iraq",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Ireland": {
        "alpha-2": "IE",
        "alpha-3": "IRL",
        "country-code": "372",
        "iso_3166-2": "ISO 3166-2:IE",
        "name": "Ireland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Isle of Man": {
        "alpha-2": "IM",
        "alpha-3": "IMN",
        "country-code": "833",
        "iso_3166-2": "ISO 3166-2:IM",
        "name": "Isle of Man",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Israel": {
        "alpha-2": "IL",
        "alpha-3": "ISR",
        "country-code": "376",
        "iso_3166-2": "ISO 3166-2:IL",
        "name": "Israel",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Italy": {
        "alpha-2": "IT",
        "alpha-3": "ITA",
        "country-code": "380",
        "iso_3166-2": "ISO 3166-2:IT",
        "name": "Italy",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Jamaica": {
        "alpha-2": "JM",
        "alpha-3": "JAM",
        "country-code": "388",
        "iso_3166-2": "ISO 3166-2:JM",
        "name": "Jamaica",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Japan": {
        "alpha-2": "JP",
        "alpha-3": "JPN",
        "country-code": "392",
        "iso_3166-2": "ISO 3166-2:JP",
        "name": "Japan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "Jersey": {
        "alpha-2": "JE",
        "alpha-3": "JEY",
        "country-code": "832",
        "iso_3166-2": "ISO 3166-2:JE",
        "name": "Jersey",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Jordan": {
        "alpha-2": "JO",
        "alpha-3": "JOR",
        "country-code": "400",
        "iso_3166-2": "ISO 3166-2:JO",
        "name": "Jordan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Kazakhstan": {
        "alpha-2": "KZ",
        "alpha-3": "KAZ",
        "country-code": "398",
        "iso_3166-2": "ISO 3166-2:KZ",
        "name": "Kazakhstan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Central Asia",
        "sub-region-code": "143"
    },
    "Kenya": {
        "alpha-2": "KE",
        "alpha-3": "KEN",
        "country-code": "404",
        "iso_3166-2": "ISO 3166-2:KE",
        "name": "Kenya",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Kiribati": {
        "alpha-2": "KI",
        "alpha-3": "KIR",
        "country-code": "296",
        "iso_3166-2": "ISO 3166-2:KI",
        "name": "Kiribati",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "Korea (Democratic People's Republic of)": {
        "alpha-2": "KP",
        "alpha-3": "PRK",
        "country-code": "408",
        "iso_3166-2": "ISO 3166-2:KP",
        "name": "Korea (Democratic People's Republic of)",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "Korea (Republic of)": {
        "alpha-2": "KR",
        "alpha-3": "KOR",
        "country-code": "410",
        "iso_3166-2": "ISO 3166-2:KR",
        "name": "Korea (Republic of)",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "Kuwait": {
        "alpha-2": "KW",
        "alpha-3": "KWT",
        "country-code": "414",
        "iso_3166-2": "ISO 3166-2:KW",
        "name": "Kuwait",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Kyrgyzstan": {
        "alpha-2": "KG",
        "alpha-3": "KGZ",
        "country-code": "417",
        "iso_3166-2": "ISO 3166-2:KG",
        "name": "Kyrgyzstan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Central Asia",
        "sub-region-code": "143"
    },
    "Lao People's Democratic Republic": {
        "alpha-2": "LA",
        "alpha-3": "LAO",
        "country-code": "418",
        "iso_3166-2": "ISO 3166-2:LA",
        "name": "Lao People's Democratic Republic",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Latvia": {
        "alpha-2": "LV",
        "alpha-3": "LVA",
        "country-code": "428",
        "iso_3166-2": "ISO 3166-2:LV",
        "name": "Latvia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Lebanon": {
        "alpha-2": "LB",
        "alpha-3": "LBN",
        "country-code": "422",
        "iso_3166-2": "ISO 3166-2:LB",
        "name": "Lebanon",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Lesotho": {
        "alpha-2": "LS",
        "alpha-3": "LSO",
        "country-code": "426",
        "iso_3166-2": "ISO 3166-2:LS",
        "name": "Lesotho",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Southern Africa",
        "sub-region-code": "018"
    },
    "Liberia": {
        "alpha-2": "LR",
        "alpha-3": "LBR",
        "country-code": "430",
        "iso_3166-2": "ISO 3166-2:LR",
        "name": "Liberia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Libya": {
        "alpha-2": "LY",
        "alpha-3": "LBY",
        "country-code": "434",
        "iso_3166-2": "ISO 3166-2:LY",
        "name": "Libya",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "Liechtenstein": {
        "alpha-2": "LI",
        "alpha-3": "LIE",
        "country-code": "438",
        "iso_3166-2": "ISO 3166-2:LI",
        "name": "Liechtenstein",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "Lithuania": {
        "alpha-2": "LT",
        "alpha-3": "LTU",
        "country-code": "440",
        "iso_3166-2": "ISO 3166-2:LT",
        "name": "Lithuania",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Luxembourg": {
        "alpha-2": "LU",
        "alpha-3": "LUX",
        "country-code": "442",
        "iso_3166-2": "ISO 3166-2:LU",
        "name": "Luxembourg",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "Macao": {
        "alpha-2": "MO",
        "alpha-3": "MAC",
        "country-code": "446",
        "iso_3166-2": "ISO 3166-2:MO",
        "name": "Macao",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "Macedonia (the former Yugoslav Republic of)": {
        "alpha-2": "MK",
        "alpha-3": "MKD",
        "country-code": "807",
        "iso_3166-2": "ISO 3166-2:MK",
        "name": "Macedonia (the former Yugoslav Republic of)",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Madagascar": {
        "alpha-2": "MG",
        "alpha-3": "MDG",
        "country-code": "450",
        "iso_3166-2": "ISO 3166-2:MG",
        "name": "Madagascar",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Malawi": {
        "alpha-2": "MW",
        "alpha-3": "MWI",
        "country-code": "454",
        "iso_3166-2": "ISO 3166-2:MW",
        "name": "Malawi",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Malaysia": {
        "alpha-2": "MY",
        "alpha-3": "MYS",
        "country-code": "458",
        "iso_3166-2": "ISO 3166-2:MY",
        "name": "Malaysia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Maldives": {
        "alpha-2": "MV",
        "alpha-3": "MDV",
        "country-code": "462",
        "iso_3166-2": "ISO 3166-2:MV",
        "name": "Maldives",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "Mali": {
        "alpha-2": "ML",
        "alpha-3": "MLI",
        "country-code": "466",
        "iso_3166-2": "ISO 3166-2:ML",
        "name": "Mali",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Malta": {
        "alpha-2": "MT",
        "alpha-3": "MLT",
        "country-code": "470",
        "iso_3166-2": "ISO 3166-2:MT",
        "name": "Malta",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Marshall Islands": {
        "alpha-2": "MH",
        "alpha-3": "MHL",
        "country-code": "584",
        "iso_3166-2": "ISO 3166-2:MH",
        "name": "Marshall Islands",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "Martinique": {
        "alpha-2": "MQ",
        "alpha-3": "MTQ",
        "country-code": "474",
        "iso_3166-2": "ISO 3166-2:MQ",
        "name": "Martinique",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Mauritania": {
        "alpha-2": "MR",
        "alpha-3": "MRT",
        "country-code": "478",
        "iso_3166-2": "ISO 3166-2:MR",
        "name": "Mauritania",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Mauritius": {
        "alpha-2": "MU",
        "alpha-3": "MUS",
        "country-code": "480",
        "iso_3166-2": "ISO 3166-2:MU",
        "name": "Mauritius",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Mayotte": {
        "alpha-2": "YT",
        "alpha-3": "MYT",
        "country-code": "175",
        "iso_3166-2": "ISO 3166-2:YT",
        "name": "Mayotte",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Mexico": {
        "alpha-2": "MX",
        "alpha-3": "MEX",
        "country-code": "484",
        "iso_3166-2": "ISO 3166-2:MX",
        "name": "Mexico",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "Micronesia (Federated States of)": {
        "alpha-2": "FM",
        "alpha-3": "FSM",
        "country-code": "583",
        "iso_3166-2": "ISO 3166-2:FM",
        "name": "Micronesia (Federated States of)",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "Moldova (Republic of)": {
        "alpha-2": "MD",
        "alpha-3": "MDA",
        "country-code": "498",
        "iso_3166-2": "ISO 3166-2:MD",
        "name": "Moldova (Republic of)",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "Monaco": {
        "alpha-2": "MC",
        "alpha-3": "MCO",
        "country-code": "492",
        "iso_3166-2": "ISO 3166-2:MC",
        "name": "Monaco",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "Mongolia": {
        "alpha-2": "MN",
        "alpha-3": "MNG",
        "country-code": "496",
        "iso_3166-2": "ISO 3166-2:MN",
        "name": "Mongolia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "Montenegro": {
        "alpha-2": "ME",
        "alpha-3": "MNE",
        "country-code": "499",
        "iso_3166-2": "ISO 3166-2:ME",
        "name": "Montenegro",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Montserrat": {
        "alpha-2": "MS",
        "alpha-3": "MSR",
        "country-code": "500",
        "iso_3166-2": "ISO 3166-2:MS",
        "name": "Montserrat",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Morocco": {
        "alpha-2": "MA",
        "alpha-3": "MAR",
        "country-code": "504",
        "iso_3166-2": "ISO 3166-2:MA",
        "name": "Morocco",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "Mozambique": {
        "alpha-2": "MZ",
        "alpha-3": "MOZ",
        "country-code": "508",
        "iso_3166-2": "ISO 3166-2:MZ",
        "name": "Mozambique",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Myanmar": {
        "alpha-2": "MM",
        "alpha-3": "MMR",
        "country-code": "104",
        "iso_3166-2": "ISO 3166-2:MM",
        "name": "Myanmar",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Namibia": {
        "alpha-2": "NA",
        "alpha-3": "NAM",
        "country-code": "516",
        "iso_3166-2": "ISO 3166-2:NA",
        "name": "Namibia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Southern Africa",
        "sub-region-code": "018"
    },
    "Nauru": {
        "alpha-2": "NR",
        "alpha-3": "NRU",
        "country-code": "520",
        "iso_3166-2": "ISO 3166-2:NR",
        "name": "Nauru",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "Nepal": {
        "alpha-2": "NP",
        "alpha-3": "NPL",
        "country-code": "524",
        "iso_3166-2": "ISO 3166-2:NP",
        "name": "Nepal",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "Netherlands": {
        "alpha-2": "NL",
        "alpha-3": "NLD",
        "country-code": "528",
        "iso_3166-2": "ISO 3166-2:NL",
        "name": "Netherlands",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "New Caledonia": {
        "alpha-2": "NC",
        "alpha-3": "NCL",
        "country-code": "540",
        "iso_3166-2": "ISO 3166-2:NC",
        "name": "New Caledonia",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Melanesia",
        "sub-region-code": "054"
    },
    "New Zealand": {
        "alpha-2": "NZ",
        "alpha-3": "NZL",
        "country-code": "554",
        "iso_3166-2": "ISO 3166-2:NZ",
        "name": "New Zealand",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Australia and New Zealand",
        "sub-region-code": "053"
    },
    "Nicaragua": {
        "alpha-2": "NI",
        "alpha-3": "NIC",
        "country-code": "558",
        "iso_3166-2": "ISO 3166-2:NI",
        "name": "Nicaragua",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "Niger": {
        "alpha-2": "NE",
        "alpha-3": "NER",
        "country-code": "562",
        "iso_3166-2": "ISO 3166-2:NE",
        "name": "Niger",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Nigeria": {
        "alpha-2": "NG",
        "alpha-3": "NGA",
        "country-code": "566",
        "iso_3166-2": "ISO 3166-2:NG",
        "name": "Nigeria",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Niue": {
        "alpha-2": "NU",
        "alpha-3": "NIU",
        "country-code": "570",
        "iso_3166-2": "ISO 3166-2:NU",
        "name": "Niue",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "Norfolk Island": {
        "alpha-2": "NF",
        "alpha-3": "NFK",
        "country-code": "574",
        "iso_3166-2": "ISO 3166-2:NF",
        "name": "Norfolk Island",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Australia and New Zealand",
        "sub-region-code": "053"
    },
    "Northern Mariana Islands": {
        "alpha-2": "MP",
        "alpha-3": "MNP",
        "country-code": "580",
        "iso_3166-2": "ISO 3166-2:MP",
        "name": "Northern Mariana Islands",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "Norway": {
        "alpha-2": "NO",
        "alpha-3": "NOR",
        "country-code": "578",
        "iso_3166-2": "ISO 3166-2:NO",
        "name": "Norway",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Oman": {
        "alpha-2": "OM",
        "alpha-3": "OMN",
        "country-code": "512",
        "iso_3166-2": "ISO 3166-2:OM",
        "name": "Oman",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Pakistan": {
        "alpha-2": "PK",
        "alpha-3": "PAK",
        "country-code": "586",
        "iso_3166-2": "ISO 3166-2:PK",
        "name": "Pakistan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "Palau": {
        "alpha-2": "PW",
        "alpha-3": "PLW",
        "country-code": "585",
        "iso_3166-2": "ISO 3166-2:PW",
        "name": "Palau",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Micronesia",
        "sub-region-code": "057"
    },
    "Palestine, State of": {
        "alpha-2": "PS",
        "alpha-3": "PSE",
        "country-code": "275",
        "iso_3166-2": "ISO 3166-2:PS",
        "name": "Palestine, State of",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Panama": {
        "alpha-2": "PA",
        "alpha-3": "PAN",
        "country-code": "591",
        "iso_3166-2": "ISO 3166-2:PA",
        "name": "Panama",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Central America",
        "sub-region-code": "013"
    },
    "Papua New Guinea": {
        "alpha-2": "PG",
        "alpha-3": "PNG",
        "country-code": "598",
        "iso_3166-2": "ISO 3166-2:PG",
        "name": "Papua New Guinea",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Melanesia",
        "sub-region-code": "054"
    },
    "Paraguay": {
        "alpha-2": "PY",
        "alpha-3": "PRY",
        "country-code": "600",
        "iso_3166-2": "ISO 3166-2:PY",
        "name": "Paraguay",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Peru": {
        "alpha-2": "PE",
        "alpha-3": "PER",
        "country-code": "604",
        "iso_3166-2": "ISO 3166-2:PE",
        "name": "Peru",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Philippines": {
        "alpha-2": "PH",
        "alpha-3": "PHL",
        "country-code": "608",
        "iso_3166-2": "ISO 3166-2:PH",
        "name": "Philippines",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Pitcairn": {
        "alpha-2": "PN",
        "alpha-3": "PCN",
        "country-code": "612",
        "iso_3166-2": "ISO 3166-2:PN",
        "name": "Pitcairn",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "Poland": {
        "alpha-2": "PL",
        "alpha-3": "POL",
        "country-code": "616",
        "iso_3166-2": "ISO 3166-2:PL",
        "name": "Poland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "Portugal": {
        "alpha-2": "PT",
        "alpha-3": "PRT",
        "country-code": "620",
        "iso_3166-2": "ISO 3166-2:PT",
        "name": "Portugal",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Puerto Rico": {
        "alpha-2": "PR",
        "alpha-3": "PRI",
        "country-code": "630",
        "iso_3166-2": "ISO 3166-2:PR",
        "name": "Puerto Rico",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Qatar": {
        "alpha-2": "QA",
        "alpha-3": "QAT",
        "country-code": "634",
        "iso_3166-2": "ISO 3166-2:QA",
        "name": "Qatar",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Romania": {
        "alpha-2": "RO",
        "alpha-3": "ROU",
        "country-code": "642",
        "iso_3166-2": "ISO 3166-2:RO",
        "name": "Romania",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "Russian Federation": {
        "alpha-2": "RU",
        "alpha-3": "RUS",
        "country-code": "643",
        "iso_3166-2": "ISO 3166-2:RU",
        "name": "Russian Federation",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "Rwanda": {
        "alpha-2": "RW",
        "alpha-3": "RWA",
        "country-code": "646",
        "iso_3166-2": "ISO 3166-2:RW",
        "name": "Rwanda",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "R\u00e9union": {
        "alpha-2": "RE",
        "alpha-3": "REU",
        "country-code": "638",
        "iso_3166-2": "ISO 3166-2:RE",
        "name": "R\u00e9union",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Saint Barth\u00e9lemy": {
        "alpha-2": "BL",
        "alpha-3": "BLM",
        "country-code": "652",
        "iso_3166-2": "ISO 3166-2:BL",
        "name": "Saint Barth\u00e9lemy",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Saint Helena, Ascension and Tristan da Cunha": {
        "alpha-2": "SH",
        "alpha-3": "SHN",
        "country-code": "654",
        "iso_3166-2": "ISO 3166-2:SH",
        "name": "Saint Helena, Ascension and Tristan da Cunha",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Saint Kitts and Nevis": {
        "alpha-2": "KN",
        "alpha-3": "KNA",
        "country-code": "659",
        "iso_3166-2": "ISO 3166-2:KN",
        "name": "Saint Kitts and Nevis",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Saint Lucia": {
        "alpha-2": "LC",
        "alpha-3": "LCA",
        "country-code": "662",
        "iso_3166-2": "ISO 3166-2:LC",
        "name": "Saint Lucia",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Saint Martin (French part)": {
        "alpha-2": "MF",
        "alpha-3": "MAF",
        "country-code": "663",
        "iso_3166-2": "ISO 3166-2:MF",
        "name": "Saint Martin (French part)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Saint Pierre and Miquelon": {
        "alpha-2": "PM",
        "alpha-3": "SPM",
        "country-code": "666",
        "iso_3166-2": "ISO 3166-2:PM",
        "name": "Saint Pierre and Miquelon",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Northern America",
        "sub-region-code": "021"
    },
    "Saint Vincent and the Grenadines": {
        "alpha-2": "VC",
        "alpha-3": "VCT",
        "country-code": "670",
        "iso_3166-2": "ISO 3166-2:VC",
        "name": "Saint Vincent and the Grenadines",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Samoa": {
        "alpha-2": "WS",
        "alpha-3": "WSM",
        "country-code": "882",
        "iso_3166-2": "ISO 3166-2:WS",
        "name": "Samoa",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "San Marino": {
        "alpha-2": "SM",
        "alpha-3": "SMR",
        "country-code": "674",
        "iso_3166-2": "ISO 3166-2:SM",
        "name": "San Marino",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Sao Tome and Principe": {
        "alpha-2": "ST",
        "alpha-3": "STP",
        "country-code": "678",
        "iso_3166-2": "ISO 3166-2:ST",
        "name": "Sao Tome and Principe",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Middle Africa",
        "sub-region-code": "017"
    },
    "Saudi Arabia": {
        "alpha-2": "SA",
        "alpha-3": "SAU",
        "country-code": "682",
        "iso_3166-2": "ISO 3166-2:SA",
        "name": "Saudi Arabia",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Senegal": {
        "alpha-2": "SN",
        "alpha-3": "SEN",
        "country-code": "686",
        "iso_3166-2": "ISO 3166-2:SN",
        "name": "Senegal",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Serbia": {
        "alpha-2": "RS",
        "alpha-3": "SRB",
        "country-code": "688",
        "iso_3166-2": "ISO 3166-2:RS",
        "name": "Serbia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Seychelles": {
        "alpha-2": "SC",
        "alpha-3": "SYC",
        "country-code": "690",
        "iso_3166-2": "ISO 3166-2:SC",
        "name": "Seychelles",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Sierra Leone": {
        "alpha-2": "SL",
        "alpha-3": "SLE",
        "country-code": "694",
        "iso_3166-2": "ISO 3166-2:SL",
        "name": "Sierra Leone",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Singapore": {
        "alpha-2": "SG",
        "alpha-3": "SGP",
        "country-code": "702",
        "iso_3166-2": "ISO 3166-2:SG",
        "name": "Singapore",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Sint Maarten (Dutch part)": {
        "alpha-2": "SX",
        "alpha-3": "SXM",
        "country-code": "534",
        "iso_3166-2": "ISO 3166-2:SX",
        "name": "Sint Maarten (Dutch part)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Slovakia": {
        "alpha-2": "SK",
        "alpha-3": "SVK",
        "country-code": "703",
        "iso_3166-2": "ISO 3166-2:SK",
        "name": "Slovakia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "Slovenia": {
        "alpha-2": "SI",
        "alpha-3": "SVN",
        "country-code": "705",
        "iso_3166-2": "ISO 3166-2:SI",
        "name": "Slovenia",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Solomon Islands": {
        "alpha-2": "SB",
        "alpha-3": "SLB",
        "country-code": "090",
        "iso_3166-2": "ISO 3166-2:SB",
        "name": "Solomon Islands",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Melanesia",
        "sub-region-code": "054"
    },
    "Somalia": {
        "alpha-2": "SO",
        "alpha-3": "SOM",
        "country-code": "706",
        "iso_3166-2": "ISO 3166-2:SO",
        "name": "Somalia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "South Africa": {
        "alpha-2": "ZA",
        "alpha-3": "ZAF",
        "country-code": "710",
        "iso_3166-2": "ISO 3166-2:ZA",
        "name": "South Africa",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Southern Africa",
        "sub-region-code": "018"
    },
    "South Georgia and the South Sandwich Islands": {
        "alpha-2": "GS",
        "alpha-3": "SGS",
        "country-code": "239",
        "iso_3166-2": "ISO 3166-2:GS",
        "name": "South Georgia and the South Sandwich Islands",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "South Sudan": {
        "alpha-2": "SS",
        "alpha-3": "SSD",
        "country-code": "728",
        "iso_3166-2": "ISO 3166-2:SS",
        "name": "South Sudan",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Spain": {
        "alpha-2": "ES",
        "alpha-3": "ESP",
        "country-code": "724",
        "iso_3166-2": "ISO 3166-2:ES",
        "name": "Spain",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Southern Europe",
        "sub-region-code": "039"
    },
    "Sri Lanka": {
        "alpha-2": "LK",
        "alpha-3": "LKA",
        "country-code": "144",
        "iso_3166-2": "ISO 3166-2:LK",
        "name": "Sri Lanka",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Southern Asia",
        "sub-region-code": "034"
    },
    "Sudan": {
        "alpha-2": "SD",
        "alpha-3": "SDN",
        "country-code": "729",
        "iso_3166-2": "ISO 3166-2:SD",
        "name": "Sudan",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "Suriname": {
        "alpha-2": "SR",
        "alpha-3": "SUR",
        "country-code": "740",
        "iso_3166-2": "ISO 3166-2:SR",
        "name": "Suriname",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Svalbard and Jan Mayen": {
        "alpha-2": "SJ",
        "alpha-3": "SJM",
        "country-code": "744",
        "iso_3166-2": "ISO 3166-2:SJ",
        "name": "Svalbard and Jan Mayen",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Swaziland": {
        "alpha-2": "SZ",
        "alpha-3": "SWZ",
        "country-code": "748",
        "iso_3166-2": "ISO 3166-2:SZ",
        "name": "Swaziland",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Southern Africa",
        "sub-region-code": "018"
    },
    "Sweden": {
        "alpha-2": "SE",
        "alpha-3": "SWE",
        "country-code": "752",
        "iso_3166-2": "ISO 3166-2:SE",
        "name": "Sweden",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "Switzerland": {
        "alpha-2": "CH",
        "alpha-3": "CHE",
        "country-code": "756",
        "iso_3166-2": "ISO 3166-2:CH",
        "name": "Switzerland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Western Europe",
        "sub-region-code": "155"
    },
    "Syrian Arab Republic": {
        "alpha-2": "SY",
        "alpha-3": "SYR",
        "country-code": "760",
        "iso_3166-2": "ISO 3166-2:SY",
        "name": "Syrian Arab Republic",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Taiwan, Province of China": {
        "alpha-2": "TW",
        "alpha-3": "TWN",
        "country-code": "158",
        "iso_3166-2": "ISO 3166-2:TW",
        "name": "Taiwan, Province of China",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Eastern Asia",
        "sub-region-code": "030"
    },
    "Tajikistan": {
        "alpha-2": "TJ",
        "alpha-3": "TJK",
        "country-code": "762",
        "iso_3166-2": "ISO 3166-2:TJ",
        "name": "Tajikistan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Central Asia",
        "sub-region-code": "143"
    },
    "Tanzania, United Republic of": {
        "alpha-2": "TZ",
        "alpha-3": "TZA",
        "country-code": "834",
        "iso_3166-2": "ISO 3166-2:TZ",
        "name": "Tanzania, United Republic of",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Thailand": {
        "alpha-2": "TH",
        "alpha-3": "THA",
        "country-code": "764",
        "iso_3166-2": "ISO 3166-2:TH",
        "name": "Thailand",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Timor-Leste": {
        "alpha-2": "TL",
        "alpha-3": "TLS",
        "country-code": "626",
        "iso_3166-2": "ISO 3166-2:TL",
        "name": "Timor-Leste",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Togo": {
        "alpha-2": "TG",
        "alpha-3": "TGO",
        "country-code": "768",
        "iso_3166-2": "ISO 3166-2:TG",
        "name": "Togo",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Western Africa",
        "sub-region-code": "011"
    },
    "Tokelau": {
        "alpha-2": "TK",
        "alpha-3": "TKL",
        "country-code": "772",
        "iso_3166-2": "ISO 3166-2:TK",
        "name": "Tokelau",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "Tonga": {
        "alpha-2": "TO",
        "alpha-3": "TON",
        "country-code": "776",
        "iso_3166-2": "ISO 3166-2:TO",
        "name": "Tonga",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "Trinidad and Tobago": {
        "alpha-2": "TT",
        "alpha-3": "TTO",
        "country-code": "780",
        "iso_3166-2": "ISO 3166-2:TT",
        "name": "Trinidad and Tobago",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Tunisia": {
        "alpha-2": "TN",
        "alpha-3": "TUN",
        "country-code": "788",
        "iso_3166-2": "ISO 3166-2:TN",
        "name": "Tunisia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "Turkey": {
        "alpha-2": "TR",
        "alpha-3": "TUR",
        "country-code": "792",
        "iso_3166-2": "ISO 3166-2:TR",
        "name": "Turkey",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Turkmenistan": {
        "alpha-2": "TM",
        "alpha-3": "TKM",
        "country-code": "795",
        "iso_3166-2": "ISO 3166-2:TM",
        "name": "Turkmenistan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Central Asia",
        "sub-region-code": "143"
    },
    "Turks and Caicos Islands": {
        "alpha-2": "TC",
        "alpha-3": "TCA",
        "country-code": "796",
        "iso_3166-2": "ISO 3166-2:TC",
        "name": "Turks and Caicos Islands",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Tuvalu": {
        "alpha-2": "TV",
        "alpha-3": "TUV",
        "country-code": "798",
        "iso_3166-2": "ISO 3166-2:TV",
        "name": "Tuvalu",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "Uganda": {
        "alpha-2": "UG",
        "alpha-3": "UGA",
        "country-code": "800",
        "iso_3166-2": "ISO 3166-2:UG",
        "name": "Uganda",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Ukraine": {
        "alpha-2": "UA",
        "alpha-3": "UKR",
        "country-code": "804",
        "iso_3166-2": "ISO 3166-2:UA",
        "name": "Ukraine",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Eastern Europe",
        "sub-region-code": "151"
    },
    "United Arab Emirates": {
        "alpha-2": "AE",
        "alpha-3": "ARE",
        "country-code": "784",
        "iso_3166-2": "ISO 3166-2:AE",
        "name": "United Arab Emirates",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "United Kingdom of Great Britain and Northern Ireland": {
        "alpha-2": "GB",
        "alpha-3": "GBR",
        "country-code": "826",
        "iso_3166-2": "ISO 3166-2:GB",
        "name": "United Kingdom of Great Britain and Northern Ireland",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    },
    "United States Minor Outlying Islands": {
        "alpha-2": "UM",
        "alpha-3": "UMI",
        "country-code": "581",
        "iso_3166-2": "ISO 3166-2:UM",
        "name": "United States Minor Outlying Islands",
        "region": None,
        "region-code": None,
        "sub-region": None,
        "sub-region-code": None
    },
    "United States of America": {
        "alpha-2": "US",
        "alpha-3": "USA",
        "country-code": "840",
        "iso_3166-2": "ISO 3166-2:US",
        "name": "United States of America",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Northern America",
        "sub-region-code": "021"
    },
    "Uruguay": {
        "alpha-2": "UY",
        "alpha-3": "URY",
        "country-code": "858",
        "iso_3166-2": "ISO 3166-2:UY",
        "name": "Uruguay",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Uzbekistan": {
        "alpha-2": "UZ",
        "alpha-3": "UZB",
        "country-code": "860",
        "iso_3166-2": "ISO 3166-2:UZ",
        "name": "Uzbekistan",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Central Asia",
        "sub-region-code": "143"
    },
    "Vanuatu": {
        "alpha-2": "VU",
        "alpha-3": "VUT",
        "country-code": "548",
        "iso_3166-2": "ISO 3166-2:VU",
        "name": "Vanuatu",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Melanesia",
        "sub-region-code": "054"
    },
    "Venezuela (Bolivarian Republic of)": {
        "alpha-2": "VE",
        "alpha-3": "VEN",
        "country-code": "862",
        "iso_3166-2": "ISO 3166-2:VE",
        "name": "Venezuela (Bolivarian Republic of)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "South America",
        "sub-region-code": "005"
    },
    "Viet Nam": {
        "alpha-2": "VN",
        "alpha-3": "VNM",
        "country-code": "704",
        "iso_3166-2": "ISO 3166-2:VN",
        "name": "Viet Nam",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "South-Eastern Asia",
        "sub-region-code": "035"
    },
    "Virgin Islands (British)": {
        "alpha-2": "VG",
        "alpha-3": "VGB",
        "country-code": "092",
        "iso_3166-2": "ISO 3166-2:VG",
        "name": "Virgin Islands (British)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Virgin Islands (U.S.)": {
        "alpha-2": "VI",
        "alpha-3": "VIR",
        "country-code": "850",
        "iso_3166-2": "ISO 3166-2:VI",
        "name": "Virgin Islands (U.S.)",
        "region": "Americas",
        "region-code": "019",
        "sub-region": "Caribbean",
        "sub-region-code": "029"
    },
    "Wallis and Futuna": {
        "alpha-2": "WF",
        "alpha-3": "WLF",
        "country-code": "876",
        "iso_3166-2": "ISO 3166-2:WF",
        "name": "Wallis and Futuna",
        "region": "Oceania",
        "region-code": "009",
        "sub-region": "Polynesia",
        "sub-region-code": "061"
    },
    "Western Sahara": {
        "alpha-2": "EH",
        "alpha-3": "ESH",
        "country-code": "732",
        "iso_3166-2": "ISO 3166-2:EH",
        "name": "Western Sahara",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Northern Africa",
        "sub-region-code": "015"
    },
    "Yemen": {
        "alpha-2": "YE",
        "alpha-3": "YEM",
        "country-code": "887",
        "iso_3166-2": "ISO 3166-2:YE",
        "name": "Yemen",
        "region": "Asia",
        "region-code": "142",
        "sub-region": "Western Asia",
        "sub-region-code": "145"
    },
    "Zambia": {
        "alpha-2": "ZM",
        "alpha-3": "ZMB",
        "country-code": "894",
        "iso_3166-2": "ISO 3166-2:ZM",
        "name": "Zambia",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "Zimbabwe": {
        "alpha-2": "ZW",
        "alpha-3": "ZWE",
        "country-code": "716",
        "iso_3166-2": "ISO 3166-2:ZW",
        "name": "Zimbabwe",
        "region": "Africa",
        "region-code": "002",
        "sub-region": "Eastern Africa",
        "sub-region-code": "014"
    },
    "\u00c5land Islands": {
        "alpha-2": "AX",
        "alpha-3": "ALA",
        "country-code": "248",
        "iso_3166-2": "ISO 3166-2:AX",
        "name": "\u00c5land Islands",
        "region": "Europe",
        "region-code": "150",
        "sub-region": "Northern Europe",
        "sub-region-code": "154"
    }
}


def list_sorted_by_long_name():
    return sorted(
        [(key, value["native"]) for key, value in HTTP_LANGUAGE_TAGS.items()],
        key=lambda aTuple: aTuple[1])
