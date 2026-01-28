from fractions import Fraction
from collections import defaultdict

# ==============================
# 循環小数を ( ) 付きで文字列化
# ==============================
def fraction_to_decimal(frac: Fraction) -> str:
    sign = "-" if frac < 0 else ""
    frac = abs(frac)

    n, d = frac.numerator, frac.denominator
    integer = n // d
    rem = n % d

    # 割り切れる場合
    if rem == 0:
        return sign + str(integer)

    digits = []
    seen = {}  # 余り → 位置

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

    # 循環しなかった場合（理論上ほぼ出ない）
    return f"{sign}{integer}." + "".join(digits)


# ==============================
# 括弧構造（表示と計算で完全一致）
# ==============================
forms = [
    "A o1 B o2 C o3 D",          #（44 4 4）

    "(A o1 B) o2 C o3 D",        # (44)44
    "A o1 (B o2 C) o3 D",        # 4(44)4
    "A o1 B o2 (C o3 D)",        # 44(44)
    "(A o1 B o2 C) o3 D",        # (444)4
    "A o1 (B o2 C o3 D)",        # 4(444)
    "((A o1 B) o2 C) o3 D",      # ((44)4)4
    "(A o1 (B o2 C)) o3 D",      # (4(44))4
    "A o1 ((B o2 C) o3 D)",      # 4((44)4)
    "A o1 (B o2 (C o3 D))",      # 4(4(44))
    "(A o1 B) o2 (C o3 D)",      # (44)(44)
]

# 演算子
op_symbols = ["+", "-", "*", "/"]

results = defaultdict(int)

count = 0

# ==============================
# 全探索
# ==============================
for form_idx, form in enumerate(forms):
    for i in range(64):
        # 64通りの演算子選択
        o1 = op_symbols[i // 16]
        o2 = op_symbols[(i % 16) // 4]
        o3 = op_symbols[i % 4]

        # Fraction 用の数値トークン
        A = "Fraction(4)"
        B = "Fraction(4)"
        C = "Fraction(4)"
        D = "Fraction(4)"

        # 式文字列生成（表示と計算で共通）
        expr = (
            form
            .replace("A", A)
            .replace("B", B)
            .replace("C", C)
            .replace("D", D)
            .replace("o1", o1)
            .replace("o2", o2)
            .replace("o3", o3)
        )

        count += 1

        # 評価
        try:
            value = eval(expr)
            result_str = fraction_to_decimal(value)
        except ZeroDivisionError:
            result_str = "ERROR"

        # 表示用（Fraction を 4 に戻す）
        display_expr = expr.replace("Fraction(4)", "4")

        print(f"{count:3d} : {display_expr} = {result_str}")
        results[result_str] += 1


# ==============================
# 並び替え用キー（値の昇順）
# ==============================
def sort_key(s):
    if s == "ERROR":
        return (1, 0)
    if "(" in s:
        return (0, float(s.replace("(", "").replace(")", "")))
    return (0, float(s))


# ==============================
# 集計結果出力
# ==============================
print("\n--- 集計結果（値の昇順） ---")
for k in sorted(results.keys(), key=sort_key):
    print(f"{k} : {results[k]}")
