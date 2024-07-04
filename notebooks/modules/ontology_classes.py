"""
Classes to infer ontology instances from a cognitive function and emotion
"""
import json
from json import JSONEncoder
from owlready2 import get_ontology

onto = get_ontology('./../ontology/COGAF_Ontology.rdf').load()


class CogafEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class CogafInstance():
    def __init__(self, cognitiveFunction: str, emotion: str) -> None:

        self.cognitiveFunction = CognitiveFunction(cognitiveFunction)

        self.emotion = Emotion(emotion)

    def to_json(self) -> str:
        return json.dumps(self, cls=CogafEncoder, indent=4)

    def to_dict(self) -> dict:
        return json.loads(self.to_json())


class CognitiveFunction():
    def __init__(self, name) -> None:
        self.name = name
        if onto[name] is None:
            raise NotImplementedError(
                "Cognitive Function not defined in ontology")
        self.isBasicFunction = onto[name].isBasicFunction[0]
        self.activities = []
        for activity in onto[name].trainedThrough:
            self.activities.append(ComplementaryActivity(activity.name))

        self.tasks = []
        for task in onto[name].assessedWith:
            self.tasks.append(PsychologicalTask(task.name))

        self.capabilites = []
        for capability in onto[name].generates:
            self.capabilites.append(capability.name)


class ComplementaryActivity():
    def __init__(self, name) -> None:
        self.name = name
        self.mechanics = []

        for mechanic in onto[name].comprises:
            self.mechanics.append(mechanic.name)


class PsychologicalTask():
    def __init__(self, name) -> None:
        self.name = name
        self.tests = []

        for test in onto[name].measuredWith:
            self.tests.append(CognitiveTest(test.name))


class CognitiveTest():
    def __init__(self, name) -> None:
        self.name = name
        instance = onto[name]
        self.abbreviation = instance.abbreviation
        self.description = instance.cognitiveTestDescription
        self.author = instance.author
        self.testType = instance.testType
        self.applicationType = instance.applicationType


class Emotion():
    def __init__(self, name) -> None:
        self.name = name
        if onto[name] is None:
            self.isBasicEmotion = None
            self.state = None
            return
        self.isBasicEmotion = onto[name].isBasicEmotion[0]
        self.state = State(onto[name].hasState)

        self.characteristics = []
        for chara in onto[name].characterizedBy:
            self.characteristics.append(Characteristic(chara.name))


class State():
    def __init__(self, state) -> None:
        self.valence = state.valence
        self.arousal = state.arousal


class Characteristic():
    def __init__(self, name) -> None:
        self.name = name
        self.parameters = []
        for param in onto[name].generates:
            self.parameters.append(param.name)

        self.recognitionMethod = onto[name].recognizedWith[0].name
