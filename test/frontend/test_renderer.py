import unittest

from lark import Token

from pcc.frontend.renderer import Renderer

class TestRenderer(unittest.TestCase):
    def test_render_normal_identifier(self):
        tok: Token = Token("NAME", "foobar")
        renderer = Renderer()
        result = renderer.process(iter([tok]))
        _ = list(result)
        print(renderer.identifiers)
        self.assertEqual(renderer.identifiers, {("foobar", "foobar")})

    def test_render_non_name(self):
        tok: Token = Token("DEC_INTEGER", 123)
        renderer = Renderer()
        result = renderer.process(iter([tok]))
        _ = list(result)
        self.assertEqual(renderer.identifiers, set())

    def test_format_unicode_identifier(self):
        tok: Token = Token("NAME", "$\\beta$")
        renderer = Renderer()
        result = renderer.process(iter([tok]))
        _ = list(result)
        self.assertEqual(renderer.identifiers, {("$\\beta$", "𝛽")})
