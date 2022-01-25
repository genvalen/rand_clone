"""Clone /dev/random, a CSPRNG that makes use of random real-world events to create
a hash that is impossible to reverse through brute force or back tracking.
"""
from CSPRNG import CSPRNG
from sshkeyboard import listen_keyboard

# Instantiate a CSPRNG.
csprng = CSPRNG()

# Mix, or stir, each key press into the entropy pool of the CSPRNG object.
def press(key):
    csprng.mix_pool_bytes(random_event=key)


# Main program -->
# Manual labor is required here:
#   Press random keys on keyboard for 2-3 seconds, then press enter.
#   Repeat this process a few times.
#   If enough entropy has been collected while pressing keys (>= 16 bytes), then
#       random output will be printed to the console when "enter" is pressed.
#       Otherwise, no output is printed when "enter" is pressed.
#   Press "CTR-C" to exit the program.
while True:
    listen_keyboard(on_press=press, until="enter")

    with open("/dev/tty", "a") as f:
        f.write(csprng.get_random_bytes())
