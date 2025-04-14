from typing import Protocol

from lark import Tree

class PccTranspiler(Protocol):
    def transpile(self, tree: Tree) -> str:
        """
        Transpile the given Pcc AST to Python code.

        Args:
            tree (Tree): The Abstract Syntax Tree to transpile.

        Returns:
            str: The transpiled Python code.
        """
        ...