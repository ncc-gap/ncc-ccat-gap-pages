AWS EC2 の利用
--------------

AWS コンソールにログイン
~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://aws.amazon.com を web
ブラウザで開き、「コンソールにサインイン」をクリックします。

|image31|

次の画面でアカウント、ユーザ名、パスワードを入力します。

|image32|

AWS マネジメントコンソールで東京リージョンを選択しておきます。

|image33|

.. _ec2-インスタンスの起動-1:

EC2 インスタンスの起動
~~~~~~~~~~~~~~~~~~~~~~~~~

AWS マネジメントコンソールで EC2 サービスを選択します。

|image34|

EC2
ダッシュボードが表示されますので、「インスタンスの作成」ボタンを押します。

|image35|

| まず最初にマシンイメージを選択します。今回はAmazon Linux2 AMI (HVM) を使用します。
| マシンイメージ名の横にある「選択」ボタンを押します。

|image36|

| 次にインスタンスタイプを選択します。今回は m5.4xlarge を使用します。
| インスタンスタイプ名の先頭にあるチェックボックスを選択したら、ページの最後にある「次の手順」ボタンを押します。

|image37|

「インスタンスの詳細の設定」では何もせず、ページの最後にある「次の手順」ボタンを押します。

|image38|

| 「ストレージの追加」では 1T のボリュームを追加します。
| まず、「新しいボリュームの追加」ボタンを押して行を追加し、サイズを「1000」と入力します。
| 入力後、ページの最後にある「次の手順」ボタンを押します。

|image39|

| 「タグの追加」では作成するインスタンスに名前をつけます。
| 必須ではありませんが、名前がついていた方が管理しやすくなります。
| まず、「タグの追加」ボタンを押して行を追加し、キーに「Name」、値に名前
  (任意の英数字) を入力します。
| 入力後、ページの最後にある「次の手順」ボタンを押します。

|image40|

| 最後は「セキュリティグループの設定」です。
| 今回は新しくセキュリティグループを作成しますが、既存のグループがあればそちらを選択しても構いません。
| まず「セキュリティグループ名」「説明」を入力します。
| タイプ「SSH」を選択し、ソースにアクセスを許可しようとしている IP アドレスを入力します。「マイIP」を選択すると、現在の自分のIPアドレスを設定することができます。
| 入力後、ページの最後にある「確認と作成」ボタンを押します。

|image41|

確認画面が表示されますので、問題なければ「起動」ボタンを押してください。

|image42|

| キーペアの選択画面が表示されます。
| ここでは新しいキーペアを作成しますが、既存のキーペアがある場合はそちらを使用しても構いません。
| 「キーペア名」を入力し、「キーペアのダウンロード」ボタンを押します。

|image43|

今回作成するキーペアはここでしかダウンロードできません。大切に保管してください。

|image44|

キーペアをダウンロードしたら、「インスタンスの作成」ボタンを押します。

|image45|

作成ステータス画面が表示されます。「インスタンスの表示」ボタンを押します。

|image46|

| EC2 インスタンスリストが表示されます。
| 今回作成したインスタンスはまだ作成中であることが分かります。

|image47|

「チェックに合格しました」と表示されれば使用可能です。

|image48|

作成したインスタンスに SSH ログイン
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

先ほどのインスタンスリストで今回作成したインスタンスのパブリック DNS
をコピーしておきます。

|image49|

ターミナルを開きます。

1) | 先ほどダウンロードしたキーペアのパーミッションを変更します。
   | ここでは ``~/.ssh/`` の下に保存していますが、適宜読み替えてください。

2) | 次に ``ssh`` コマンドで作成したインスタンスにログインします。
   | Amazon Linux の場合、ユーザ名は ``ec2-user`` 固定です。
   | サーバのアドレスは先ほどコピーしたパブリック DNS を張り付けてください。

3) 続けますかと聞かれたら ``yes`` と入力してください。

|image50|

ログインできましたか？

work ディレクトリの準備
~~~~~~~~~~~~~~~~~~~~~~~~~~

アタッチしたディスクが存在するかを確認します。

.. code:: bash

   $ ls /dev/sdb
   /dev/sdb

フォーマットします。

.. code:: bash

   $ sudo mkfs -t ext4 /dev/sdb
   mke2fs 1.42.9 (28-Dec-2013)
   Filesystem label=
   OS type: Linux
   Block size=4096 (log=2)
   Fragment size=4096 (log=2)
   Stride=0 blocks, Stripe width=0 blocks
   65536000 inodes, 262144000 blocks
   13107200 blocks (5.00%) reserved for the super user
   First data block=0
   Maximum filesystem blocks=2409627648
   8000 block groups
   32768 blocks per group, 32768 fragments per group
   8192 inodes per group
   Superblock backups stored on blocks:
           32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
           4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968,
           102400000, 214990848

   Allocating group tables: done
   Writing inode tables: done
   Creating journal (32768 blocks): done
   Writing superblocks and filesystem accounting information: done

work ディレクトリにマウントします。

.. code:: bash

   $ sudo mkdir /work
   $ sudo mount /dev/sdb /work
   $ df -h
   Filesystem      Size  Used Avail Use% Mounted on
   devtmpfs         16G     0   16G   0% /dev
   tmpfs            16G     0   16G   0% /dev/shm
   tmpfs            16G  448K   16G   1% /run
   tmpfs            16G     0   16G   0% /sys/fs/cgroup
   /dev/nvme0n1p1  8.0G  1.2G  6.8G  15% /
   tmpfs           3.2G     0  3.2G   0% /run/user/0
   tmpfs           3.2G     0  3.2G   0% /run/user/1000
   /dev/nvme1n1    985G   77M  935G   1% /work

