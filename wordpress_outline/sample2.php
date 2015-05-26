<?php
/**
 * 目次を作成します。
 */
function add_outline($content) {
    if (!is_single() && !is_page()) {
        // 個別記事ページと固定ページ以外には目次を表示させません。
        return $content;
    } else if (strtolower(get_post_meta(get_the_ID(), 'disable_outline', true)) == 'true') {
        // カスタムフィールド（disable_outline）にtrueが設定されている場合、目次を表示しません。
        return $content;
    }

    // 目次関連の情報を取得します。
    $outline_info = get_outline_info($content);
    $content = $outline_info['content'];
    $outline = $outline_info['outline'];

    if ($outline != '') {
        // 目次を装飾します。
        $decorated_outline = sprintf('<div id="outline"><div class="outline_header">目次 [<a href="#"><span class="hide_text">非表示</span><span class="show_text" style="display: none;">表示</span></a>]</div>%s</div>', $outline);

        // 目次を追加します。
        $shortcode_outline = '[outline]';
        if (strpos($content, $shortcode_outline) !== false) {
            // 記事内にショートコードがある場合、ショートコードを目次で置換します。
            $content = str_replace($shortcode_outline, $decorated_outline, $content);
        } else if (preg_match('/<h[1-6].*>/', $content, $matches, PREG_OFFSET_CAPTURE)) {
            // 最初のhタグの前に目次を追加します。
            $pos = $matches[0][1];
            $content = substr($content, 0, $pos) . $decorated_outline . substr($content, $pos);
        }
    }
    return $content;
}
add_filter('the_content', 'add_outline');
