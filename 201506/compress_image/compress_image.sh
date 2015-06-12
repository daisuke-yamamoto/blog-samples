#!/bin/sh
OPTIPNG_BIN=/usr/local/bin/optipng
JPEGOPTIM_BIN=/usr/local/bin/jpegoptim

# 作業用のディレクトリを定義します。
# ※最後は/で終わるようにします。
WORK_DIR=/tmp/works/image_compression/

# 圧縮対象の画像が含まれるディレクトリを定義します。
# ※最後は/で終わるようにします。
#   例) TARGET_DIR=/var/www/remotestance.com/__wp__/wp-content/uploads/
TARGET_DIR=<TARGET_DIR>

# 何日以内に更新された画像を対象とするかを定義します。
MDATE=1

# 作業用ディレクトリを作成します。
mkdir -p $WORK_DIR

# 圧縮対象のディレクトリを、作業用ディレクトリに同期させます。
rsync -avz --checksum $TARGET_DIR $WORK_DIR

# 作業用のディレクトリのPNGファイルを圧縮します。
find $WORK_DIR -name "*.png" -type f -mtime -$MDATE -exec $OPTIPNG_BIN -o7 {} \;

# 作業用ディレクトリのJPEGファイルを圧縮します。
find $WORK_DIR -name "*.jpg" -type f -mtime -$MDATE -exec $JPEGOPTIM_BIN --strip-all {} \;

# 作業用ディレクトリを、圧縮対象のディレクトリに同期させます。
rsync -avz --checksum $WORK_DIR $TARGET_DIR
