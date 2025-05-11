__version__ = "3.1.0"

import re
import logging

logging.basicConfig(
    filename = "pnv3.log",
    level = logging.DEBUG,
    format = "%(asctime)s [%(levelname)s] %(message)s"
)

# Handle real string length calculation
ANSI_ESCAPE = re.compile(r"\033\[[0-?]*[ -/]*[@-~]")

def xlen(string: str) -> int:
    return len(ANSI_ESCAPE.sub("", string))
