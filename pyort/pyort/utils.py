import random
import string


def short_key_generator(size=5, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
