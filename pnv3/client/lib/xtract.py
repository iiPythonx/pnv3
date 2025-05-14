# Copyright (c) 2025 iiPython

# Modules
import re
import textwrap

# Initialization
ESCAPE_SEQS = {
    "black"  : 30,
    "red"    : 31,
    "green"  : 32,
    "yellow" : 33,
    "blue"   : 34,
    "magenta": 35,
    "cyan"   : 36,
    "white"  : 37,
    "/"      :  0,
}

# Regex
TITLE_REGEX  = re.compile(r"<title>(.+)<\/title>")
BODY_REGEX   = re.compile(r"<body>(.*)<\/body>", re.S)
ESCAPE_REGEX = re.compile(rf"<(?:(?:{'|'.join(ESCAPE_SEQS.keys())})|\/)\>")

# Exceptions
class InvalidMarkup(Exception):
    pass

# Handle parsing
def wrap(text: str, width: int) -> list[str]:
    tags = []
    def loopback(match: re.Match) -> str:
        tags.append((match.span()[0], match.group()))
        return ""

    text = ESCAPE_REGEX.sub(loopback, text)

    # Check actual tag status
    opening, offset = None, 0
    for index, (position, tag) in enumerate(tags):
        if tag == "</>":
            if opening is None:
                raise InvalidMarkup

            opening = None

        elif opening:
            raise InvalidMarkup

        else:
            opening = tag
        
        tags[index] = (position - offset, tag)
        offset += len(tag)

    # Build new lines
    lines = []
    while text:
        lines.append(text[:width])
        text = text[width:]

    for position, tag in reversed(tags):
        target_index = position // width
        target_offset = position - (target_index * width)
        lines[target_index] = lines[target_index][:target_offset] + tag + lines[target_index][target_offset:]

    return lines

def parse(input: str, width: int) -> tuple[str | None, list[str]]:
    title, content = (m := TITLE_REGEX.match(input)) and m.group(1), BODY_REGEX.search(input)
    if content is None:
        return title, wrap("This page has no content.", width)

    content = textwrap.dedent(content.group(1)).strip()
    return title, wrap(content, width)

def escape(input: list[str]) -> list[str]:
    active_escape, escaped_lines = None, []
    for line in input:
        last_match = None
        for match in ESCAPE_REGEX.findall(line):
            line = line.replace(match, f"\033[{ESCAPE_SEQS[match[1:-1].lower()]}m")
            last_match = match

        if active_escape is not None:
            line = f"\033[{ESCAPE_SEQS[active_escape.lower()]}m{line}"

        if last_match is not None:
            active_escape = None if last_match == "</>" else last_match[1:-1]

        escaped_lines.append(f"{line}\033[0m")

    return escaped_lines
