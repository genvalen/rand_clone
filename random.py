"""Clone /dev/random, a CSPRNG that makes use of random real-world events to create
a hash that is impossible to reverse using brute force.
"""
from CSPRNG import CSPRNG
from sshkeyboard import listen_keyboard

csprng = CSPRNG()

# Collect random user input from the keyboard.
# Mix, or stir, every key press into the existing entropy pool of CSPRNG.
def press(key):
    csprng.mix_pool_bytes(random_event=key)


# Produce output only while entropy pool has the min required new entropy.
while True:
    listen_keyboard(on_press=press, until="enter")

    with open("/dev/tty", "a") as f:
        f.write(csprng.get_random_bytes())
