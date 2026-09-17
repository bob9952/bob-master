#!/usr/bin/env python3
"""Split a Cursor transcript only at complete User/Cursor message boundaries.

The generated ``chunk_NNN.md`` files contain source text only.  Their byte
concatenation is verified against the input after each run.  ``manifest.json``
is deliberately a sidecar so that it can hold metadata without changing the
transcript text.

Token counting uses ``tiktoken``'s ``cl100k_base`` encoding when it is
installed.  No dependency is required: the deterministic fallback counts each
Unicode word run and each non-whitespace, non-word character as one estimated
token.  The fallback is an estimate, so chunk sizes can differ from model token
counts, but the message boundaries and output content are identical.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


DEFAULT_INPUT = Path("cursor_master_thesis_implementation_pla.md")
DEFAULT_OUTPUT = Path("chunks")
DEFAULT_TARGET_TOKENS = 20_000

# A delimiter is structural only when it has the exact blank-line layout used
# by Cursor exports.  Bare --- lines inside message bodies do not match.
MESSAGE_BOUNDARY = re.compile(
    r"(?m)^---(?:\r?\n){2}\*\*(?:User|Cursor)\*\*(?:\r?\n){2}"
)
FALLBACK_TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


class SplitterError(ValueError):
    """Raised when a transcript cannot be safely split or verified."""


@dataclass(frozen=True)
class Message:
    index: int
    content: str
    start_char: int
    end_char: int


@dataclass(frozen=True)
class Chunk:
    index: int
    messages: tuple[Message, ...]
    token_count: int

    @property
    def content(self) -> str:
        return "".join(message.content for message in self.messages)


def fallback_token_count(text: str) -> int:
    """Return a dependency-free, deterministic approximation of token count."""

    return len(FALLBACK_TOKEN_PATTERN.findall(text))


def get_token_counter() -> tuple[str, Callable[[str], int]]:
    """Return the available counter and a stable label for the manifest."""

    try:
        import tiktoken  # type: ignore[import-not-found]

        encoder = tiktoken.get_encoding("cl100k_base")
    except (ImportError, AttributeError, KeyError, OSError):
        return "deterministic_regex_estimate", fallback_token_count

    return "tiktoken:cl100k_base", lambda text: len(encoder.encode(text))


def parse_messages(source: str) -> list[Message]:
    """Return messages while attaching any export prelude to message one."""

    starts = [match.start() for match in MESSAGE_BOUNDARY.finditer(source)]
    if not starts:
        raise SplitterError(
            "No Cursor message boundaries found; expected --- followed by a blank "
            "line and a **User** or **Cursor** heading."
        )

    messages: list[Message] = []
    for index, start in enumerate(starts, start=1):
        end = starts[index] if index < len(starts) else len(source)
        # The first slice intentionally begins at zero, retaining the prelude.
        slice_start = 0 if index == 1 else start
        messages.append(Message(index, source[slice_start:end], slice_start, end))
    return messages


def build_chunks(
    messages: Sequence[Message], target_tokens: int, count_tokens: Callable[[str], int]
) -> list[Chunk]:
    """Greedily group whole messages without exceeding the target when possible."""

    if target_tokens <= 0:
        raise SplitterError("Target token count must be positive.")

    chunks: list[Chunk] = []
    pending: list[Message] = []

    def flush() -> None:
        if not pending:
            return
        content = "".join(message.content for message in pending)
        chunks.append(Chunk(len(chunks) + 1, tuple(pending), count_tokens(content)))
        pending.clear()

    for message in messages:
        if not pending:
            message_tokens = count_tokens(message.content)
            pending.append(message)
            if message_tokens > target_tokens:
                flush()
            continue

        candidate = "".join(item.content for item in (*pending, message))
        if count_tokens(candidate) > target_tokens:
            flush()
            pending.append(message)
            if count_tokens(message.content) > target_tokens:
                flush()
        else:
            pending.append(message)

    flush()
    return chunks


def _byte_offset(text: str, char_offset: int, encoding: str) -> int:
    return len(text[:char_offset].encode(encoding))


def make_manifest(
    source_path: Path,
    source_bytes: bytes,
    source_text: str,
    chunks: Sequence[Chunk],
    encoding: str,
    tokenizer: str,
    target_tokens: int,
) -> dict[str, object]:
    oversized = [
        message.index
        for chunk in chunks
        if len(chunk.messages) == 1 and chunk.token_count > target_tokens
        for message in chunk.messages
    ]
    return {
        "format": "cursor-conversation-chunks-v1",
        "source": {
            "path": str(source_path),
            "sha256": hashlib.sha256(source_bytes).hexdigest(),
            "bytes": len(source_bytes),
            "encoding": encoding,
            "message_count": sum(len(chunk.messages) for chunk in chunks),
        },
        "split": {
            "target_tokens": target_tokens,
            "tokenizer": tokenizer,
            "boundary": "--- + blank line + **User**/**Cursor** + blank line",
            "lossless_reconstruction_verified": True,
            "oversized_message_indexes": oversized,
        },
        "chunks": [
            {
                "file": f"chunk_{chunk.index:03d}.md",
                "token_count": chunk.token_count,
                "message_indexes": [message.index for message in chunk.messages],
                "source_char_range": [
                    chunk.messages[0].start_char,
                    chunk.messages[-1].end_char,
                ],
                "source_byte_range": [
                    _byte_offset(source_text, chunk.messages[0].start_char, encoding),
                    _byte_offset(source_text, chunk.messages[-1].end_char, encoding),
                ],
            }
            for chunk in chunks
        ],
    }


def validate_reconstruction(source_bytes: bytes, chunk_paths: Sequence[Path]) -> None:
    """Raise when emitted chunks do not reconstruct the input byte-for-byte."""

    reconstructed = b"".join(path.read_bytes() for path in chunk_paths)
    if reconstructed != source_bytes:
        raise SplitterError("Chunk reconstruction does not match the source bytes.")


def split_file(
    input_path: Path,
    output_dir: Path,
    target_tokens: int = DEFAULT_TARGET_TOKENS,
    encoding: str = "utf-8",
) -> dict[str, object]:
    """Split one transcript, write chunks plus manifest, and return the manifest."""

    source_bytes = input_path.read_bytes()
    try:
        source_text = source_bytes.decode(encoding)
    except UnicodeDecodeError as error:
        raise SplitterError(f"Cannot decode {input_path} as {encoding}: {error}") from error

    tokenizer, count_tokens = get_token_counter()
    messages = parse_messages(source_text)
    chunks = build_chunks(messages, target_tokens, count_tokens)

    output_dir.mkdir(parents=True, exist_ok=True)
    chunk_paths: list[Path] = []
    for chunk in chunks:
        path = output_dir / f"chunk_{chunk.index:03d}.md"
        path.write_bytes(chunk.content.encode(encoding))
        chunk_paths.append(path)

    validate_reconstruction(source_bytes, chunk_paths)
    manifest = make_manifest(
        input_path,
        source_bytes,
        source_text,
        chunks,
        encoding,
        tokenizer,
        target_tokens,
    )
    with (output_dir / "manifest.json").open("w", encoding="utf-8", newline="\n") as manifest_file:
        manifest_file.write(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    for stale_path in output_dir.glob("chunk_*.md"):
        if stale_path not in chunk_paths:
            stale_path.unlink()

    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--target-tokens", type=int, default=DEFAULT_TARGET_TOKENS,
        help="Preferred maximum tokens per chunk (default: %(default)s).",
    )
    parser.add_argument("--encoding", default="utf-8", help="Transcript encoding (default: utf-8).")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        manifest = split_file(args.input, args.output, args.target_tokens, args.encoding)
    except (OSError, SplitterError) as error:
        print(f"split_conversation: {error}", file=sys.stderr)
        return 1

    chunks = manifest["chunks"]
    oversized = manifest["split"]["oversized_message_indexes"]
    print(f"Wrote {len(chunks)} chunks for {manifest['source']['message_count']} messages to {args.output}.")
    if oversized:
        print(f"Oversized messages kept alone: {', '.join(map(str, oversized))}.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
