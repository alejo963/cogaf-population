__event_title = [{"IS_PUNCT": True},
                 {"LOWER": {"FUZZY": "qué"}},
                 {"LOWER": {"FUZZY": "pasó"}},
                 {"IS_PUNCT": True}]

__event_title_2 = [{"LOWER": {"FUZZY": "descripción"}},
                   {"LOWER": "del"},
                   {"LOWER": {"FUZZY": {"IN": ["accidente", "caso"]}}}]

__event_title_3 = [{"IS_PUNCT": True},
                   {"LOWER": {"FUZZY": "qué"}},
                   {"LOWER": {"FUZZY": "sucedió"}},
                   {"LOWER": "y"},
                   {"LOWER": {"FUZZY2": "consecuencia"}},
                   {"IS_PUNCT": True}]

__event_content = [{"OP": r"{1,}"}, {"TEXT": "."},
                   {"OP": "?", "IS_PUNCT": True},
                   {"LOWER": {"REGEX": {"IN": ["consecuencias*", "acciones", "qué*e*", "causas"]}}}]

EVENT_PATTERNS = [
    [*__event_title, *__event_content],
    [*__event_title_2, *__event_content],
    [*__event_title_3, *__event_content]
]

CAPABILITY_NOUNS = ("control", "supervisión", "evaluación", "comunicación",
                    "seguimiento", "concentración", "planificación",
                    "inspección", "orientación", "identificación", "reacción",
                    "planeación", "autocuidado", "entendimiento", "confianza")
CAPABILITY_VERBS = ("controlar", "supervisar", "evaluar", "comunicar",
                    "seguir", "concentrar", "planificar",
                    "inspeccionar", "orientar", "identificar", "reaccionar",
                    "planear", "autocuidar", "entender", "confiar")

CAPABILITY_PATTERNS = [
    [{"POS": "NOUN", "LOWER": {"FUZZY2": {"IN": CAPABILITY_NOUNS}}}],
    [{"POS": "VERB", "LOWER": {"FUZZY2": {"IN": CAPABILITY_VERBS}}}],
]
