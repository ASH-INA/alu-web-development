#!/usr/bin/env python3
"""
LFU Cache Module
Implements a Least Frequently Used caching system
Uses LFU algorithm with LRU as tie-breaker for items with same frequency
"""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """
    LFUCache class that implements a Least Frequently Used caching system
    Discards the least frequently used item, with LRU as tie-breaker
    """

    def __init__(self):
        """Initialize the LFU cache"""
        super().__init__()
        self.frequency = defaultdict(int)  # Track frequency of each key
        self.min_frequency = 0  # Track the minimum frequency
        self.frequency_map = defaultdict(OrderedDict)  # Map frequency to keys in LRU order

    def _update_frequency(self, key):
        """
        Update frequency of a key and maintain frequency maps

        Args:
            key: Key to update frequency for
        """
        if key in self.frequency:
            old_freq = self.frequency[key]
            new_freq = old_freq + 1
            
            # Remove from old frequency bucket
            if key in self.frequency_map[old_freq]:
                del self.frequency_map[old_freq][key]
                # If old frequency bucket is empty and it was the min, update min frequency
                if not self.frequency_map[old_freq] and old_freq == self.min_frequency:
                    self.min_frequency += 1

            # Add to new frequency bucket (at the end for LRU order)
            self.frequency_map[new_freq][key] = None
            self.frequency[key] = new_freq
        else:
            # New key, set frequency to 1
            self.frequency[key] = 1
            self.frequency_map[1][key] = None
            self.min_frequency = 1

    def put(self, key, item):
        """
        Add an item to the cache using LFU algorithm

        Args:
            key: Key to identify the item
            item: Value to be stored in cache
        """
        if key is not None and item is not None:
            # If cache is full and key is new, evict LFU item (with LRU tie-breaker)
            if (len(self.cache_data) >= BaseCaching.MAX_ITEMS and 
                key not in self.cache_data):
                # Find the least frequently used key(s)
                lfu_keys = self.frequency_map[self.min_frequency]

                # Get the least recently used key from the LFU bucket (first key in OrderedDict)
                lru_lfu_key = next(iter(lfu_keys))

                # Remove the evicted key from all data structures
                del self.cache_data[lru_lfu_key]
                del self.frequency_map[self.min_frequency][lru_lfu_key]
                del self.frequency[lru_lfu_key]

                print(f"DISCARD: {lru_lfu_key}")

            # Add/update the item
            self.cache_data[key] = item
            self._update_frequency(key)

    def get(self, key):
        """
        Retrieve an item from the cache by key and update frequency

        Args:
            key: Key to identify the item

        Returns:
            The value associated with the key, or None if not found
        """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency since key was accessed
        self._update_frequency(key)
        return self.cache_data.get(key)


if __name__ == "__main__":
    """Test the LFUCache"""
    my_cache = LFUCache()
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
    print(my_cache.get("I"))
    print(my_cache.get("H"))
    print(my_cache.get("I"))
    print(my_cache.get("H"))
    print(my_cache.get("I"))
    print(my_cache.get("H"))
    my_cache.put("J", "J")
    my_cache.print_cache()
    my_cache.put("K", "K")
    my_cache.print_cache()
    my_cache.put("L", "L")
    my_cache.print_cache()
    my_cache.put("M", "M")
    my_cache.print_cache()
