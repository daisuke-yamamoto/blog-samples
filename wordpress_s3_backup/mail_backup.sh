#!/bin/sh
MYSQLDUMP_BIN=/usr/bin/mysqldump
MAIL_BIN=/bin/mail
ZIP_BIN=/usr/bin/zip
UUENCODE_BIN=/usr/bin/uuencode

# メールの宛先と件名
MAIL_TOADDR=<MAIL_ADDRESS>
MAIL_SUBJECT=<SUBJECT>

# バックアップの一時保存先
BACKUP_TEMPDIR=/tmp/backups/
mkdir -p $BACKUP_TEMPDIR

# ZIPファイルのパス
ZIP_OUTPUT_PATH=$BACKUP_TEMPDIR/backup-`date '+%F'`.zip
ZIP_PASS=<PASSWORD>

# MySQLのユーザ名
MYSQL_USER=<MYSQL_USERNAME>
# MySQLのホスト
MYSQL_HOST=<MYSQL_HOST>
# MySQLのパスワード
MYSQL_PASS=<MYSQL_PASSWORD>
# MySQLのDB名
MYSQL_DBNAME=<MYSQL_DBNAME>
# MySQLの、一時保存先
MYSQL_TEMPPATH=$BACKUP_TEMPDIR/dump.sql

# アップロードされた画像が保存されているディレクトリのパス
UPLOADED_IMAGE_DIR=<WORDPRESS_PATH>/wp-content/uploads/

# MySQLのバックアップを取ります。
$MYSQLDUMP_BIN -cu $MYSQL_USER -h $MYSQL_HOST --password=$MYSQL_PASS $MYSQL_DBNAME > $MYSQL_TEMPPATH

# パスワード付きで圧縮します。
$ZIP_BIN -r -P $ZIP_PASS $ZIP_OUTPUT_PATH $MYSQL_TEMPPATH $UPLOADED_IMAGE_DIR

# メールを送信します。
$UUENCODE_BIN $ZIP_OUTPUT_PATH `basename $ZIP_OUTPUT_PATH` | $MAIL_BIN -s "$MAIL_SUBJECT" $MAIL_TOADDR
