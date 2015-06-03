$(function() {
  var $messageBox = $('#message_box');
  var $messageBoxInner = $messageBox.find('span');

  // ボタンを押せるようにします。
  $('button').removeAttr('disabled');

  $('button').click(function() {
    // 処理するURLを取得します。
    var url = './' + $(this).val() + '.json';
    // 保存中のメッセージを表示します。
    requestStart('保存中...');

    // 非同期でリクエストを投げます。
    $.ajax({
      dataType: 'json',
      url: url,
      success: function(res) {
        if (res.is_success) {
          // 通信終了時の処理をします。
          requestEnd('保存しました。', true, 1000);
        } else {
          // 通信終了時の処理をします。
          requestEnd('保存できませんでした。', false, 5000);
        }
      }
    });
  });

  /**
    * 通信開始時の処理を行います。
    *   1. ボタンを無効にします。
    *   2. メッセージボックスのクラスをprogressにします。
    *   3. jQueryTimerを停止します。
    *   4. メッセージを設定して表示します。
    */
  function requestStart(message) {
    // ボタンを無効にします。
    $('button').attr('disabled', 'disabled');

    // メッセージの色をprogressにします。
    changeFormMessageClass('progress');

    // jQuery Timersのイベントを削除します。
    // ※ 削除しないと、次の通信の途中でメッセージが消える場合があります。
    $messageBox.stopTime();

    // メッセージを設定してから表示します。
    $messageBoxInner.text(message);
    $messageBox.fadeIn();
  }

  /**
    * 通信終了時の処理をします。
    *   1. 表示するメッセージを設定します。
    *   2. 成功、失敗に応じてクラスを設定します。
    *   3. 規定の間隔後にメッセージを非表示にします。
    *   4. ボタンを有効にします。
    */
  function requestEnd(message, isSuccess, displayDuration) {
    // メッセージを設定します。
    $messageBoxInner.text(message);

    // メッセージボックスのクラスを切り替えます。
    changeFormMessageClass(isSuccess ? 'success': 'error')

    // メッセージ表示して、規定のミリ秒後に非表示にします。
    $messageBox.oneTime(displayDuration, function() {
      $(this).fadeOut(300);
    });

    // ボタンを押せるようにします。
    $('button').removeAttr('disabled');
  }

  /**
    * メッセージボックスに設定されているクラスを変更します。
    */
  function changeFormMessageClass(className) {
    $messageBox.removeClass()
               .addClass(className);
  }
});
