ChangeLog
=========

0.48 (2022-04-11)
===================

Features:


- Python3.9のサポートを追加しました。
- toxの実行環境を、Travis CIからGitHubに変更しました。
- READMEの書式をmarkdownからreStructuredTxtに変更しました。　
- mockパッケージに関して、標準ライブラリのunitestに含まれるmockを使用するように変更しました。

Incompatible Changes:

- Python2.7のサポートを終了しました。
- Django1.11のサポートを終了しました。
- Celeryのタスク名を `Notify` から `notify` に変更しました。
