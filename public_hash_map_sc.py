# Author:       RangerTJ
# Due Date:     8/9/2022
# Description:  Implements a separate-chaining hash map using skeleton code provided by Oregon State University's
#               CS-261 Data Structures course.


# OSU-provided code starts here.
from HashMap.a6_include import (DynamicArray, LinkedList,
                                hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # OSU-provided code ends here.
    # ------------------------------------------------------------------ #
    # Implementation Coding Starts Here:

    def put(self, key: str, value: object) -> None:
        """
        Updates a key/value pair in the hash map. Adds the pair if it doesn't exist.
        Replaces the old pair for the key if it already exists.

        Parameter "key" refers to the key being targeted.
        Parameter "value" refers to the value paired with the input key.

        No return - modifies the underlying hash table.
        """

        # Run key through hash map to find its target index, and match to it's linked list
        target_index = self._hash_function(key) % self._capacity
        target_list = self._buckets[target_index]

        # Check if target key is in bucket already and remove if it is, or increase element count if it is not
        if target_list.contains(key) is not None:
            target_list.remove(key)
        else:
            self._size += 1

        # Insert the new element into the bucket
        target_list.insert(key, value)

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        No parameters.

        Returns an integers representing the empty bucket count.
        """

        # Tally the empty buckets in the array
        empty_buckets = 0
        for elem in range(self._capacity):
            if self._buckets[elem].length() == 0:
                empty_buckets += 1
        return empty_buckets

    def table_load(self) -> float:
        """
        Returns the hash table's load factor as a float.

        No parameters.

        Returns a float that is the result of dividing the number of elements
        in the map's array by the number of buckets in it.
        """

        # Sum up the length of all bucket lists
        key_count = 0
        for elem in range(self._capacity):
            key_count += self._buckets[elem].length()

        # Calculate the load factor and return it
        return key_count / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map without messing with capacity.

        No parameters.

        No return - modifies the underlying dynamic array.
        """

        # Replaces all array indices with empty linked lists and resets size
        for elem in range(self._capacity):
            self._buckets[elem] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the underlying dynamic array's capacity. Re-hashes all existing key/value pairs
        while keeping them in the new hash map. If the argument capacity is not prime, sets capacity to
        the next highest prime number instead.

        Parameter "new_capacity" refers to the new intended capacity for the bucket array.

        No return - modifies the underlying bucket array (aka the hash map).
        """

        # Track the new capacity, in case it needs to change and mark original map / capacity
        update_capacity = new_capacity
        old_map = self._buckets
        old_capacity = self._capacity

        # Filter out impossible capacities
        if new_capacity < 1:
            return

        # Make sure the new capacity is prime; and update it to next prime if not
        if self._is_prime(new_capacity) is False:
            update_capacity = self._next_prime(new_capacity)

        # Create new hash map based on updated capacity and bind it to bucket list / update capacity
        new_map = DynamicArray()
        for elem in range(update_capacity):
            new_map.append(LinkedList())
        self._buckets = new_map
        self._capacity = update_capacity

        # Rehash all elements in old hash map and place in new map based on re-hashed index
        for bucket in range(old_capacity):
            for old_node in old_map[bucket]:
                self.put(old_node.key, old_node.value)
                self._size -= 1                                     # Offsets not actually "adding" a new element

    def get(self, key: str) -> object:
        """
        Returns the value associated with a given key, and None if it is not in the hash map.

        Parameter "key" refers to the key being searched for.

        Returns the object searched for if it was found, None if it was not.
        """

        # Check hashmap for targeted value and return it if found
        for bucket in range(self._capacity):
            if self._buckets[bucket].contains(key) is not None:
                return self._buckets[bucket].contains(key).value

        # Return None if the key was not found
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the hash map contains a key and False if it does not.

        Parameter "key" is the key being searched for.

        Returns True or False depending on whether the key was found.
        """

        # Search the hash map for the key and return True if it was found
        for bucket in range(self._capacity):
            if self._buckets[bucket].contains(key) is not None:
                return True

        # Return False if the key was not found
        return False

    def remove(self, key: str) -> None:
        """
        Removes the targeted key and its value from the hash map.
        Does nothing if key doesn't exist.

        Parameter "key" is the key being searched for.

        No return - modifies the hash map.
        """

        # Run key through hash map to find its target index, and match to it's linked list
        target_index = self._hash_function(key) % self._capacity
        target_list = self._buckets[target_index]

        # Check if target key is in bucket already and remove if it is
        if target_list.contains(key) is not None:
            target_list.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a key/value pair tuple stored in the hash map.

        No parameter.

        Returns a dynamic array consisting of key/value tuples.
        """

        # Create the new array to be returned
        key_val_array = DynamicArray()

        # Rehash all elements in old hash map and place in new map based on re-hashed index
        for bucket in range(self._capacity):
            for node in self._buckets[bucket]:
                key_val_array.append((node.key, node.value))

        # Returns the new array
        return key_val_array

    def get_hash(self, key: str) -> int:
        """
        Returns the hash value of the key input, using this object's defined hash function.

        Key parameter refers to the key to be hashed.

        Returns the hash value of the input key.
        """

        # Return the hashed index value for the input key
        return self._hash_function(key) % self._capacity

    def get_list(self, index: int) -> LinkedList:
        """
        Returns the linked list found at a given index in the hash map.

        Parameter  index refers to the index that we want to access the list for.

        Returns the linked list at the targeted index.
        """

        # Returns the linked list at the targeted index
        return self._buckets[index]

    def key_val_mode_helper(self, key: str) -> None:
        """
        Helper function for use when the hash map is storing counting information
        for mode calculations. Increases the value for a node by 1 when called and
        moves it front of its list to reduce list iterations for frequently called keys.

        Parameter "key" refers to the key for the node to be modified.

        No return - modifies the value for a node in a bucket.
        """

        # Use the hashed index to get to the target node location
        key_index = self.get_hash(key)
        target_list = self._buckets[key_index]
        target_node = target_list.contains(key)

        # Create or update the key node and its value
        if target_node:                                             # Updates frequency and moves node to front of line
            old_value = target_node.value
            self.remove(key)
            self.put(key, old_value + 1)
        else:
            self.put(key, 1)                                        # Creates node with defaults if it doesn't exist


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives a dynamic array (not necessarily sorted) and returns a tuple containing:
        -A dynamic array comprising the mode value(s) of the array
        -An integer that represents the frequency with which the mode appeared
    Uses a hashmap intermediary to store the key and its frequency (which will be stored as a key node value).

    Parameter "da" refers to the dynamic array being analyzed.

    Returns a tuple of the mode (in array form) and its frequency as an integer.
    """

    # Initialize counting hashmap, the mode array, and the frequency of the most common element tracker
    map = HashMap()
    mode_array = DynamicArray()
    mode_freq = None

    # Iterate through initial array and tally counts of each unique element as key/value nodes in a hashmap
    for elem in range(da.length()):
        key = da[elem]
        map.key_val_mode_helper(key)                                # Create 1st entry in map, or update freq value

    # Resize hashmap to reduce chances of collisions/improve performance (since memory isn't an issue)
    map.resize_table(2 * da.length())

    # Iterate through counting hashmap, updating mode as needed
    for bucket in range(map.get_capacity()):
        current_list = map.get_list(bucket)
        for node in current_list:
            if mode_freq is None:                                   # First iteration, define start mode/frequency
                mode_array.append(node.key)
                mode_freq = node.value
            elif mode_freq == node.value:                           # If mode tied, append to mode list
                mode_array.append(node.key)
            elif mode_freq < node.value:                            # New mode: Clear array save for new mode
                mode_array = DynamicArray()
                mode_array.append(node.key)
                mode_freq = node.value

    # Return a tuple of the mode array and the frequency the mode value(s) appeared
    return mode_array, mode_freq
