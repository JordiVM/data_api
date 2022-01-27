import random

# Defines functions used in tests


def random_string(n: int = 10):
    """
    Generates length n all lowercase letters returned as str
    """

    result = ""

    for _ in range(n):
        # Considering only lowercase letters
        random_integer = random.randint(97, 97 + 26 - 1)
        # Append generated characters using chr(x)
        result += chr(random_integer)

    return result
