# Copyright (c) 2025 iiPython

# Modules
import re
import textwrap

# Initialization
TITLE_REGEX  = re.compile(r"<title>(.+)<\/title>")
BODY_REGEX   = re.compile(r"<body>(.*)<\/body>", re.S)
INDENT_REGEX = re.compile(r"^[ \t]*")

# Exceptions
class InvalidMarkup(Exception):
    pass

# Handle parsing
def wrap(text: str, width: int) -> list[str]:
    tags = []
    text = re.sub(r"<(?:(?:red|blue|b)|\/)\>", lambda match: [tags.append((match.span()[0], match.group())), ""][1], text)

    # Check actual tag status
    opening, offset = None, 0
    for index, (position, tag) in enumerate(tags):
        if tag == "</>":
            if opening is None:
                raise InvalidMarkup

            # Manage our position offset based on the last tag
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
