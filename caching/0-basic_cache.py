#!/usr/bin/env python3
"""
Basic Cache Module
Implements a basic caching system without size limits
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache class that implements a simple caching system
    without any eviction policy (no size limits)
    """

    def __init__(self):
        """Initialize the basic cache"""
        super().__init__()

    def put(self, key, item):
        """
        Add an item to the cache

        Args:
            key: Key to identify the item
            item: Value to be stored in cache
        """
        if key is not None and item is not None:
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
    """Test the BasicCache"""
    my_cache = BasicCache()
    my_cache.print_cache()
    my_cache.put("A", "Hello")
    my_cache.put("B", "World")
    my_cache.put("C", "Holberton")
    my_cache.print_cache()
    print(my_cache.get("A"))
    print(my_cache.get("B"))
    print(my_cache.get("C"))
    print(my_cache.get("D"))
    my_cache.print_cache()
    my_cache.put("D", "School")
    my_cache.put("E", "Battery")
    my_cache.put("A", "Street")
    my_cache.print_cache()
    print(my_cache.get("A"))
