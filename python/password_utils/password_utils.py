# coding: utf-8
import re

# 「 （スペース）」〜「/」までの範囲を定義します。
PASSWORD_MARK_RANGE1 = range(0x20, 0x2f + 1)
# 「:」〜「@」までの範囲を定義します。
PASSWORD_MARK_RANGE2 = range(0x3a, 0x40 + 1)
# 「[」〜「`」までの範囲を定義します。
PASSWORD_MARK_RANGE3 = range(0x5b, 0x60 + 1)
# 「{」〜「~」までの範囲を定義します。
PASSWORD_MARK_RANGE4 = range(0x7b, 0x7e + 1)


def is_allowed_chars(password):
    """
    パスワードに使用可能文字かをチェックします。
    Args:
        チェック対象のパスワード
    Returns:
        全ての文字がパスワードとして使用可能ならTrue
    """
    # 全ての文字が「 （スペース）」〜「~」までの範囲内かをチェックします。
    m = re.search(r'^[\x20-\x7E]+$', password)
    return True if m else False


def _has_digit(password):
    """
    パスワードに半角数字が含まれるかをチェックします。
    Args:
        チェック対象のパスワード
    Returns:
        半角数字を含んでいればTrue
    """
    m = re.search(r'[0-9]', password)
    return True if m else False


def _has_lower_letter(password):
    """
    パスワードに英字小文字が含まれるかをチェックします。
    Args:
        チェック対象のパスワード
    Returns:
        英字小文字を含んでいればTrue
    """
    m = re.search(r'[a-z]', password)
    return True if m else False


def _has_upper_letter(password):
    """
    パスワードに英字大文字が含まれるかをチェックします。
    Args:
        チェック対象のパスワード
    Returns:
        英字大文字を含んでいればTrue
    """
    m = re.search(r'[A-Z]', password)
    return True if m else False


def _has_mark(password):
    """
    パスワードに記号が含まれるかをチェックします。
    Args:
        チェック対象のパスワード
    Returns:
        記号を含んでいればTrue
    """
    def range_to_pattern(r):
        """
        rangeから、その範囲に一致させるための正規表現のパターンを取得します。
        例）「range(0x20, 0x2f + 1)」から「[\x20-\x2f]」を取得します。
        """
        return r'[\x%x-\x%x]' % (r[0], r[-1])
        '''
        start, end = [hex(i).replace('0x', '\\x') for i in (r[0], r[-1])]
        print('[%s-%s]' % (start, end))
        return '[%s-%s]' % (start, end)
        '''

    p = r'(?:%s|%s|%s|%s)' % (
        range_to_pattern(PASSWORD_MARK_RANGE1),
        range_to_pattern(PASSWORD_MARK_RANGE2),
        range_to_pattern(PASSWORD_MARK_RANGE3),
        range_to_pattern(PASSWORD_MARK_RANGE4))

    m = re.search(p, password)
    return True if m else False


def is_valid_complexity(password):
    """
    パスワードが十分に複雑化をチェックします。
    Args:
        password: チェック対象のパスワード
    Returns:
        半角数字・英語小文字・英語大文字・記号の全てが含まれているならTrue
    """
    if not _has_digit(password):
        # 半角数字を含んでいない場合
        return False
    if not _has_lower_letter(password):
        # 半角英字小文字を含んでいない場合
        return False
    if not _has_upper_letter(password):
        # 半角英字大文字を含んでいない場合
        return False
    if not _has_mark(password):
        # 記号を含んでいない場合
        return False
    return True
