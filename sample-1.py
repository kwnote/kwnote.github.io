
from pyhwpx import Hwp
import re

def transform_equation(eq_str: str) -> str:
    r"""
    0) 백틱(`) 제거
    1) 앞뒤 따옴표(' 또는 ") 제거
    2) \r, \n 등 개행문자 제거
    3) sqrt -> \sqrt
    4) { ... } over { ... } -> \frac{...}{...}
    5) prime -> '
    6) 그리스 문자 변환 (소문자/대문자 + _, ^, 또는 단독)
    7) left / right -> \left / \right (대소문자 무시)
    8) leq / geq / times -> \leq / \geq / \times (대소문자 무시)
    """

    # 0) 백틱(`) 제거
    eq_str = eq_str.replace("`", "")

    # 1) 앞뒤 따옴표(' 또는 ") 제거
    eq_str = eq_str.strip("'\"")

    # 2) \r, \n 등 개행문자 제거
    eq_str = eq_str.replace("\r\n", "").replace("\n", "").replace("\r", "")

    # 3) sqrt -> \sqrt
    eq_str = eq_str.replace("sqrt", r"\sqrt")

    # 4) { ... } over { ... } -> \frac{...}{...}
    eq_str = re.sub(
        r"\{\s*([^}]*)\}\s*over\s*\{\s*([^}]*)\}",
        r"\\frac{\1}{\2}",
        eq_str
    )

    # 5) prime -> '
    eq_str = eq_str.replace("prime", "'")

    # 6) 그리스 문자 처리

    # (A) 소문자 목록
    greek_lower = [
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta",
        "eta", "theta", "iota", "kappa", "lambda", "mu",
        "nu", "xi", "omicron", "pi", "rho", "sigma", "tau",
        "upsilon", "phi", "chi", "psi", "omega"
    ]
    # (B) 대문자 목록
    greek_upper = [
        "ALPHA", "BETA", "GAMMA", "DELTA", "EPSILON", "ZETA",
        "ETA", "THETA", "IOTA", "KAPPA", "LAMBDA", "MU",
        "NU", "XI", "OMICRON", "PI", "RHO", "SIGMA", "TAU",
        "UPSILON", "PHI", "CHI", "PSI", "OMEGA"
    ]

    # 길이가 긴 것부터 치환 (부분 문자열 충돌 방지)
    greek_lower.sort(key=len, reverse=True)
    greek_upper.sort(key=len, reverse=True)

    # --- 대문자 그리스 문자 ---
    # 1) 대문자 + underscore
    for letter in greek_upper:
        # 예: "PHI_" -> "\Phi_"
        #     그룹핑해서 _ 뒤에 어떤 문자가 와도 유지 (phi_i => \phi_i)
        pattern = rf"\b({letter})_"
        replacement = rf"\\{letter.capitalize()}_"
        eq_str = re.sub(pattern, replacement, eq_str, flags=re.IGNORECASE)

    # 2) 대문자 + caret(^)
    for letter in greek_upper:
        # 예: "PHI^" -> "\Phi^"
        pattern = rf"\b({letter})\^"
        replacement = rf"\\{letter.capitalize()}^"
        eq_str = re.sub(pattern, replacement, eq_str, flags=re.IGNORECASE)

    # 3) 대문자 단독
    for letter in greek_upper:
        # 예: "PHI" -> "\Phi"
        pattern = rf"\b({letter})\b"
        replacement = rf"\\{letter.capitalize()}"
        eq_str = re.sub(pattern, replacement, eq_str, flags=re.IGNORECASE)

    # --- 소문자 그리스 문자 ---
    # 4) 소문자 + underscore
    for letter in greek_lower:
        # 예: "phi_" -> "\phi_"
        pattern = rf"\b({letter})_"
        replacement = rf"\\{letter}_"
        eq_str = re.sub(pattern, replacement, eq_str, flags=re.IGNORECASE)

    # 5) 소문자 + caret(^)
    for letter in greek_lower:
        # 예: "phi^" -> "\phi^"
        pattern = rf"\b({letter})\^"
        replacement = rf"\\{letter}^"
        eq_str = re.sub(pattern, replacement, eq_str, flags=re.IGNORECASE)

    # 6) 소문자 단독
    for letter in greek_lower:
        # 예: "phi" -> "\phi"
        pattern = rf"\b({letter})\b"
        replacement = rf"\\{letter}"
        eq_str = re.sub(pattern, replacement, eq_str, flags=re.IGNORECASE)

    # 7) left / right -> \left / \right (대소문자 무시)
    eq_str = re.sub(r"(?i)\bleft\b",  r"\\left",  eq_str)
    eq_str = re.sub(r"(?i)\bright\b", r"\\right", eq_str)

    # 8) leq / geq / times -> \leq / \geq / \times (대소문자 무시)
    eq_str = re.sub(r"(?i)\bleq\b",   r"\\leq",   eq_str)
    eq_str = re.sub(r"(?i)\bgeq\b",   r"\\geq",   eq_str)
    eq_str = re.sub(r"(?i)\btimes\b", r"\\times", eq_str)

    return eq_str

# 간단 테스트 예시
if __name__ == "__main__":
    sample_list = [
        "LEFT ( － {4,000} over {273＋T( DELTA `t  _{i} )} ＋13.65 RIGHT )",
        "LEFT [ {9} over {2} RIGHT ]",  
        "alpha", 
        "prime", 
        "sqrt(4)", 
        "beta prime eta",  
        "   \r\n   theta   \r\n",
        "a leq b",    # leq -> \leq
        "x geq 3",    # geq -> \geq
        "DELTA, GAMMA, OMEGA",  # 대문자 그리스 변환
    ]
    
    converted_list = [transform_equation(s) for s in sample_list]
    for before, after in zip(sample_list, converted_list):
        print(f"입력 :  {repr(before)}")
        print(f"출력 :  {repr(after)}")
        print("-"*60)
