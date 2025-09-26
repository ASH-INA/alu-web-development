#!/usr/bin/env python3
"""
FIFO Cache Module
Implements a First-In-First-Out caching system
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache class that implements a First-In-First-Out caching system
    Discards the oldest item when the cache is full
    """

    def __init__(self):
        """Initialize the FIFO cache"""
        super().__init__()
        self.keys_queue = []  # To maintain insertion order

    def put(self, key, item):
        """
        Add an item to the cache using FIFO algorithm

        Args:
            key: Key to identify the item
            item: Value to be stored in cache
        """
        if key is not None and item is not None:
            # If key already exists, update it but don't change queue position
            if key not in self.cache_data:
                self.keys_queue.append(key)
            self.cache_data[key] = item

            # If cache exceeds max size, remove first item (FIFO)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                first_key = self.keys_queue.pop(0)
                del self.cache_data[first_key]
                print(f"DISCARD: {first_key}")

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
    """Test the FIFOCache"""
    my_cache = FIFOCache()
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
