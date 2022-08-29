# Author:       Raptor2k1
# Due Date:     8/9/2022
# Description:  Implements an open address hash map using quadratic probing based on provided dynamic arrays.
#               Uses skeleton code provided by Oregon State University's CS-261 Data Structures course.

# MAKE SURE TO ADD QUADRATIC PROBING  IN GET AND CONTAINS KEY METHODS


from HashMap.a6_include import (DynamicArray, HashEntry,
                                hash_function_1, hash_function_2)


# OSU-provided code starts here.
class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

        No return value - modifies the underlying hash table.
        """

        # Resize the array if load factor is >= 0.5 (double -> prime)
        if self.table_load() > 0.5:
            self.resize_table(2 * self._capacity)                   # Resize makes it next prime of doubled, if needed

        # Generate the hashed key's index and start quadratic probing until empty space found
        og_hash_index = self._hash_function(key) % self._capacity
        cur_hash_index = og_hash_index
        quad_factor = 1
        while self._buckets[cur_hash_index] and self._buckets[cur_hash_index].is_tombstone is False:

            # Over-write key data and end method if matching key found
            if self._buckets[cur_hash_index].key == key:
                self._buckets[cur_hash_index] = HashEntry(key, value)
                return

            # Continue iteration otherwise
            cur_hash_index = (og_hash_index + quad_factor**2) % self._capacity
            quad_factor += 1

        # If match not found and the space is vacant/tombstone, place value and increase array size
        self._buckets[cur_hash_index] = HashEntry(key, value)
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the hash table's load factor as a float.

        No parameters.

        Returns a float that is the result of dividing the number of elements
        in the map's array by the number of buckets in it.
        """

        # Count all array entries, ignoring empty spaces and tombstones
        key_count = 0
        for elem in range(self._capacity):
            if self._buckets[elem]:
                key_count += 1

        # Calculate the load factor and return it
        return key_count / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        No parameters.

        Returns an integers representing the empty bucket count.
        """

        # Tally the empty buckets in the array
        empty_buckets = 0
        for elem in range(self._capacity):
            if self._buckets[elem] is None:
                empty_buckets += 1
        return empty_buckets

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
        if new_capacity < self._capacity - self.empty_buckets():
            return

        # Make sure the new capacity is prime; and update it to next prime if not
        if self._is_prime(new_capacity) is False:
            update_capacity = self._next_prime(new_capacity)

        # Create new, empty hash map based on updated capacity and bind it to bucket list / update capacity
        new_map = DynamicArray()
        for elem in range(update_capacity):
            new_map.append(None)                                    # Add null data sets to build desired size array
        self._buckets = new_map
        self._capacity = update_capacity
        self._size = 0                                              # Resets size, since we'll add things back

        # Rehash all elements in old hash map and place in new map based on re-hashed index
        for bucket in range(old_capacity):
            if old_map[bucket]:
                self.put(old_map[bucket].key, old_map[bucket].value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with a given key, and None if it is not in the hash map.

        Parameter "key" refers to the key being searched for.

        Returns the object searched for if it was found, None if it was not.
        """

        # Check hashmap for targeted key and return its value if found (and not a tombstone)
        for bucket in range(self._capacity):
            if self._buckets[bucket]:
                if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone is False:
                    return self._buckets[bucket].value

        # Return None if the key was not found
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the hash map contains a key and False if it does not.

        Parameter "key" is the key being searched for.

        Returns True or False depending on whether the key was found.
        """

        # Search the hash map for the key and return True if it was found (and not a tombstone)
        for bucket in range(self._capacity):
            if self._buckets[bucket]:
                if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone is False:
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

        # Note the target key's original hash index and start quadratic probing until key or empty space found
        og_del_index = self._hash_function(key) % self._capacity
        del_index = og_del_index

        quad_factor = 1
        while self._buckets[del_index]:

            # If the key is found (and not already a tomb), set the tombstone flag, reduce size and end iteration
            if self._buckets[del_index].key == key:
                if self._buckets[del_index].is_tombstone is True:
                    return
                else:
                    self._buckets[del_index].is_tombstone = True
                    self._size -= 1
                    return

            # Continue iteration otherwise
            del_index = (og_del_index + quad_factor**2) % self._capacity
            quad_factor += 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing capacity.

        No parameters.

        No return - modifies the underlying dynamic array.
        """

        # Re-create an empty bucket array with the same capacity and reset size
        self._buckets = DynamicArray()
        for elem in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

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
            if self._buckets[bucket] and self._buckets[bucket].is_tombstone is False:
                key_val_array.append((self._buckets[bucket].key, self._buckets[bucket].value))

        # Returns the new array
        return key_val_array
