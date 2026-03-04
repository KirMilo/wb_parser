## Basket finding

# `basket-${s}.wbbasket.ru/vol${n}`


def get_basket_num(n: int) -> str:
    switch_basket = (
        143,
        287,
        431,
        719,
        1007,
        1061,
        1115,
        1169,
        1313,
        1601,
        1655,
        1919,
        2045,
        2189,
        2405,
        2621,
        2837,
        3053,
        3269,
        3485,
        3701,
        3917,
        4133,
        4349,
        4565,
        4877,
        5189,
        5501,
        5813,
        6125,
        6437,
        6749,
        7061,
        7373,
        7685,
        7997,
        8309,
        8741,
        9173,
        9605
    )
    if n > 0:
        for i, val in enumerate(switch_basket, start=1):
            if n <= val:
                return "{:02d}".format(i)
    return "41"


def get_basket(e: int):
    n = int(e // 1e5)
    return get_basket_num(n)
