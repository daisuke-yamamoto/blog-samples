# coding: utf-8
import unittest
import string
import password_utils

# 使用可能な記号を並べた文字列定義します。
# ※使用可能な記号:  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~`
PASSWORD_ALLOWED_MARKS = ''.join([chr(i) for i in
                                  list(password_utils.PASSWORD_MARK_RANGE1) +
                                  list(password_utils.PASSWORD_MARK_RANGE2) +
                                  list(password_utils.PASSWORD_MARK_RANGE3) +
                                  list(password_utils.PASSWORD_MARK_RANGE4)])


class TestPasswordCheck(unittest.TestCase):
    def test_is_allowed_chars(self):
        """パスワードの入力可能文字のテストです。"""
        # 全ての半角数字、半角英字、使用可能な記号を連結した文字列を定義します。
        allowed_password = '%s%s%s' % (
            string.digits, string.ascii_letters, PASSWORD_ALLOWED_MARKS)

        self.assertTrue(password_utils.is_allowed_chars(allowed_password))
        self.assertFalse(
            password_utils.is_allowed_chars(allowed_password + '１'))
        self.assertFalse(
            password_utils.is_allowed_chars(allowed_password + 'ａ'))
        self.assertFalse(
            password_utils.is_allowed_chars(allowed_password + 'あ'))
        self.assertFalse(
            password_utils.is_allowed_chars(allowed_password + '〜'))

    def test_has_digit(self):
        # 数字以外を全て使った文字列を定義します。
        nodigit = string.ascii_letters + PASSWORD_ALLOWED_MARKS

        # 数字が含まれていないのでFalseになります。
        self.assertFalse(password_utils._has_digit(nodigit))

        for c in string.digits:
            # 数字をくっつけるとTrueになります。
            self.assertTrue(password_utils._has_digit(nodigit + c))

    def test_has_lower_letter(self):
        # 英字小文字以外を全て使った文字列を定義します。
        nolowerletter = '%s%s%s' % (
            string.digits,
            string.ascii_uppercase,
            PASSWORD_ALLOWED_MARKS)

        # 英字小文字が含まれていないのでFalseになります。
        self.assertFalse(password_utils._has_lower_letter(nolowerletter))

        for c in string.ascii_lowercase:
            # 英字小文字をくっつけるとTrueになります。
            self.assertTrue(
                password_utils._has_lower_letter(nolowerletter + c))

    def test_has_letter(self):
        # 英字大文字以外を全て使った文字列を定義します。
        noupperletter = '%s%s%s' % (
            string.digits, string.ascii_lowercase, PASSWORD_ALLOWED_MARKS)

        # 英字大文字が含まれていないのでFalseになります。
        self.assertFalse(password_utils._has_upper_letter(noupperletter))

        for c in string.ascii_uppercase:
            # 英字大文字をくっつけるとTrueになります。
            self.assertTrue(
                password_utils._has_upper_letter(noupperletter + c))

    def test_has_mark_chars(self):
        # 記号以外を全て使った文字列を定義します。
        nomark = string.digits + string.ascii_letters

        # 記号が含まれていないのでFalseになります。
        self.assertFalse(password_utils._has_mark(nomark))

        for c in PASSWORD_ALLOWED_MARKS:
            # 記号をくっつけるとTrueになります。
            self.assertTrue(password_utils._has_mark(nomark + c))

    def test_is_valid_complexity(self):
        # 数字以外の、使用可能文字全てを含む文字列を定義します。
        nodigit = string.ascii_letters + PASSWORD_ALLOWED_MARKS

        # 英字小文字以外の、使用可能文字全てを含む文字列を定義します。
        nolowerletter = '%s%s%s' % (
            string.digits, string.ascii_uppercase, PASSWORD_ALLOWED_MARKS)

        # 英字大文字以外の、使用可能文字全てを含む文字列を定義します。
        noupperletter = '%s%s%s' % (
            string.digits, string.ascii_lowercase, PASSWORD_ALLOWED_MARKS)

        # 記号以外の、使用可能文字列全てを含む文字列を定義します。
        nomark = string.digits + string.ascii_letters

        # 数字を含まないのでFalseになります。
        self.assertFalse(password_utils.is_valid_complexity(nodigit))

        for c in string.digits:
            # 数字をくっつけるとTrueになります。
            self.assertTrue(password_utils.is_valid_complexity(nodigit + c))

        # 英字小文字を含まなのでFalseになります。
        self.assertFalse(password_utils.is_valid_complexity(nolowerletter))

        for c in string.ascii_lowercase:
            # 英字小文字をくっつけるとTrueになります。
            self.assertTrue(
                password_utils.is_valid_complexity(nolowerletter + c))

        # 英字大文字を含まないのでFalseになります。
        self.assertFalse(password_utils.is_valid_complexity(noupperletter))

        for c in string.ascii_uppercase:
            # 英字小文字をくっつけるとTrueになります。
            self.assertTrue(
                password_utils.is_valid_complexity(noupperletter + c))

        # 記号を含まないのでFalseになります。
        self.assertFalse(password_utils.is_valid_complexity(nomark))
        for c in PASSWORD_ALLOWED_MARKS:
            # 英字小文字をくっつけるとTrueになります。
            self.assertTrue(password_utils.is_valid_complexity(nomark + c))


if __name__ == '__main__':
    unittest.main()
