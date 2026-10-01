"""Registry of view builders (scene scripts register themselves with @view)."""
VIEWS = {}      # id -> (chapter, builder)
ORDER = []

def view(id, chapter):
    def deco(fn):
        VIEWS[id] = (chapter, fn)
        ORDER.append(id)
        return fn
    return deco
