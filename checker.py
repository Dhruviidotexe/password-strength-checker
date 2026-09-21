import math
import re
from typing import Any, Dict, List


COMMON_PATTERNS = (
    "password",
    "123456",
    "12345678",
    "qwerty",
    "admin",
    "welcome",
    "letmein",
    "iloveyou",
    "monkey",
    "dragon",
)

SEQUENCES = (
    "abcdefghijklmnopqrstuvwxyz",
    "0123456789",
    "qwertyuiopasdfghjklzxcvbnm",
)


def _has_sequence(password: str, min_len: int = 4) -> bool:
    lowered = password.lower()
    for sequence in SEQUENCES:
        reverse = sequence[::-1]
        for index in range(len(sequence) - min_len + 1):
            chunk = sequence[index : index + min_len]
            if chunk in lowered or reverse[index : index + min_len] in lowered:
                return True

    for index in range(len(lowered) - min_len + 1):
        chunk = lowered[index : index + min_len]
        if all(ord(chunk[i + 1]) - ord(chunk[i]) == 1 for i in range(len(chunk) - 1)):
            return True
        if all(ord(chunk[i]) - ord(chunk[i + 1]) == 1 for i in range(len(chunk) - 1)):
            return True
    return False


def _has_excessive_repetition(password: str) -> bool:
    if re.search(r"(.)\1{3,}", password):
        return True
    if len(password) >= 8:
        unique_ratio = len(set(password)) / len(password)
        return unique_ratio <= 0.25
    return False


def _has_common_pattern(password: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]", "", password.lower())
    if not normalized:
        return False
    return any(pattern in normalized for pattern in COMMON_PATTERNS)


def _character_pool(password: str) -> int:
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[^A-Za-z0-9\s]", password):
        pool += 32
    if re.search(r"[^\x00-\x7F]", password):
        pool += 40
    return pool


def _strength_label(score: int) -> str:
    if score < 30:
        return "Very Weak"
    if score < 50:
        return "Weak"
    if score < 70:
        return "Moderate"
    if score < 85:
        return "Strong"
    return "Very Strong"


def analyze_password(password: Any) -> Dict[str, Any]:
    if not isinstance(password, str):
        password = ""

    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_number = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^A-Za-z0-9\s]", password))
    repetition = _has_excessive_repetition(password)
    sequence = _has_sequence(password)
    common = _has_common_pattern(password)
    pool = _character_pool(password)
    categories = sum([has_lower, has_upper, has_number, has_special])
    entropy = round(length * math.log2(pool), 1) if length and pool else 0.0

    score = 0
    if length >= 8:
        score += 10
    if length >= 12:
        score += 15
    if length >= 16:
        score += 10
    if has_lower:
        score += 10
    if has_upper:
        score += 10
    if has_number:
        score += 10
    if has_special:
        score += 15
    if categories >= 3:
        score += 10
    if categories == 4:
        score += 5
    if not sequence and length:
        score += 10
    if not repetition and length:
        score += 10

    if length < 8:
        score -= 25
    elif length < 12:
        score -= 10
    if length < 4 and length:
        score -= 15
    if common:
        score -= 30
    if sequence:
        score -= 20
    if repetition:
        score -= 20
    if categories <= 1 and length:
        score -= 10

    score = max(0, min(100, score))

    suggestions: List[str] = []
    if not password:
        suggestions.append("Enter a password to see a private strength breakdown.")
    if length and length < 12:
        suggestions.append("Use at least 12-16 characters.")
    if length >= 12 and length < 16:
        suggestions.append("Consider 16+ characters for stronger resilience.")
    if password and not has_upper:
        suggestions.append("Consider adding uppercase letters.")
    if password and not has_lower:
        suggestions.append("Consider adding lowercase letters.")
    if password and not has_number:
        suggestions.append("Consider adding numbers.")
    if password and not has_special:
        suggestions.append("Consider adding special characters.")
    if common:
        suggestions.append("Avoid common passwords and predictable variations.")
    if sequence:
        suggestions.append("Avoid predictable sequences such as 123456 or abcdef.")
    if repetition:
        suggestions.append("Avoid repeating the same character multiple times.")
    if password and score >= 85 and not suggestions:
        suggestions.append("Your password meets the basic strength checks.")

    checks = {
        "length": length >= 12,
        "excellent_length": length >= 16,
        "lowercase": has_lower,
        "uppercase": has_upper,
        "numbers": has_number,
        "special": has_special,
        "diversity": categories >= 3,
        "repetition": repetition,
        "sequence": sequence,
        "common": common,
    }

    return {
        "score": score,
        "strength": _strength_label(score),
        "entropy": entropy,
        "character_pool": pool,
        "length": length,
        "checks": checks,
        "suggestions": suggestions,
        "disclaimer": "Password strength scores are heuristic estimates intended for educational purposes. A high score does not guarantee that a password is secure against every attack.",
    }


