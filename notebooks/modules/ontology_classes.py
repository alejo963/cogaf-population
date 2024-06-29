"""
Classes to infer ontology instances from a cognitive function and emotion
"""

from owlready2 import get_ontology

onto = get_ontology('./../ontology/COGAF_Ontology.rdf').load()


class CogafInstance():
    def __init__(self, cognitiveFunction: str, emotion: str) -> None:

        self.cognitiveFunction = CognitiveFunction(cognitiveFunction)

        self.emotion = Emotion(emotion)

    def toDict(self) -> dict:
        return {
            "cognitiveFunction": self.cognitiveFunction.toDict(),
            "emotion": self.emotion.toDict()
        }


class CognitiveFunction():
    def __init__(self, name) -> None:
        self.name = name
        if onto[name] is None:
            raise NotImplementedError("Cognitive Function not defined in ontology")
        self.isBasicFunction = onto[name].isBasicFunction[0]
        self.activities = []
        for activity in onto[name].trainedThrough:
            self.activities.append(ComplementaryActivity(activity.name))

        self.tasks = []
        for task in onto[name].assessedWith:
            self.tasks.append(PsychologicalTask(task.name))

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "isBasicFunction": self.isBasicFunction,
            "activities": [act.toDict() for act in self.activities],
            "tasks": [task.toDict() for task in self.tasks],
        }


class ComplementaryActivity():
    def __init__(self, name) -> None:
        self.name = name
        self.mechanics = []

        for mechanic in onto[name].comprises:
            self.mechanics.append(mechanic.name)

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "mechanics": [mechanic for mechanic in self.mechanics],
        }


class PsychologicalTask():
    def __init__(self, name) -> None:
        self.name = name
        self.tests = []

        for test in onto[name].measuredWith:
            self.tests.append(CognitiveTest(test.name))

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "tests": [test.toDict() for test in self.tests],
        }


class CognitiveTest():
    def __init__(self, name) -> None:
        self.name = name
        instance = onto[name]
        self.abbreviation = instance.abbreviation
        self.description = instance.cognitiveTestDescription
        self.author = instance.author
        self.testType = instance.testType
        self.applicationType = instance.applicationType

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "abbreviation": self.abbreviation,
            "description": self.description,
            "author": self.author,
            "testType": self.testType,
            "applicationType": self.applicationType,
        }


class Emotion():
    def __init__(self, name) -> None:
        self.name = name
        self.isBasicEmotion = onto[name].isBasicEmotion[0]
        self.state = State(onto[name].hasState)

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "isBasicEmotion": self.isBasicEmotion,
            "state": self.state.toDict()
        }


class State():
    def __init__(self, state) -> None:
        self.valence = state.valence
        self.arousal = state.arousal

    def toDict(self) -> dict:
        return {
            "valence": self.valence,
            "arousal": self.arousal
        }
