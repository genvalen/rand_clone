"""Clone /dev/random, a CSPRNG that makes use of random real-world events to create
a hash that is difficult to reverse using brute force.
"""
import hashlib

MIN_ENTROPY = 128 # should be 128 bytes, but is reduced for testing purposes, since we get input manually.
entropy_pool = hashlib.sha512()
base_entropy = b"0000000000000000000000000000000000000000000000000000000000000"
entropy_pool.update(base_entropy)
base_hash = entropy_pool.digest()

# Keep track of how many key presses (random events)
# have been collected.
entropy_counter = 0

# Collect random event and update counter.
simulated_random_event = input("Type in random chars for about 30 seconds and then press enter: ").strip()
entropy_counter += len(simulated_random_event)

# Serialize the random event, and then hash it with the current entropy_pool.
hashed_event = hashlib.sha512(simulated_random_event.encode("utf-8")).digest()
entropy_pool.update(base_hash + hashed_event)

# Update the base hash.
base_hash = entropy_pool.digest()

# Block output until enough entropy has been collected.
while entropy_counter < MIN_ENTROPY:
    simulated_random_event = input("Type in some more random chars: ").strip()
    entropy_counter += len(simulated_random_event)
    hashed_event = hashlib.sha512(simulated_random_event.encode("utf-8")).digest()
    entropy_pool.update(base_hash + hashed_event)
    base_hash = entropy_pool.digest()

print("Random output:")
with open("/dev/tty", "w") as f:
    f.write(entropy_pool.hexdigest())
