"""Guard explicit UTF-8 for portable text ingestion and corpus generation.

Windows Python may default to cp1252; omitting encoding broke module import.
"""
import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EncodingPolicyTests(unittest.TestCase):
    def test_all_repository_text_io_declares_utf8(self):
        for name in ("api/mcp.py", "scripts/build_corpus.py"):
            with self.subTest(file=name):
                src = (ROOT / name).read_text(encoding="utf-8")
                tree = ast.parse(src, filename=name)
                io_calls = [
                    node for node in ast.walk(tree)
                    if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr in {"read_text", "write_text"}
                ]
                self.assertTrue(io_calls, f"No text I/O detected in {name}")
                for node in io_calls:
                    options = {kw.arg: kw.value for kw in node.keywords}
                    self.assertIn("encoding", options, f"{name}:{node.lineno} omits encoding")
                    value = options["encoding"]
                    self.assertIsInstance(value, ast.Constant, f"{name}:{node.lineno}")
                    self.assertEqual(value.value.lower(), "utf-8", f"{name}:{node.lineno}")


if __name__ == "__main__":
    unittest.main()
