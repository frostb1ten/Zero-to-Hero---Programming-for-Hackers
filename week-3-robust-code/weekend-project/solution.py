# =============================================================
# SOLUTION — Week 3 Project: Password Strength Analyzer
# =============================================================
import hashlib
import random
import string
import os


class PasswordAnalyzer:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def check(self, password):
        issues = []
        score = 0

        # Length check
        if len(password) >= self.min_length:
            score += 1
        else:
            issues.append(f"Too short (min {self.min_length}, got {len(password)})")

        # Uppercase
        if any(c.isupper() for c in password):
            score += 1
        else:
            issues.append("No uppercase letter")

        # Lowercase
        if any(c.islower() for c in password):
            score += 1
        else:
            issues.append("No lowercase letter")

        # Digit
        if any(c.isdigit() for c in password):
            score += 1
        else:
            issues.append("No digit")

        # Special character
        if any(c in string.punctuation for c in password):
            score += 1
        else:
            issues.append("No special character")

        # Rating
        if score <= 2:
            rating = "Weak"
        elif score <= 4:
            rating = "Medium"
        else:
            rating = "Strong"

        # Hash
        md5 = hashlib.md5(password.encode()).hexdigest()

        return {
            "score": score,
            "max_score": 5,
            "rating": rating,
            "issues": issues,
            "hash": md5
        }


class PasswordGenerator:
    def generate(self, length=16):
        if length < 4:
            length = 4

        # Guarantee at least one of each type
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice(string.punctuation),
        ]

        # Fill the rest
        all_chars = string.ascii_letters + string.digits + string.punctuation
        for _ in range(length - 4):
            password.append(random.choice(all_chars))

        random.shuffle(password)
        return ''.join(password)


def print_banner(title):
    print("=" * 42)
    print(f"  {title}")
    print("=" * 42)


def check_password(analyzer):
    password = input("Enter password: ")
    result = analyzer.check(password)

    print(f"\n[*] Analysis for: {password}")
    print(f"    Score: {result['score']}/{result['max_score']} — {result['rating']}")

    if result['issues']:
        print("    Issues:")
        for issue in result['issues']:
            print(f"      - {issue}")
    else:
        print("    No issues found!")

    print(f"    MD5: {result['hash']}")


def generate_password(generator):
    try:
        length = int(input("Length (default 16): ").strip() or "16")
    except ValueError:
        length = 16

    password = generator.generate(length)
    print(f"\n[+] Generated: {password}")


def check_from_file(analyzer):
    filename = input("Filename: ").strip()
    if not os.path.exists(filename):
        print(f"[!] File not found: {filename}")
        return

    with open(filename, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]

    print(f"\n[*] Analyzing {len(passwords)} passwords:\n")
    for pw in passwords:
        result = analyzer.check(pw)
        print(f"  {pw:<20} {result['score']}/5 {result['rating']}")

    # Save report
    with open("password_report.txt", "w") as f:
        f.write("Password Analysis Report\n")
        f.write("=" * 50 + "\n")
        for pw in passwords:
            result = analyzer.check(pw)
            f.write(f"{pw:<20} {result['score']}/5 {result['rating']}\n")
            for issue in result['issues']:
                f.write(f"  - {issue}\n")
            f.write("\n")

    print(f"\n[+] Report saved to password_report.txt")


def main():
    analyzer = PasswordAnalyzer()
    generator = PasswordGenerator()

    print_banner("Password Strength Analyzer")

    while True:
        print("\n[1] Check a password")
        print("[2] Generate a password")
        print("[3] Check from file")
        print("[4] Quit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            check_password(analyzer)
        elif choice == "2":
            generate_password(generator)
        elif choice == "3":
            check_from_file(analyzer)
        elif choice == "4":
            print("[*] Goodbye!")
            break
        else:
            print("[!] Invalid choice")


if __name__ == "__main__":
    main()
