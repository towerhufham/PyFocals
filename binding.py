import autopy

motions = ["Left Wink", "Right Wink", "Eyebrows Up", "Open Mouth", "Head Left", "Head Right", "Head Up", "Head Down"]

bindings = {"Left Wink": "x",
            "Right Wink": "o",
            "Eyebrows Up": None,
            "Open Mouth": None,
            "Head Left": None,
            "Head Right": None,
            "Head Up": None,
            "Head Down": None
}

def getBindString(motion):
    """Returns a string of the form "motion: key" for use in the ui"""
    if bindings[motion]:
        return motion + ": " + bindings[motion]
    else:
        return motion + ": (unbound)"

def pressBoundKey(motion):
    """Takes in a motion, and sends the bound key signal"""
    print("pressing " + bindings[motion])
    autopy.key.tap(bindings[motion], [])

def bind(motion, character):
    """Binds a character key to a motion in the bindings table"""
    bindings[motion] = character

def unbind(motion):
    """Unbinds a motion"""
    bindings[motion] = None
