import unittest

from checker import analyze_password


class PasswordCheckerTests(unittest.TestCase):
    def test_very_weak_passwords(self):
        for password in ["", "abc", "123456", "password"]:
            with self.subTest(password=password):
                result = analyze_password(password)
                self.assertLessEqual(result["score"], 29)
                self.assertEqual(result["strength"], "Very Weak")
                self.assertNotIn("password", result)

    def test_weak_passwords(self):
        for password in ["password123", "hello123"]:
            with self.subTest(password=password):
                result = analyze_password(password)
                self.assertLess(result["score"], 50)
                self.assertTrue(result["checks"]["common"] or result["checks"]["sequence"] or result["length"] < 12)

    def test_moderate_password(self):
        result = analyze_password("River7Moon")
        self.assertGreaterEqual(result["score"], 30)
        self.assertLessEqual(result["score"], 69)
        self.assertTrue(result["checks"]["uppercase"])
        self.assertTrue(result["checks"]["lowercase"])
        self.assertTrue(result["checks"]["numbers"])

    def test_strong_password(self):
        result = analyze_password("River!Cloud92#Orbit")
        self.assertGreaterEqual(result["score"], 85)
        self.assertEqual(result["strength"], "Very Strong")
        self.assertGreater(result["entropy"], 90)
        self.assertFalse(result["checks"]["common"])
        self.assertFalse(result["checks"]["sequence"])
        self.assertFalse(result["checks"]["repetition"])

    def test_very_long_password_is_scored_and_bounded(self):
        result = analyze_password("A9!" * 80)
        self.assertLessEqual(result["score"], 100)
        self.assertGreater(result["entropy"], 0)

    def test_numbers_only_and_letters_only(self):
        numbers = analyze_password("849204729401")
        letters = analyze_password("justlettersforever")
        self.assertTrue(numbers["checks"]["numbers"])
        self.assertFalse(numbers["checks"]["lowercase"])
        self.assertTrue(letters["checks"]["lowercase"])
        self.assertFalse(letters["checks"]["numbers"])

    def test_special_characters_only(self):
        result = analyze_password("!@#$%^&*()_+")
        self.assertTrue(result["checks"]["special"])
        self.assertGreaterEqual(result["character_pool"], 32)

    def test_repeated_characters(self):
        result = analyze_password("Password111111")
        self.assertTrue(result["checks"]["repetition"])
        self.assertTrue(any("repeating" in item for item in result["suggestions"]))

    def test_sequential_characters(self):
        result = analyze_password("Safeabcdef9!")
        self.assertTrue(result["checks"]["sequence"])
        self.assertTrue(any("sequences" in item for item in result["suggestions"]))

    def test_common_password_variations(self):
        result = analyze_password("Password123!")
        self.assertTrue(result["checks"]["common"])
        self.assertTrue(any("common passwords" in item for item in result["suggestions"]))

    def test_unicode_characters(self):
        result = analyze_password("नमस्तेSecure42!")
        self.assertGreater(result["entropy"], 0)
        self.assertGreater(result["character_pool"], 94)

    def test_non_string_is_handled(self):
        result = analyze_password(None)
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["length"], 0)


if __name__ == "__main__":
    unittest.main()
