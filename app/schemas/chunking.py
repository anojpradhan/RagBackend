from enum import Enum


class ChunkingStrategy(str, Enum):
    RECURSIVE = "recursive"
    SENTENCE = "sentence"
