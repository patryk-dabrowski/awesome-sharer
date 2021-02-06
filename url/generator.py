import random
import string


class Generator:
    @staticmethod
    def generate(num: int = 10):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(num))