work ディレクトリのパーミッションを変更します。

.. code:: bash

   $ touch /work/file1
   touch: cannot touch ‘/work/file1’: Permission denied
   $ sudo chown ec2-user /work
   $ touch /work/file1
   $ ls -l /work
   total 16
   -rw-rw-r-- 1 ec2-user ec2-user     0 Jul 31 02:35 file1
   drwx------ 2 root     root     16384 Jul 31 02:28 lost+found

片付け
~~~~~~~~~

ターミナルから抜ける
^^^^^^^^^^^^^^^^^^^^^^^^

``exit`` でログアウトします。

.. code:: bash

   $ exit
   logout
   Connection to ec2-52-194-226-103.ap-northeast-1.compute.amazonaws.com closed.

インスタンスを停止する
^^^^^^^^^^^^^^^^^^^^^^^^^^

| インスタンスを起動したままでは課金対象になってしまいますので、使用しない場合は停止しておきます。
| ただし、ディスクは停止した状態であっても課金対象となりますので、無課金状態にはなりません。

※完全に削除したい場合はこの項目を飛ばして、次の 「インスタンスを削除する」に進んでください。

AWS マネジメントコンソールから作成したインスタンスを選択し、「アクション」→「インスタンスの状態」とたどって「停止」をクリックします。

|image51|

確認画面が表示されますので、停止したいインスタンスを十分に確認したら「停止する」ボタンを押します。

|image52|

停止処理が始まりました。

|image53|

完全に停止すると「stopped」と表示されます。

|image54|

インスタンスを削除する
^^^^^^^^^^^^^^^^^^^^^^^^^^

必要のないインスタンスは削除します。

AWS
マネジメントコンソールから作成したインスタンスを選択し、「アクション」→「インスタンスの状態」とたどって「終了」をクリックします。

|image55|

確認画面が表示されますので、削除したいインスタンスを十分に確認したら「はい、削除する」ボタンを押します。

|image56|

削除されたインスタンスは「terminated」と表示されます。一定期間表示されますが、その後リストからも消えます。

|image57|

| アタッチしたボリュームを削除します。
| ※インスタンス削除時、一緒に削除する設定にしていた場合はすでに削除されていますので、この操作は必要ありません。

| 左端のメニューから「ボリューム」を選択し、ボリュームを表示します。
| 今回作成したボリュームを選択した後、「アクション」→「Delete
  Volume」をクリックします。

|image58|

確認画面が表示されますので、内容を確認したら、「はい、削除する」ボタンを押します。

|image59|

| 今回作成したセキュリティグループを削除します。

| 左端のメニューから「セキュリティグループ」を選択し、セキュリティグループを表示します。
| 今回作成したセキュリティグループを選択した後、「アクション」→「セキュリティグループの削除」をクリックします。

|image60|

確認画面が表示されますので、内容を確認したら、「はい、削除する」ボタンを押します。

|image61|

今回作成したキーペアを削除します。

| 左端のメニューから「キーペア」を選択しキーペアを表示します。
| 今回作成したキーペアを選択した後、「削除」ボタンを押します。

|image62|

確認画面が表示されますので、内容を確認したら、「はい」ボタンを押します。

|image63|

.. |image31| image:: ../image/ec2_1.PNG
.. |image32| image:: ../image/ec2_2.PNG
.. |image33| image:: ../image/ec2_3.PNG
.. |image34| image:: ../image/ec2_4.PNG
.. |image35| image:: ../image/ec2_5.PNG
.. |image36| image:: ../image/ec2_6.PNG
.. |image37| image:: ../image/ec2_7.PNG
.. |image38| image:: ../image/ec2_8.PNG
.. |image39| image:: ../image/ec2_9.PNG
.. |image40| image:: ../image/ec2_10.PNG
.. |image41| image:: ../image/ec2_11.PNG
.. |image42| image:: ../image/ec2_12.PNG
.. |image43| image:: ../image/ec2_13.PNG
.. |image44| image:: ../image/ec2_14.PNG
.. |image45| image:: ../image/ec2_15.PNG
.. |image46| image:: ../image/ec2_16.PNG
.. |image47| image:: ../image/ec2_17.PNG
.. |image48| image:: ../image/ec2_18.PNG
.. |image49| image:: ../image/ec2_19.PNG
.. |image50| image:: ../image/ec2_20.PNG
.. |image51| image:: ../image/ec2_21.PNG
.. |image52| image:: ../image/ec2_22.PNG
.. |image53| image:: ../image/ec2_23.PNG
.. |image54| image:: ../image/ec2_24.PNG
.. |image55| image:: ../image/ec2_25.PNG
.. |image56| image:: ../image/ec2_26.PNG
.. |image57| image:: ../image/ec2_27.PNG
.. |image58| image:: ../image/ec2_32.PNG
.. |image59| image:: ../image/ec2_33.PNG
.. |image60| image:: ../image/ec2_28.PNG
.. |image61| image:: ../image/ec2_29.PNG
.. |image62| image:: ../image/ec2_30.PNG
.. |image63| image:: ../image/ec2_31.PNG

