event_title = [{"IS_PUNCT": True},
               {"LOWER": {"FUZZY": "qué"}},
               {"LOWER": {"FUZZY": "pasó"}},
               {"IS_PUNCT": True}]

event_title_2 = [{"LOWER": {"FUZZY": "descripción"}},
                 {"LOWER": "del"},
                 {"LOWER": {"FUZZY": {"IN": ["accidente", "caso"]}}}]

event_title_3 = [{"IS_PUNCT": True},
                 {"LOWER": {"FUZZY": "qué"}},
                 {"LOWER": {"FUZZY": "sucedió"}},
                 {"LOWER": {"y"}},
                 {"LOWER": {"consecuencia"}},
                 {"IS_PUNCT": True}]

event_content = [{"OP": r"{1,}"}, {"TEXT": "."},
                 {"LOWER": {"REGEX": {"IN": ["consecuencias*", "acciones"]}}}]
EVENT_PATTERNS = [
    [*event_title, *event_content],
    [*event_title_2, *event_content]
]
