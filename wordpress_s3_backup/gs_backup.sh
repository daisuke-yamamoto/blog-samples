#!/bin/sh
GSUTIL_BIN=$HOME/gsutil/gsutil
MYSQLDUMP_BIN=/usr/bin/mysqldump

# 保存先のバケット名
GS_BUCKET_NAME=<BUCKET_NAME>

# MySQLのユーザ名
MYSQL_USER=<MYSQL_USERNAME>
# MySQLのホスト
MYSQL_HOST=<MYSQL_HOST>
# MySQLのパスワード
MYSQL_PASS=<MYSQL_PASSWORD>
# MySQLのDB名
MYSQL_DBNAME=<MYSQL_DBNAME>
# MySQLの、バックアップの一時保存先
MYSQL_TEMPPATH=/tmp/dump.sql
# MySQLの、S3の保存先パス
MYSQL_S3_DESTPATH=mysql/

# アップロードされた画像が保存されているディレクトリのパス
UPLOADED_IMAGE_DIR=<WORDPRESS_PATH>/wp-content/uploads/
# アップロードされた画像の、S3の保存先パス
UPLOADED_IMAGE_S3_DESTPATH=uploaded_images/

# MySQLをGoogle Cloud Storageにバックアップ
$MYSQLDUMP_BIN -cu $MYSQL_USER -h $MYSQL_HOST --password=$MYSQL_PASS $MYSQL_DBNAME > $MYSQL_TEMPPATH
$GSUTIL_BIN cp $MYSQL_TEMPPATH gs://$GS_BUCKET_NAME/$MYSQL_S3_DESTPATH

# 画像をGoogle Cloud Storageにバックアップ
$GSUTIL_BIN rsync -d -c -r $UPLOADED_IMAGE_DIR gs://$GS_BUCKET_NAME/$UPLOADED_IMAGE_S3_DESTPATH
