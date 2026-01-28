from fractions import Fraction
from collections import defaultdict

def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a / b

ops = [add, sub, mul, div]
op_symbols = ["+", "-", "*", "/"]

def fraction_to_decimal(frac: Fraction) -> str:
    sign = "-" if frac < 0 else ""
    frac = abs(frac)

    n, d = frac.numerator, frac.denominator
    integer = n // d
    rem = n % d

    if rem == 0:
        return sign + str(integer)

    digits = []
    seen = {}

    pos = 0
    while rem != 0:
        if rem in seen:
            start = seen[rem]
            non_rep = "".join(digits[:start])
            rep = "".join(digits[start:])
            return f"{sign}{integer}.{non_rep}({rep})"
        seen[rem] = pos
        rem *= 10
        digits.append(str(rem // d))
        rem %= d
        pos += 1

    return f"{sign}{integer}." + "".join(digits)

def evaluate(form, a, b, c, d, o1, o2, o3, s1, s2, s3):
    try:
        if form == 0:
            return o3(o2(o1(a, b), c), d), f"4{s1}4{s2}4{s3}4"

        elif form == 1:
            return o3(o2(o1(a, b), c), d), f"((4{s1}4){s2}4){s3}4"

        elif form == 2:
            return o3(o1(a, o2(b, c)), d), f"(4{s1}(4{s2}4)){s3}4"

        elif form == 3:
            return o1(a, o3(o2(b, c), d)), f"4{s1}((4{s2}4){s3}4)"

        elif form == 4:
            return o1(a, o2(b, o3(c, d))), f"4{s1}(4{s2}(4{s3}4))"

        elif form == 5:
            return o2(o1(a, b), o3(c, d)), f"(4{s1}4){s2}(4{s3}4)"

        elif form == 6:
            return o2(o1(o1(a, b), c), d), f"((4{s1}4){s2}4){s3}4"

        elif form == 7:
            return o1(a, o2(o2(b, c), d)), f"4{s1}((4{s2}4){s3}4)"

        elif form == 8:
            return o3(o1(a, b), o2(c, d)), f"(4{s1}4){s3}(4{s2}4)"

        elif form == 9:
            return o1(o1(a, b), o2(c, d)), f"((4{s1}4){s2}(4{s3}4))"

        elif form == 10:
            return o1(a, o1(o2(b, c), d)), f"4{s1}((4{s2}4){s3}4)"

    except ZeroDivisionError:
        return "ERROR", "ERROR"

def sort_key(result_str):
    if result_str == "ERROR":
        return (1, 0)   
    if "(" in result_str:
        return (0, float(result_str.replace("(", "").replace(")", "")))
    return (0, float(result_str))

results = defaultdict(int)

for i in range(1, 705):
    form = (i - 1) // 64
    r = (i - 1) % 64

    idx1 = r // 16
    idx2 = (r % 16) // 4
    idx3 = r % 4

    o1, o2, o3 = ops[idx1], ops[idx2], ops[idx3]
    s1, s2, s3 = op_symbols[idx1], op_symbols[idx2], op_symbols[idx3]

    value, expr = evaluate(
        form,
        Fraction(4), Fraction(4), Fraction(4), Fraction(4),
        o1, o2, o3,
        s1, s2, s3
    )

    if value == "ERROR":
        result_str = "ERROR"
    else:
        result_str = fraction_to_decimal(value)

    print(f"{i:3d} : {expr} = {result_str}")
    results[result_str] += 1

print("\n--- 集計結果（値の昇順） ---")
for k in sorted(results.keys(), key=sort_key):
    print(f"{k} : {results[k]}")
