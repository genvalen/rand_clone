import hashlib


class CSPRNG:
    def __init__(
        self,
        base_entropy: str = "00000000"
        * 64,  # Simulates 512 bytes / 4096 bits of deterministic entropy
    ) -> None:
        self.MIN_ENTROPY = 16  # /dev/random reads 128 bytes at a time -- 16 is for testing
        self.entropy_pool = hashlib.sha1(base_entropy.encode("utf-8"))
        self.entropy_pool_in_bytes = self.entropy_pool.digest()  # byte version of pool
        self.entropy_count = 0

    def update_entropy_count(self) -> int:
        "Increment number of bytes available for use by 1."
        self.entropy_count += 1

    def reset_entropy_count(self) -> None:
        """Reset self.entropy_count to `0`.

        This only gets called if `get_random_bytes` has collected sufficient
        entropy to print a random bytes output on the console.
        """
        self.entropy_count = 0

    def mix_pool_bytes(self, random_event: str) -> None:
        """Mix random event (user input) into the existing entropy pool.

        Random events are passed in as a single char, converted to an
        integer using Python's ord() fucntion, serialized using Sha1, and
        then mixed into the existing entropy pool. Sha1 is not crytographially
        secure, but is reasonable and fast enough to use during each interrupt.

        Each time this method is called, `update_entropy_count` is called, too,
        to keep track of how much new entropy is collected.
        """
        self.update_entropy_count()  # Track entropy.

        try:
            random_event_numerical = str(ord(random_event))
        except:
            # This is needed because, occasionally,
            # sshkeyboard passes in more than one char at a time, causing an error.
            random_event_numerical = "0"

        new_entropy_bytes = hashlib.sha1(
            random_event_numerical.encode("utf-8")
        ).digest()
        self.entropy_pool = hashlib.sha1(self.entropy_pool_in_bytes + new_entropy_bytes)
        self.entropy_pool_in_bytes = self.entropy_pool.digest()

    def get_entropy_count(self) -> int:
        """Return amount of new entropy seen since last random bytes output."""
        return self.entropy_count

    def get_random_bytes(self) -> str:
        """Take the blake2s hash of the entropy pool and print the random ouput
        to the console *IF* 16 bytes or more of new entropy have been collected
        since the last output dump. Otherwise, block -- simulated by returning an
        empty string -- until more entropy is collected.
        """
        if self.entropy_count >= 16:
            self.reset_entropy_count()
            blake2s_hash = hashlib.blake2s(self.entropy_pool_in_bytes)

            # Mix the output back into the pool to prevent backtracking
            # attacks (where the attacker knows the state of the pool
            # plus the current outputs and attempts to find previous
            # outputs).
            self.entropy_pool = hashlib.sha1(
                self.entropy_pool_in_bytes + blake2s_hash.digest()
            )
            self.entropy_pool_in_bytes = self.entropy_pool.digest()

            # Return random output.
            return blake2s_hash.digest().decode(
                "utf-8", "ignore"  # Ignore unicode errors.
            )

        # Simulates blocking. 
        return " "
