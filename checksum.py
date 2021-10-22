class Checksum:
    @staticmethod
    def checksum(text: str, max_val: int):
        return sum(map(ord, ascii(text)[1:-1])) % (max_val + 1)

    @staticmethod
    def checksum_gamma(text: str, a: int, b: int, c: int, t0: int, max_val: int):
        x = list(map(ord, ascii(text)[1:-1]))
        t = [t0]
        for i in range(len(x)):
            t.append((a * t[-1] + b) % c)
        return sum(map(lambda xt: xt[0] ^ xt[1], zip(x, t[1:]))) % (max_val + 1)
