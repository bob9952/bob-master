from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "split_conversation.py"
SPEC = importlib.util.spec_from_file_location("split_conversation", MODULE_PATH)
assert SPEC and SPEC.loader
splitter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = splitter
SPEC.loader.exec_module(splitter)


PRELUDE = "# Export\n_Export metadata_\n\n"


def message(role: str, body: str) -> str:
    return f"---\n\n**{role}**\n\n{body}"


class SplitConversationTests(unittest.TestCase):
    def test_parse_keeps_prelude_and_ignores_bare_rules_in_message_bodies(self) -> None:
        source = (
            PRELUDE
            + message("User", "First message\n\n---\n\nnot a heading\n")
            + message("Cursor", "Second message\n---\ninside the response\n")
            + message("User", "Third message\n")
        )

        messages = splitter.parse_messages(source)

        self.assertEqual(3, len(messages))
        self.assertTrue(messages[0].content.startswith(PRELUDE))
        self.assertIn("not a heading", messages[0].content)
        self.assertIn("inside the response", messages[1].content)
        self.assertEqual(source, "".join(item.content for item in messages))

    def test_build_chunks_preserves_message_boundaries_and_oversized_message(self) -> None:
        source = (
            PRELUDE
            + message("User", "one two\n")
            + message("Cursor", "three four\n")
            + message("User", "five six seven eight\n")
        )
        messages = splitter.parse_messages(source)

        chunks = splitter.build_chunks(messages, target_tokens=4, count_tokens=splitter.fallback_token_count)

        self.assertEqual([[1], [2], [3]], [[m.index for m in c.messages] for c in chunks])
        self.assertGreater(chunks[2].token_count, 4)
        self.assertEqual(source, "".join(chunk.content for chunk in chunks))

    def test_split_file_writes_lossless_chunks_and_metadata(self) -> None:
        source = (
            PRELUDE
            + message("User", "alpha beta\n")
            + message("Cursor", "gamma delta\n")
            + message("User", "epsilon zeta eta theta iota kappa lambda mu nu xi\n")
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_path = root / "conversation.md"
            output_dir = root / "chunks"
            input_path.write_bytes(source.encode("utf-8"))

            with patch.object(
                splitter,
                "get_token_counter",
                return_value=("test_word_counter", lambda text: len(text.split())),
            ):
                manifest = splitter.split_file(input_path, output_dir, target_tokens=8)

            chunk_paths = sorted(output_dir.glob("chunk_*.md"))
            self.assertEqual(source.encode("utf-8"), b"".join(path.read_bytes() for path in chunk_paths))
            saved_manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest, saved_manifest)
            self.assertEqual(3, saved_manifest["source"]["message_count"])
            self.assertEqual([3], saved_manifest["split"]["oversized_message_indexes"])

    def test_parse_rejects_content_without_structural_message_boundary(self) -> None:
        with self.assertRaises(splitter.SplitterError):
            splitter.parse_messages("# Export\n\n---\n\nplain text\n")


if __name__ == "__main__":
    unittest.main()
