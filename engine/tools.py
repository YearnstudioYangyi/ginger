import json, re


def parseResult(hasCodeBlock: str):
    pattern = re.compile(r"```(\w*)\n(.*?)\n```", re.DOTALL)
    matches = pattern.search(hasCodeBlock)
    if matches:
        return matches.group(2).strip()
    else:
        return hasCodeBlock


def getOutput(aiResponse: str) -> str:
    return json.loads(parseResult(aiResponse))["output"]


def getExtension(aiResponse: str) -> str:
    return json.loads(parseResult(aiResponse))["extension"]


def getStatus(aiResponse: str) -> bool:
    return json.loads(parseResult(aiResponse))["status"]


def getDependencies(aiResponse: str) -> list[str]:
    return json.loads(parseResult(aiResponse))["dependencies"]


def getData(output: str):
    return "\n".join(output)


def mergeDictRecursive(*dicts: dict):
    if len(dicts) == 0:
        return {}
    elif len(dicts) < 2:
        return dicts[0]
    else:
        dictsList = list(dicts)
        dict1 = dictsList[0]
        dict2 = dictsList[1]
        del dictsList[:2]
        mergedDict = dict1.copy()
        for key, value in dict2.items():
            if (
                key in dict1
                and isinstance(dict1[key], dict)
                and isinstance(value, dict)
            ):
                mergedDict[key] = mergeDictRecursive(dict1[key], value)
            else:
                mergedDict[key] = value
        return mergeDictRecursive(mergedDict, *dictsList)
