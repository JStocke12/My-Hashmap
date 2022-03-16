import random
import hashlib

class MyHashMap:
    def __init__(self, radixbits=3):
        self.radix = 1<<radixbits
        self.keys = [None]*self.radix
        self.values = [None]*self.radix
        self.numitems = 0

    def __getitem__(self, key):
        keyhash = hash(key) % self.radix
        while self.keys[keyhash] is not None and self.keys[keyhash] is not key:
            keyhash += 1
            keyhash %= self.radix

        if self.keys[keyhash] is None:
            raise "key is not in dictionary"

        return self.values[keyhash]

    def __setitem__(self, key, value):
        keyhash = hash(key) % self.radix

        while self.keys[keyhash] is not None and self.keys[keyhash] is not key:
            keyhash += 1
            keyhash %= self.radix

        if self.keys[keyhash] is None and self.numitems >= self.radix>>1:
            self.rehash()
            self[key] = value
            return

        if self.keys[keyhash] is not key:
            self.numitems += 1

        self.keys[keyhash] = key
        self.values[keyhash] = value

    def __contains__(self, key):
        keyhash = hash(key) % self.radix

        while self.keys[keyhash] is not None and self.keys[keyhash] is not key:
            keyhash += 1
            keyhash %= self.radix

        return self.keys[keyhash] is key

    def rehash(self):
        newhash = MyHashMap()

        newhash.radix = self.radix<<1

        newhash.keys = [None]*newhash.radix
        newhash.values = [None]*newhash.radix

        for key in self.keys:
            if key is not None:
                newhash[key] = self[key]

        self.radix <<= 1
        self.keys = newhash.keys
        self.values = newhash.values

        

def main():
    print("Generating Keys")
    test_keys = random.sample(range(1<<32), 1<<8)
    print("Generating Values")
    test_values = random.sample(range(1<<32), 1<<8)
    print()
    test_hash = MyHashMap()

    for k, v in zip(test_keys, test_values):
        print("Inserting key {} with value {}".format(k, v))
        test_hash[k] = v
        if k not in test_hash:
            print("key {} not found!".format(k))
    print()

    for k, v in zip(test_keys, test_values):
        if k not in test_hash:
            print("key {} not found!".format(k))
    print()

    print("Key Count: {}".format(test_hash.numitems))
    print("Dictionary Size: {}".format(test_hash.radix))

    test = True
    for k,v in zip(test_keys,test_values):
        if k not in test_hash:
            print("key {} not found!".format(k))
            test = False
        elif test_hash[k] is not v:
            print("key {} has incorrect value (expected {}. found {})".format(k, v, test_hash[k]))
            test=False

    if test:
        print("Tests passed!")
    else:
        print("Tests failed. See output above.")

if __name__ == "__main__":
    main()