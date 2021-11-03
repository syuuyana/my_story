# ベースイメージを指定する
FROM mysql/mysql-server:5.7

# ポートを公開
EXPOSE 3306

# リモートからファイル追加ができ、圧縮ファイルがその場で自動解凍。
# ここではmysql設定ファイルを追加。
# 引数は、ADD (src) (destination)
ADD my.cnf /etc/mysql/conf.d/my.cnf

# コマンド実行(default実行)
CMD ["mysqld"]