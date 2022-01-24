import hashlib


class CSPRNG:
    def __init__(
        self,
        seed: str = "00000000",
    ) -> None:
        self.MIN_ENTROPY = 16  # aka 128 bits
        self.entropy_pool = hashlib.blake2s(seed.encode("utf-8"))
        self.entropy_pool_in_bytes = self.entropy_pool.digest()
        self.entropy_count = 0

    def update_entropy_count(self):
        self.entropy_count += 1

    def mix_pool_bytes(self, random_event: str) -> None:
        self.update_entropy_count()

        random_event_numerical = str(ord(random_event))

        new_entropy_bytes = hashlib.blake2s(
            random_event_numerical.encode("utf-8")
        ).digest()

        self.entropy_pool.update(self.entropy_pool_in_bytes + new_entropy_bytes)
        self.entropy_pool_in_bytes = self.entropy_pool.digest()

    def get_entropy_count(self) -> int:
        return self.entropy_count

    def get_random_bytes(self) -> str:
        return self.entropy_pool.digest().decode(
            "utf-8", "ignore"
        )  # Ignore unicode errors.
