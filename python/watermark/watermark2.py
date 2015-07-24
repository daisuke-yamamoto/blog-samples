# coding: utf-8
from PIL import Image, ImageDraw, ImageFont

watermark = 'HELLOW'  # 透かし文字を定義します。
fontsize = 16  # 透かし文字の大きさを定義します。
opacity = 64  # 透かし文字の透明度を定義します。
color = (255, 255, 255)  # 透かし文字の色を定義します。
angle = 30  # 回転させる度数を定義します。

# 透かしを入れる画像を使って、画像オブジェクトを取得します。
base = Image.open('images/test.png').convert('RGBA')

# テキストを描画する画像オブジェクトを作成します。
# ※後ほど45度回転させたとき、元の画像と同じ大きさにしておくと隙間ができてしまいます。
#  その隙間をなくすために拡大します。
txt = Image.new('RGBA', (base.width * 3, base.height * 3), (255, 255, 255, 0))
draw = ImageDraw.Draw(txt)

# フォントを取得します。
fnt = ImageFont.truetype(font='fonts/Arial Black.ttf', size=fontsize)

# 透かし文字の横幅、縦幅を取得します。
textw, texth = draw.textsize(watermark, font=fnt)

margin_x = int(textw * 1.5)  # 透かし文字間の、X方向のマージンを定義します。
margin_y = int(texth * 3)  # 透かし文字間の、Y方向のマージンを定義します。
for i in range(int(txt.width / margin_x)):  # X方向のループ
    xpos = margin_x * i  # X方向の位置を計算します。
    for j in range(int(txt.height / margin_y)):  # Y方向のループ
        ypos = j * margin_y  # Y方向の位置を計算します。

        # テキストを描画します。
        draw.text((xpos, ypos), watermark, font=fnt, fill=color + (opacity,))

# テキストを描画した画像を回転させます。
txt = txt.rotate(angle)

# 拡大したテキスト画像を、元のサイズで切り取ります。
left, top = int((txt.width - base.width)/ 2), int((txt.height - base.height) / 2)
txt = txt.crop((left, top, left + base.width, top + base.height))

# 画像オブジェクトを重ねます。
out = Image.alpha_composite(base, txt)

# 画像を出力します。
out.save('output/test2.png', 'png', quality=95, optimize=True)
