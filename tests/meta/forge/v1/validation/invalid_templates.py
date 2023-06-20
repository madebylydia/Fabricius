from fabricius.app.forger.v1 import SetupV1


def setup() -> SetupV1:
    return {"version": 1, "type": "template", "root": "templates", "templates": "my_template"}
