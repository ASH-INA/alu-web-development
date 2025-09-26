#!/usr/bin/env python3
"""
LRU Cache Module
Implements a Least Recently Used caching system
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache class that implements a Least Recently Used caching system
    Discards the least recently accessed item when the cache is full
    """

    def __init__(self):
        """Initialize the LRU cache"""
        super().__init__()
        self.access_order = []  # Track access order (most recent at end)

    def put(self, key, item):
        """
        Add an item to the cache using LRU algorithm

        Args:
            key: Key to identify the item
            item: Value to be stored in cache
        """
        if key is not None and item is not None:
            # If key exists, remove from current position
            if key in self.cache_data:
                self.access_order.remove(key)
            # If cache is full and key is new, remove LRU item
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lru_key = self.access_order.pop(0)
                del self.cache_data[lru_key]
                print(f"DISCARD: {lru_key}")

            # Add key to end (most recent)
            self.access_order.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """
        Retrieve an item from the cache by key and update access order

        Args:
            key: Key to identify the item

        Returns:
            The value associated with the key, or None if not found
        """
        if key is None or key not in self.cache_data:
            return None

        # Move key to end (most recent)
        self.access_order.remove(key)
        self.access_order.append(key)
        return self.cache_data.get(key)


if __name__ == "__main__":
    """Test the LRUCache"""
    my_cache = LRUCache()
    my_cache.put("A", "Hello")
    my_cache.put("B", "World")
    my_cache.put("C", "Holberton")
    my_cache.put("D", "School")
    my_cache.print_cache()
    print(my_cache.get("B"))
    my_cache.put("E", "Battery")
    my_cache.print_cache()
    my_cache.put("C", "Street")
    my_cache.print_cache()
    print(my_cache.get("A"))
    print(my_cache.get("B"))
    print(my_cache.get("C"))
    my_cache.put("F", "Mission")
    my_cache.print_cache()
    my_cache.put("G", "San Francisco")
    my_cache.print_cache()
    my_cache.put("H", "H")
    my_cache.print_cache()
    my_cache.put("I", "I")
    my_cache.print_cache()
    my_cache.put("J", "J")
    my_cache.print_cache()
    my_cache.put("K", "K")
    my_cache.print_cache()
