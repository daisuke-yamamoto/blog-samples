# coding: utf-8
from PIL import Image, ImageDraw, ImageFont

watermark = 'HELLOW WORLD'  # 透かし文字を定義します。
fontsize = 32  # 透かし文字の大きさを定義します。
opacity = 64  # 透かし文字の透明度を定義します。
color = (255, 255, 255)  # 透かし文字の色を定義します。

# 透かしを入れる画像を使って、画像オブジェクトを取得します。
base = Image.open('images/test.png').convert('RGBA')

# テキストを描画する画像オブジェクトを作成します。
txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
draw = ImageDraw.Draw(txt)

# フォントを取得します。
fnt = ImageFont.truetype(font='fonts/Arial Black.ttf', size=fontsize)

# 透かし文字の横幅、縦幅を取得します。
textw, texth = draw.textsize(watermark, font=fnt)

# 透かし文字を中央に入れます。
draw.text(((base.width - textw) / 2, (base.height - texth) / 2),
          watermark, font=fnt, fill=color + (opacity,))

# 画像オブジェクトを重ねます。
out = Image.alpha_composite(base, txt)

# 画像を出力します。
out.save('output/test1.png', 'png', quality=95, optimize=True)
