from randomdict import RandomDict # totally overkill, but was interested in testing out this module

easy_syllables = RandomDict()
for syllable in {
    "ba", "be", "bi", "bo", "bu",
    "da", "de", "di", "do", "du",
    "ma", "me", "mi", "mo", "mu",
    "pa", "pe", "pi", "po", "pu",
    "ra", "re", "ri", "ro", "ru",
    "sa", "se", "si", "so", "su",
    "ta", "te", "ti", "to", "tu",
    "ing", "ed", "er", "ly",
    "ay", "ee", "oo",
    "re", "un", "up",
    "lo", "ja", "zi", "nu", "fe",
    "ki", "ho", "mo", "za", "la",
    "vi", "wa", "ne", "yo", "ha"
}:
    easy_syllables[syllable] = None

medium_syllables = RandomDict()
for syllable in {
    "fa", "fe", "fi", "fo", "fu",
    "ga", "ge", "gi", "go", "gu",
    "ha", "he", "hi", "ho", "hu",
    "ja", "je", "ji", "jo", "ju",
    "ka", "ke", "ki", "ko", "ku",
    "la", "le", "li", "lo", "lu",
    "na", "ne", "ni", "no", "nu",
    "va", "ve", "vi", "vo", "vu",
    "wa", "we", "wi", "wo",
    "za", "ze", "zi", "zo", "zu",
    "bla", "ble", "blo",
    "cha", "che", "chi",
    "pla", "ple", "plo",
    "sta", "ste", "sto",
    "tra", "tre", "tri",
    "ment", "ness", "able", "ful", "less",
    "age", "ize", "ity", "ous",
    "ai", "ea", "oa", "oi", "ou",
    "dis", "mis", "non", "over", "pre",
    "bra", "bre", "bri", "bro", "bru",
    "dra", "dro", "gru", "swa", "swe",
    "fra", "flo", "sta", "sle", "spi",
    "blo", "cla", "gle", "phy", "sci",
    "tha", "tho", "qua", "qui", "sha"
}:
    medium_syllables[syllable] = None

hard_syllables = RandomDict()
for syllable in {
    "cra", "cre", "cri", "cro", "cru",
    "dra", "dre", "dri", "dro", "dru",
    "fra", "fre", "fri", "fro", "fru",
    "gra", "gre", "gri", "gro", "gru",
    "ska", "ske", "ski", "sko", "sku",
    "sma", "sme", "smi", "smo", "smu",
    "sna", "sne", "sni", "sno", "snu",
    "tion", "sion", "ible", "ably", "ibly",
    "ial", "ical", "ious", "ive", "ify",
    "anti", "auto", "inter", "semi", "super",
    "trans", "under",
    "phon", "graph", "scope", "sphere", "logy",
    "meter", "gram", "port", "form", "duct",
    "struct", "script", "rupt", "tract", "ject",
    "pose", "tend", "tain", "sist", "spect",
    "plex", "plic", "chron", "morph", "hydr",
    "therm", "astro", "geo", "bio", "psych",
    "mega", "nano", "penta", "hexa", "octo",
    "micro", "macro", "circum", "contra", "ambi",
    "hypo", "hyper", "peri", "mono", "poly",
    "phyll", "zym", "thel", "glyph", "lith"
}:
    hard_syllables[syllable] = None
