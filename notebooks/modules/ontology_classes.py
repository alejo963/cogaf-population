"""
Classes to infer ontology instances from a cognitive function and emotion
"""
import json
from json import JSONEncoder
from owlready2 import Ontology


def set_ontology(ontology: Ontology):
    global onto
    onto = ontology


class CogafEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class CogafInstance():
    def __init__(self, input_dict: dict) -> None:
        self.name = input_dict["file"][:-4]
        self.cognitiveFunction = CognitiveFunction(input_dict)
        self.emotion = HourglassEmotion(input_dict["emotion"], self.name)
        self.event = input_dict["event"]

    def to_json(self) -> str:
        return json.dumps(self, cls=CogafEncoder, indent=4)

    def to_dict(self) -> dict:
        return json.loads(self.to_json())

    def populate_ontology(self) -> None:
        if onto[self.name] is None:
            onto.Event(self.name, eventDescription=self.event)
        self.cognitiveFunction.populate(self.name)
        self.emotion.populate(self.name)

    def infer_components(self):
        pass


class CognitiveFunction():
    def __init__(self, input_dict) -> None:
        self.name = input_dict["cognitive_function"]
        if onto[self.name] is None:
            raise NotImplementedError(
                "Cognitive Function not defined in ontology")
        self.isBasicFunction = onto[self.name].isBasicFunction
        self.activities = []
        self.tasks = []
        self.capabilites = input_dict["capabilities"]

    def populate(self, event_name):
        for cap in self.capabilites:
            if onto[cap] is None:
                onto.Capability(cap)

            onto[self.name].generates.append(onto[cap])
            onto[cap].inEvent.append(onto[event_name])

    def infer(self):

        for activity in onto[self.name].trainedThrough:
            self.activities.append(ComplementaryActivity(activity.name))

        for task in onto[self.name].assessedWith:
            self.tasks.append(PsychologicalTask(task.name))


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


class HourglassEmotion():
    def __init__(self, emotion, name) -> None:
        self.name = name + "_emotion"
        self.introspection = emotion["introspection"]
        self.temper = emotion["temper"]
        self.attitude = emotion["attitude"]
        self.sensitivity = emotion["sensitivity"]

    def populate(self, event_name):
        if onto[self.name] is None:
            onto.Emotion(self.name,
                         introspection=self.introspection["value"],
                         temper=self.temper["value"],
                         attitude=self.attitude["value"],
                         sensitivity=self.sensitivity["value"],
                         )
        onto[self.name].inEvent.append(onto[event_name])


class Emotion():
    def __init__(self, name) -> None:
        self.name = name
        if onto[name] is None:
            self.isBasicEmotion = None
            self.state = None
            return
        self.isBasicEmotion = onto[name].isBasicEmotion
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
