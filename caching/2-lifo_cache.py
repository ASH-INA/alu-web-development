#!/usr/bin/env python3
"""
LIFO Cache Module
Implements a Last-In-First-Out caching system
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache class that implements a Last-In-First-Out caching system
    Discards the most recently added item when the cache is full
    """

    def __init__(self):
        """Initialize the LIFO cache"""
        super().__init__()
        self.keys_stack = []  # Stack to track insertion order

    def put(self, key, item):
        """
        Add an item to the cache using LIFO algorithm

        Args:
            key: Key to identify the item
            item: Value to be stored in cache
        """
        if key is not None and item is not None:
            # If cache is full and key is new, remove last inserted item
            if ((len(self.cache_data) >= BaseCaching.MAX_ITEMS) and
                (key not in self.cache_data)):
                last_key = self.keys_stack[-1]
                print(f"DISCARD: {last_key}")
                del self.cache_data[last_key]
                self.keys_stack.pop()

            # Add or update the key
            if key not in self.cache_data:
                self.keys_stack.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """
        Retrieve an item from the cache by key

        Args:
            key: Key to identify the item

        Returns:
            The value associated with the key, or None if not found
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)


if __name__ == "__main__":
    """Test the LIFOCache"""
    my_cache = LIFOCache()
    my_cache.put("A", "Hello")
    my_cache.put("B", "World")
    my_cache.put("C", "Holberton")
    my_cache.put("D", "School")
    my_cache.print_cache()
    my_cache.put("E", "Battery")
    my_cache.print_cache()
    my_cache.put("C", "Street")
    my_cache.print_cache()
    my_cache.put("F", "Mission")
    my_cache.print_cache()
    my_cache.put("G", "San Francisco")
    my_cache.print_cache()
