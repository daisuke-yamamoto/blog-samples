jQuery(function($) {
  // 目次の非表示・表示を切り替えます。
  $('#outline > .outline_header a').click(function() {
    $ul = $('#outline > ul');
    if ($ul.is(':hidden')) {
      // 現在目次が閉じている場合
      $ul.show('fast');  // 目次を開きます。
      $(this).find('.show_text').hide();  // 非表示から表示にするテキストを隠します。
      $(this).find('.hide_text').show();  // 表示から非表示にするテキストを表示します。
    } else {
      // 現在目次が開いている場合
      $ul.hide('fast');  // 目次を隠します。
      $(this).find('.hide_text').hide();  // 表示から非表示にするテキストを隠します。
      $(this).find('.show_text').show();  // 非表示から表示にするテキストを表示します。
    }
    return false;
  });

  // 目次がクリックされた場合に、その目次の場所までスクロールさせます。
  $('#outline ul a').click(function() {
    // 移動先のオブジェクトを取得します。
    var $target = $('*[data-outline="' + $(this).attr('href') + '"]');
    if ($target.length == 0) {
      // 移動先を取得できなかった場合は処理を終了します。
      // ※正しく目次を作成できている場合は、ここには入らないはず。
      return false;
    }

    // 移動先までスクロールさせます。
    $('html, body').animate({'scrollTop': $target.offset().top}, 100);

    // 元のaタグを実行させないように、falseを返します。
    return false;
  });
})
