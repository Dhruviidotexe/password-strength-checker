# Password Strength Checker

## Overview

Password Strength Checker is a polished Flask web application for learning what makes a password stronger or weaker. It combines a playful cybersecurity interface with practical analysis: scoring, entropy estimation, pattern detection, security checks, and personalized recommendations.

Password strength scores are heuristic estimates intended for educational purposes. A high score does not guarantee that a password is secure against every attack.

## Features

- Animated intro with blinking security eyes, a character, and a glowing yellow lightbulb
- Real-time password analysis through a Flask JSON endpoint
- 0-100 strength scoring with smooth UI animation
- Estimated entropy based on length and assumed character pool
- Length, lowercase, uppercase, number, special-character, and diversity checks
- Detection for repeated characters, predictable sequences, and common password patterns
- Personalized improvement suggestions
- Show/hide password control
- Clear/reset flow
- Responsive design for desktop, tablet, and mobile
- Privacy-focused behavior with no password storage

## Tech Stack

- Python 3
- Flask
- HTML5
- CSS3
- Vanilla JavaScript
- python -m unittest

## How It Works

The frontend sends the current password to `POST /analyze` and receives only analysis results. The backend never returns the original password. The browser updates the strength meter, score, checks, entropy, and suggestions in real time.

## Password Strength Logic

The score starts from positive signals:

- 8+ characters
- 12+ characters
- 16+ characters
- Lowercase letters
- Uppercase letters
- Numbers
- Special characters
- Character diversity
- No obvious sequence
- No excessive repetition

Penalties are applied for very short passwords, common password patterns, predictable sequences, excessive repetition, and low character diversity.

## Entropy Calculation

Entropy is estimated with:

```text
password_length * log2(character_set_size)
```

The character set size is estimated from detected categories:

- Lowercase: 26
- Uppercase: 26
- Numbers: 10
- Special characters: about 32
- Unicode characters: additional estimated range

Entropy estimates how unpredictable a password is based on assumptions. It is not a guaranteed real-world cracking prediction.

## Security Concepts

Brute-force attacks try many possible combinations until one works. Longer passwords with larger character pools increase the number of guesses required.

Dictionary attacks try known words, leaked passwords, and common variations. This project flags a small local list of common password patterns such as `password`, `qwerty`, `admin`, and `letmein`.

Character diversity can increase the assumed search space, but predictable structure still matters.

Pattern-based attacks exploit sequences such as `123456`, keyboard runs, and repeated characters.

## Security & Privacy

This project does not:

- Store passwords in a database
- Store passwords in files
- Log passwords
- Store passwords in localStorage
- Store passwords in sessionStorage
- Send passwords to analytics
- Send passwords to third-party services
- Include passwords in API responses

Security headers are added by Flask, and the app renders user-provided information safely through text-only DOM updates.

## Project Structure

```text
password-strength-checker/
├── app.py
├── checker.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── tests/
    └── test_checker.py
```

## Installation

```bash
git clone <repository-url>
cd password-strength-checker
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Usage

Type a password into the analyzer. The app updates the score, meter, checks, entropy estimate, and suggestions as you type. Use the eye button to show or hide the password, and use Clear to reset the analysis.

## Testing

```bash
python -m unittest
```

The tests cover weak, moderate, strong, empty, long, numeric, alphabetic, special-character, repeated, sequential, common-pattern, and Unicode passwords.

## Future Improvements

- Secure password generator
- Larger common-password dataset
- Privacy-preserving breach checking
- Passphrase analysis
- More advanced pattern detection
- Rate limiting
- Accessibility improvements
- Advanced security testing
- Password policy checker

