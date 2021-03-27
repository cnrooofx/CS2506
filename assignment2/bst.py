"""Binary Search Tree.

Script Name: bst.py
Author: Conor Fox
"""

class BinaryTree:
    """A Balanced Binary Search (AVL) Tree."""

    def __init__(self):
        """Initialise a new BST."""
        self._root = None
    
    def size(self):
        """Return the size of the tree."""
        if not self._root:
            return 0
        return self._root.size()
    
    def add(self, item):
        """Add item to the tree."""
        if not self._root:
            self._root = BSTNode(item)
            return item
        return self._root.add(item)
    
    def search(self, item):
        """Search for item in the tree."""
        if self._root:
            return self._root.search(item)
    
    def remove(self, item):
        """Remove item from the tree."""
        if self._root:
            removed = self._root.remove(item)
            if self._root.size() <= 0:
                self._root = None
            return removed


class BSTNode:
    """An internal node for a Binary Search Tree."""

    def __init__(self, item):
        """Initialise a BSTNode on creation, with value==item."""
        self._element = item
        self._leftchild = None
        self._rightchild = None
        self._parent = None
        self._height = 0

    def search(self, searchitem):
        """Return object matching searchitem, or None.

        Args:
            searchitem: an object of any class stored in the BST
        """
        node = self.search_node(searchitem)
        if node is not None:
            return node._element

    def search_node(self, searchitem):
        """Return the BSTNode (with subtree) containing searchitem, or None.

        Args:
            searchitem: an object of any class stored in the BST
        """
        if self._element is None:
            return None
        elif self._element == searchitem:
            pass
        elif not self._leftchild and not self._rightchild:
            return None
        elif searchitem < self._element:
            if not self._leftchild:
                return None
            return self._leftchild.search_node(searchitem)
        elif self._element < searchitem:
            if not self._rightchild:
                return None
            return self._rightchild.search_node(searchitem)
        return self

    def add(self, obj):
        """Add item to the tree, maintaining BST properties.

        Returns the item added, or None if a matching object was already there.
        """
        if self._element is None:
            self._element = obj
        elif self._element is obj:
            return None
        elif obj <= self._element:
            if not self._leftchild:
                new = BSTNode(obj)  # Create a new node for the object
                self._leftchild = new  # Link current node to new node
                new._parent = self
                self._rebalance()  # Self is the parent, so rebalance it
            else:
                self._leftchild.add(obj)
        elif obj >= self._element:
            if not self._rightchild:
                new = BSTNode(obj)
                self._rightchild = new
                new._parent = self
                self._rebalance()
            else:
                self._rightchild.add(obj)
        return obj

    def findmaxnode(self):
        """Return the BSTNode with maximal element at or below here."""
        if not self._rightchild:
            return self
        return self._rightchild.findmaxnode()

    def height(self):
        """Return the height of this node.

        Note that with the recursive definition of the tree the height of the
        node is the same as the depth of the tree rooted at this node.
        """
        if not self._leftchild and not self._rightchild:
            return 0
        if self._leftchild and not self._rightchild:
            return 1 + self._leftchild.height()
        if self._rightchild and not self._leftchild:
            return 1 + self._rightchild.height()
        return 1 + max(self._leftchild.height(), self._rightchild.height())

    def size(self):
        """Return the size of this subtree.

        The size is the number of nodes (or elements) in the tree,
        including this node.
        """
        if not self._leftchild and not self._rightchild:
            return 1
        if self._leftchild and not self._rightchild:
            return 1 + self._leftchild.size()
        if self._rightchild and not self._leftchild:
            return 1 + self._rightchild.size()
        return 1 + self._leftchild.size() + self._rightchild.size()

    def leaf(self):
        """Return True if this node has no children."""
        if not self._leftchild and not self._rightchild:
            return True
        return False

    def semileaf(self):
        """Return True if this node has exactly one child."""
        if self._leftchild and not self._rightchild:
            return True
        if self._rightchild and not self._leftchild:
            return True
        return False

    def full(self):
        """Return true if this node has two children."""
        if self._leftchild and self._rightchild:
            return True
        return False

    def internal(self):
        """Return True if this node has at least one child."""
        if self._leftchild or self._rightchild:
            return True
        return False

    def remove(self, searchitem):
        """Remove and return the object matching searchitem, if there.

        Args:
            searchitem - an object of any class stored in the BST
        """
        to_remove = self.search_node(searchitem)  # Result of search
        if to_remove:  # If the search returned something
            return to_remove.remove_node()

    def remove_node(self):
        """Remove this BSTNode from its tree, and return its element.
        Maintains the BST properties.
        """
        original_item = self._element  # Save item to return later
        parent = self._parent
        if self.full():
            max_node = self._leftchild.findmaxnode()  # Biggest item on left
            self._element = max_node._element  # Swap item with biggest item
            max_node._parent._rebalance()
            max_node.remove_node()  # Remove the previous biggest item's node
        elif self.leaf():
            if parent:  # If node has a parent,
                if parent._leftchild is self:  # Set parent's child ref to None
                    parent._leftchild = None
                elif parent._rightchild is self:
                    parent._rightchild = None
            self._clear_node()  # Clear the current node
        elif not self._rightchild:
            leftchild = self._leftchild
            self._element = leftchild._element  # Move item from left to self
            if leftchild._leftchild:  # Link leftchild's leftchild to self
                self._leftchild = leftchild._leftchild
                leftchild._leftchild._parent = self
            else:
                self._leftchild = None
            if leftchild._rightchild:  # Link leftchild's rightchild to self
                self._rightchild = leftchild._rightchild
                leftchild._rightchild._parent = self
            else:
                self._rightchild = None
            leftchild._clear_node()  # Clear the node that was removed
        else:
            rightchild = self._rightchild
            self._element = rightchild._element
            if rightchild._leftchild:
                rightchild._leftchild._parent = self
                self._leftchild = rightchild._leftchild
            else:
                self._leftchild = None
            if rightchild._rightchild:
                rightchild._rightchild._parent = self
                self._rightchild = rightchild._rightchild
            else:
                self._rightchild = None
            rightchild._clear_node()  # Clear the node that was removed
        if parent:
            parent._rebalance()
        return original_item

    def _rebalance(self):
        """Check if the node needs rebalancing.

        Update the height of the current node and, if necessary, rebalance
        the tree, maintaining BST properties.
        """
        prev_height = self._height  # Save current height for comparison later
        self._height = self.height()  # Update the height of the node
        if self._unbalanced():
            if self.full():
                if self._leftchild._height > self._rightchild._height:
                    self._restructure_leftchild()  # If left causes unbalance
                else:
                    self._restructure_rightchild()
            elif self._leftchild and not self._rightchild:
                self._restructure_leftchild()
            else:
                self._restructure_rightchild()

            if self._parent:
                self._parent._rebalance()  # Rebalance the node's parent
        elif self._height != prev_height and self._parent:
            self._parent._rebalance()  # Rebalance parent if height changed

    def _restructure_leftchild(self):
        """Restructure the leftchild, doing a double rotation if necessary."""
        left = self._leftchild
        if left.full():  # If left has both children
            if left._rightchild._height > left._leftchild._height:
                left._rotate_rightchild()  # Double rotate if right unbalanced
        elif left._rightchild and not left._leftchild:
            left._rotate_rightchild()
        self._rotate_leftchild()

    def _restructure_rightchild(self):
        """Restructure the rightchild, doing a double rotation if necessary."""
        right = self._rightchild
        if right.full():  # If right has both children
            if right._leftchild._height > right._rightchild._height:
                right._rotate_leftchild()  # Double rotate if left unbalanced
        elif right._leftchild and not right._rightchild:
            right._rotate_leftchild()
        self._rotate_rightchild()

    def _rotate_leftchild(self):
        """Rotate the leftchild into the node."""
        left = self._leftchild
        self_item = self._element  # Save current item in self
        self._element = left._element  # Move item from leftchild into self
        left._element = self_item  # Move item from self into leftchild

        if left._leftchild:  # Link to self if left has leftchild
            self._leftchild = left._leftchild
            left._leftchild._parent = self  # Update parent link
        else:
            self._leftchild = None
        if left._rightchild:  # Move rightchild into leftchild
            left._leftchild = left._rightchild
        else:
            left._leftchild = None
        if self._rightchild:   # If self had a rightchild
            left._rightchild = self._rightchild  # Link to the other node
            self._rightchild._parent = left  # Update parent link
        else:
            left._rightchild = None
        self._rightchild = left   # Now link the rotated node to self
        self._height = self.height()  # Self changed position, update height
        left._height = left.height()

    def _rotate_rightchild(self):
        """Rotate the rightchild into the node."""
        right = self._rightchild
        self_item = self._element
        self._element = right._element
        right._element = self_item

        if right._rightchild:
            self._rightchild = right._rightchild
            right._rightchild._parent = self
        else:
            self._rightchild = None
        if right._leftchild:
            right._rightchild = right._leftchild
        else:
            right._rightchild = None
        if self._leftchild:
            right._leftchild = self._leftchild
            self._leftchild._parent = right
        else:
            right._leftchild = None
        self._leftchild = right
        self._height = self.height()
        right._height = right.height()

    def _unbalanced(self):
        """Check if the node is unbalanced.

        Returns:
            True if the difference between the heights of the node's children
            is greater that or equal to 2, False otherwise
        """
        if self.internal():
            if self.full():
                if abs(self._leftchild._height-self._rightchild._height) >= 2:
                    return True
            elif self._leftchild and not self._rightchild:
                if self._leftchild._height >= 2:
                    return True
            elif self._rightchild._height >= 2:
                return True
        return False

    def _clear_node(self):
        """Set all attributes in node to None."""
        self._element = None
        self._parent = None
        self._leftchild = None
        self._rightchild = None
        self._height = None
