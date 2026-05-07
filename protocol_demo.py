from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol, runtime_checkable


class Writer(Protocol):
    def write(self, message: str) -> None:
        ...


class ScoreFormatter(Protocol):
    def __call__(self, title: str, score: float) -> str:
        ...


@runtime_checkable
class Closable(Protocol):
    def close(self) -> None:
        ...


class ConsoleWriter:
    def write(self, message: str) -> None:
        print(f"[console] {message}")


class MemoryWriter:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def write(self, message: str) -> None:
        self.messages.append(message)

    def close(self) -> None:
        print(f"[memory] flushed {len(self.messages)} messages")


@dataclass(slots=True)
class JobMatch:
    title: str
    company: str
    score: float


def broadcast(message: str, writers: Iterable[Writer]) -> None:
    for writer in writers:
        writer.write(message)


def render_match(match: JobMatch, formatter: ScoreFormatter) -> str:
    return formatter(f"{match.title} @ {match.company}", match.score)


def close_if_possible(value: object) -> None:
    if isinstance(value, Closable):
        value.close()
    else:
        print("[close] object is not closable")


def simple_formatter(title: str, score: float) -> str:
    return f"{title} -> {score:.0%} match"


def excited_formatter(title: str, score: float) -> str:
    level = "HIGH" if score >= 0.85 else "MEDIUM"
    return f"{level}: {title} ({score:.1%})"


def main() -> None:
    console = ConsoleWriter()
    memory = MemoryWriter()
    writers: list[Writer] = [console, memory]

    match = JobMatch(title="Backend Engineer", company="Example AI", score=0.91)
    formatted = render_match(match, simple_formatter)
    broadcast(formatted, writers)

    loud_version = render_match(match, excited_formatter)
    broadcast(loud_version, writers)

    print("[memory] stored messages:")
    for item in memory.messages:
        print(f"  - {item}")

    close_if_possible(memory)
    close_if_possible(console)


if __name__ == "__main__":
    main()