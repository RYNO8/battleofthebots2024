from engine import VerboseLevel, playMatches
from strategies.onecard import Algorithm as OneCard
from strategies.grok_ryno import Algorithm as GrokRyno
# from strategies.grok_haowen import Algorithm as GrokHaowen
from strategies.v1 import Algorithm as V1
# from strategies.v2 import Algorithm as V2
from strategies.v3 import Algorithm as V3
from strategies.v4 import Algorithm as V4
from strategies.hack import Algorithm as Hack
from strategies.w1 import Algorithm as W1
# from strategies.w2 import Algorithm as W2
# from strategies.w3 import Algorithm as W3
# from strategies.w4 import Algorithm as W4
from strategies.w5 import Algorithm as W5
from strategies.w6 import Algorithm as W6
from strategies.human import Algorithm as Human
# from strategies.w1_and_w5 import Algorithm as W1_and_W5
import os, sys

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

# import random
# random.seed(10)
if __name__ == "__main__":
    # with HiddenPrints():
    if True:
        result = playMatches(
            [Human, W1, V4, W6],
            verbose=VerboseLevel.VERBOSE
        )
    print(*result, sep="\n")
    pass
