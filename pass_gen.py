from secrets import SystemRandom
from string import digits
from string import ascii_lowercase, ascii_uppercase
from exeptions import InvalidAlphasSetException


def rand_choice(x):
    return SystemRandom().choice(x)


class Alphas:
    rus_alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    rus_alpha_upper = rus_alpha.upper()
    eng_alpha = ascii_lowercase
    eng_alpha_upper = ascii_uppercase
    digits = digits
    spec_chars = "!”#$%&’()*"
    alphas_count = 6


class PassGen:
    @staticmethod
    def get_rand_pass_lab1(ind: str) -> str:
        res = ""
        res += "".join([rand_choice(Alphas.digits) for _ in range(2)])
        res += "".join([rand_choice(Alphas.spec_chars) for _ in range(2)])
        res += rand_choice(Alphas.rus_alpha_upper)
        n = len(ind)
        p = (n * n) % 15 + (n * n * n) % 15 + 1
        res += Alphas.rus_alpha[p - 1]
        return res

    @staticmethod
    def get_rand_pass_lab3(length: int, *alphas: str) -> str:
        if len(alphas) == 0:
            raise InvalidAlphasSetException()
        alpha = "".join(alphas)
        return "".join([rand_choice(alpha) for _ in range(length)])
