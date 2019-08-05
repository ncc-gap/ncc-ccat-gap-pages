Cell Ranger のインストール
-----------------------------

公式ドキュメント： `Cell Ranger Installation <https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/installation>`__

AWS EC2 インスタンスを起動
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AWS コンソールにログインし、EC2 インスタンスを起動します。

Cell Ranger は以下の `システム要件 <https://support.10xgenomics.com/single-cell-gene-expression/software/overview/system-requirements>`__ となっていますので、1TByte のディスクストレージ (gp2) をつけてインスタンスタイプ t3.2xlarge を選択します。

::

   System Requirements
    - 8-core Intel
    - 64GB RAM
    - 1TB free disk space
    - 64-bit CentOS/RedHat 6.0 or Ubuntu 12.04

| セキュリティグループではポート 22 番を開けておいてください。
| その他の設定はデフォルトのままで構いません。

詳細な手順は以下を参照してください。

 - `AWS EC2 を利用する場合 <./aws_ec2.html>`__
 - `AWS Cloud9 を利用する場合 <./aws_cloud9.html>`__

| EC2 インスタンスが起動したら、 SSH ログインし、アタッチしたストレージを初期化して ``/work`` ディレクトリにマウントしておきます。
| 実際に使用する場合はマウント先のディレクトリ名はなんでも構いませんが、ここでは解説の記載に合わせて ``/work`` ディレクトリとしておきます。

.. code:: bash

   mkfs -t ext4 /dev/sdb
   mkdir /work
   mount /dev/sdb /work
   cd /work/

ターミナルはこのまま使いますので、ログインしたままにしておいてください。

Cell Ranger をダウンロード
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Cell Rangerは tar ファイルとして公開されており、提供されています。
| 必要なソフトウェア依存関係をすべてまとめたもので、さまざまな Linux ディストリビューションで動作するように事前にコンパイルされていますので、インストールはこのファイルをダウンロードして解凍するだけです。
| 
| まず、 `このページ <https://support.10xgenomics.com/single-cell-gene-expression/software/downloads/latest>`__ にアクセスし、「10x Genomics End User Software License Agreement」を確認して必要事項を入力した後、「Continue to Downloads」ボタンをクリックします。
| 
| 「Continue to Downloads」ボタンをクリックすると、次のような画面が表示されます。
| 赤枠の中がダウンロードコマンドですので、すべて選択して、先ほどログインしたターミナルに張り付けて実行します。

|image0|

| ダウンロードしたファイルを解凍します。
| ファイル名のバージョンはダウンロードしたファイルに合わせてください。

.. code:: bash

   tar -xzvf cellranger-3.1.0.tar.gz

リファレンスファイルの準備
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| 1-2 で開いたダウンロード画面にリファレンスのダウンロードコマンドも表示されています。
| 赤枠の中をすべて選択して、ターミナルに張り付けて実行します。

|image1|

| 1-2 と同様にダウンロードしたファイルを解凍します。
| ファイル名のバージョンはダウンロードしたファイルに合わせてください。

.. code:: bash

   tar -xzvf refdata-cellranger-GRCh38-and-mm10-3.1.0.tar.gz

Cell Ranger にパスを通す
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cell Ranger ディレクトリを PATH に追加します。これで `cellranger` パイプラインを実行することができます。

.. code:: bash

   export PATH=/work/cellranger-3.1.0:$PATH

インストールの確認
~~~~~~~~~~~~~~~~~~~~~~~

`cellranger` パイプラインが正しくインストールされていることを確認するために ``cellranger testrun`` を実行します。

.. code:: bash

   cellranger testrun --id=tiny

以下のように表示されれば成功です。

::

   Pipestance completed successfully!

| パイプラインの実行結果は成否にかかわらず ``tiny/tiny.mri.tgz`` に出力されています。
| 10xGenomics にサポートを求めるときは次のコマンドでこのファイルを送付するようです。

::

   cellranger upload your@email.edu tiny/tiny.mri.tgz

bcl2fastq2 をインストール
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

前述までに cellranger パイプラインをインストールしましたが、イルミナの ``bcl2fastq2`` は入っていませんので、別途インストールする必要があります。

.. code:: bash

   wget http://jp.support.illumina.com/content/dam/illumina-support/documents/downloads/software/bcl2fastq/bcl2fastq2-v2-20-0-linux-x86-64.zip
   unzip bcl2fastq2-v2-20-0-linux-x86-64.zip
   sudo yum install -y bcl2fastq2-v2.20.0.422-Linux-x86_64.rpm

.. |image0| image:: ./image/download1.PNG
.. |image1| image:: ./image/download2.PNG
