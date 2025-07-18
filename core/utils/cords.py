import math
import re
from core.utils.env import SQUARE_SIZE

def number_to_letters(n):
    result = ""
    while True:
        n, rem = divmod(n, 26)
        result = chr(ord('a') + rem) + result
        if n == 0:
            break
        n -= 1
    return result

def cordsToSq(cords):
    x, y = cords[0], cords[1]
    sq = "q"

    if x < 0:
        sq += "'"
        xq = math.ceil(abs(x) / SQUARE_SIZE)
    else:
        xq = math.floor(x / SQUARE_SIZE) + 1
    sq += str(xq)

    y_index = math.ceil(abs(y) / SQUARE_SIZE) - 1
    letters = number_to_letters(y_index)
    sq += letters
    if y < 0:
        sq += "'"

    return sq

def sqToCoords(sq: str):
    match = re.fullmatch(r"q(')?(\d+)([a-z]+)(')?", sq)
    if not match:
        raise ValueError(f"Invalid square string: {sq}")

    x_negative = bool(match.group(1))
    xq = int(match.group(2))
    y_letters = match.group(3)
    y_negative = bool(match.group(4))

    x = xq * SQUARE_SIZE
    if x_negative:
        x = -x

    y_index = 0
    for i, ch in enumerate(reversed(y_letters)):
        y_index += (ord(ch) - ord('a')) * (26 ** i)
    y = (y_index + 1) * SQUARE_SIZE
    if y_negative:
        y = -y

    return (x, y)
