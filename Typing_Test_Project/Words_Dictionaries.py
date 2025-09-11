"""-----------------------Words lists with different difficulty---------------------------------------------------"""

easy_list = ["apple", "book", "cat", "dog", "banana", "egg", "fish", "game", "hat", "ice", "jump", "kite", "leaf",
             "moon", "nest", "orange", "pig", "queen", "rose", "star", "tree", "stick", "van", "whale", "xylophone",
             "yarn", "lion", "chair", "table", "water", "door", "shoe", "light", "cloud", "smile", "mug", "fruit",
             "heart", "bird", "road", "pencil", "grass", "park", "river", "mountain", "candy", "song", "gift",
             "watch", "tent"]

medium_list = ["adventure", "bicycle", "calculator", "dolphin", "elephant", "festival", "constellation", "harmony",
               "island", "journey", "keyboard", "library", "ocean", "journal", "orchestra", "paradise", "question",
               "rainbow", "scientist", "telephone", "universe", "vacation", "waterfall", "chameleon", "zebra",
               "astronaut", "butterfly", "chocolate", "dinosaur", "encyclopedia", "firefighter", "guitar", "harmonica",
               "imagination", "jellyfish", "lantern", "lemonade", "microscope", "notebook", "octopus", "photograph",
               "quokka", "raccoon", "sunflower", "telescope", "umbrella", "violin", "watermelon", "yogurt", "galaxy"]

hard_list = ["abomination", "bureaucracy", "cacophony", "discombobulate", "eclectic", "flamboyant", "gargantuan",
             "harbinger", "incongruous", "juxtaposition", "labyrinthine", "meticulously", "nefarious", "obfuscate",
             "plethora", "quintessential", "rudimentary", "serendipity", "taciturn", "ubiquitous", "verbose",
             "whimsical", "metamorphosis", "zephyr", "ambidextrous", "belligerent", "conundrum", "dichotomy",
             "ephemeral", "fervent", "grandiloquent", "hegemony", "idiosyncrasy", "juxtapose", "paradox", "limpid",
             "munificent", "nonchalant", "obstreperous", "palimpsest", "democracy", "recalcitrant", "sagacious",
             "tumultuous", "vacillate", "waning", "xenophobe", "enigmatic", "zealous", "ambivalence"]

state_dictionary = {
    # game state
    "typing_words": [],
    "typed_words": [],
    "counter": 0,
    "score": 0,
    "start_time": None,
    "stop_time": None,
    "mistakes_words": [],
    "correct_word": [],

    # text highlights
    "start_index": "",
    "end_index": "",
    "tag_name": "highlight",
    "correct_tag": "green",
    "false_tag": "red"
                }
