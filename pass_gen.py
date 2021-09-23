from secrets import SystemRandom
from string import digits


class PassGen:
    _rus_alpha = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    _spec_chars = "!”#$%&’()*"
    @staticmethod
    def get_rand_pass_12_var(ind: str):
        res = ""
        for _ in range(3):
            res += SystemRandom().choice(digits)
        for _ in range(2):
            res += SystemRandom().choice(PassGen._spec_chars)
        res += SystemRandom().choice(PassGen._rus_alpha).upper()
        n = len(ind)
        p = (n * n) % 15 + (n * n * n) % 15 + 1
        res += PassGen._rus_alpha[p - 1]
        return res


if __name__ == "__main__":
    print(PassGen.get_rand_pass_12_var("12345"))
