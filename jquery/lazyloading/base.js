$(function() {
  // 位置データを格納する連想配列を定義します。
  // key: imgタグが設置されている、画面上部からの位置
  // value: jQueryオブジェクト（imgタグ）を格納した配列
  var posData = null;
  var makePosData = function() {
    // 位置データを組み立てます。
    var posData = {}
    $.each($('img.lazyload'), function() {
      var $img = $(this);
      var pos = $img.offset().top;  // 画面上部からの位置を取得します。
      if (!(pos in posData)) {
        // posDataにキーがなければ空の配列を設定します。
        posData[pos] = [];
      }
      // 配列にimgオブジェクトを追加します。
      posData[pos].push($img);
    });
    return posData;
  }
  posData = makePosData();

  // ウィンドウがスクロールしたときなどの処理を定義します。
  // 処理内容は、「対象のimgタグが画面内に出現したらappearedイベントを発生」です。
  // ※「対象のimgタグ」は、posDataに含まれる、lazyloadクラスを持ったimgタグです。
  $(window).bind('load scroll resize', function() {
    // ブラウザの下端の位置を取得します。
    var windowBottom = $(this).scrollTop() + $(this).height();

    // posDataに含まれる位置でループします。
    var keys = Object.keys(posData);
    for (var idx1 = 0; idx1 < keys.length; idx1++) {
      var pos = keys[idx1];
      if (pos <= windowBottom) {
        // ブラウザの下端がimgタグの位置以上、つまりimgタグが画面に出現した場合

        // appearedを発生させる、imgタグの配列を取得します。
        var imgList = posData[pos];

        for (var idx2 = 0; idx2 < imgList.length; idx2++) {
          // appearedを発生させます。
          imgList[idx2].trigger('appeared');
        }
      }
    }
  });

  // appearedが発生されたときに実行する処理を定義します。
  // 処理内容は、「imgタグのsrcを置き換える」です。
  $('img.lazyload').on('appeared', function() {
    var $img = $(this);  // 処理対象のimgタグのオブジェクト

    // 既に画像をロード済みかを判定します。
    if ($img.attr('data-lazyloaded') === undefined) {
      // まだ画像をロードしていない場合は、srcをdata-srcで置き換えます。
      // setTimeoutは、画像が読み込まれていることをわかりやすくするために使っています。
      // これにより、「画像に出現」から「画像読み込み」までに500ミリ秒だけ遅らせています。
      setTimeout(function() {
        $img.attr('src', $img.attr('data-src'));
      }, 500);

      // 画像ロード済みを示す属性を設定します。
      $img.attr('data-lazyloaded', true);
    }
  });

  $(window).on('resize', function() {
    posData = makePosData();
  });

});
