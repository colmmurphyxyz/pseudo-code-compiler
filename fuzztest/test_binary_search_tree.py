# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import pathlib
import unittest

from pcc.backend.pc_stdlib import PcBinaryTree

# add the parent directory (repository root) to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from res.transpiled_pc_examples.ch12.bst import INORDER_TREE_WALK, TREE_SEARCH, TREE_MINIMUM, TREE_MAXIMUM, \
    TREE_INSERT, TREE_DELETE

class TestBinarySearchTree(unittest.TestCase):
    def _make_bst(self) -> PcBinaryTree:
        """
                   10
                /      \\
               5        15
              / \\      /  \\
             3   7    12   17
        :return:
        """
        root = PcBinaryTree(10)
        root.left = PcBinaryTree(5, parent=root)
        root.right = PcBinaryTree(15, parent=root)
        root.left.left = PcBinaryTree(3, parent=root.left)
        root.left.right = PcBinaryTree(7, parent=root.left)
        root.right.left = PcBinaryTree(12, parent=root.right)
        root.right.right = PcBinaryTree(17, parent=root.right)
        return root

    def _inorder_walk(self, root: PcBinaryTree) -> list[any]:
        keys = []
        if root is not None:
            keys += self._inorder_walk(root.left)
            keys.append(root.key)
            keys += self._inorder_walk(root.right)
        return keys

    def test_tree_search(self):
        root = self._make_bst()
        node = TREE_SEARCH(root, 7)
        self.assertEqual(node.key, 7)

        node = TREE_SEARCH(root, 12)
        self.assertEqual(node.key, 12)

        node = TREE_SEARCH(root, 17)
        self.assertEqual(node.key, 17)

        node = TREE_SEARCH(root, 100)
        self.assertIsNone(node)

    def test_tree_minimum(self):
        root = self._make_bst()
        node = TREE_MINIMUM(root)
        self.assertEqual(node.key, 3)

    def test_tree_maximum(self):
        root = self._make_bst()
        node = TREE_MAXIMUM(root)
        self.assertEqual(node.key, 17)

    def test_tree_insert(self):
        root = self._make_bst()
        TREE_INSERT(root, PcBinaryTree(8))
        node = root.left.right.right
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 8)

    def test_tree_delete(self):
        root = self._make_bst()
        # delete leaf node
        TREE_DELETE(root, root.left.left)
        self.assertListEqual(self._inorder_walk(root), [5, 7, 10, 12, 15, 17])
        # delete non-leaf node
        TREE_DELETE(root, root.right)
        self.assertListEqual(self._inorder_walk(root), [5, 7, 10, 12, 17])
