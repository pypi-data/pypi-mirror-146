"""Score"""

import os
import pickle

from pgml.exceptions import PgMLException

def load(name, source):
    path = os.path.join(source, name)

    if not os.path.exists(path):
        raise PgMLException(f"Model source directory `{path}` does not exist.")

    with open(path, "rb") as f:
        return pickle.load(f)
