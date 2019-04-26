import autopy

bindings = {"Left Wink": None,
            "Right Wink": None,
            "Eyebrows Up": None,
            "Open Mouth": None,
            "Head Left": None,
            "Head Right": None,
            "Head Up": None,
            "Head Down": None
}

def pressBoundKey(motion):
    """Takes in a motion, and sends the bound key signal"""
    autopy.key.tap(bindings[motion])

def bind(motion, character):
    """Binds a character key to a motion in the bindings table"""
    bindings[motion] = character

def unbind(motion):
    """Unbinds a motion"""
    bindings[motion] = None