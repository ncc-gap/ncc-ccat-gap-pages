2019.7.31　作成　NCC

# AWS 環境で Cell Ranger 環境を構築する

## Cell Ranger とは

Cell Ranger は single-cell の RNA-seq に対する解析パイプラインであり、Chromium single-cell RNA-seq によるシーケンスデータをアラインメントし、feature-barcode 行列を生成してクラスタリングと遺伝子発現分析を行います。  
Cell Ranger には、single-cell 遺伝子発現実験に関連する4つのパイプラインが含まれています。

 - **cellranger mkfastq** は Illumina シーケンサによって生成された Raw Base Call (BCL) ファイルを FASTQ ファイルに逆多重化します。
 - **cellranger count** は cellranger mkfastq で作成した FASTQ ファイルを使用して、アライメント、フィルタリング、バーコードカウント、および UMI カウントを実行します。 
 - **cellranger aggr** は複数回の実行結果を集約し、結合データを分析します。 
 - **cellranger reanalyze** は cellranger count または cellranger aggr によって生成された機能バーコード行列を取得し、調整可能なパラメータ設定を使用して次元削減、クラスタリング、および遺伝子発現アルゴリズムを再実行します。

これらのパイプラインは、Chromium-specific algorithms と RNA 解析に広く使用されているアラインメントルール STAR とを組み合わせたものです。   
出力は標準的なBAM, MEX, CSV, HDF5 と HTML であり、細胞情報が付与されています。

詳しくは以下を参考にしてください。

[What is Cell Ranger?](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/what-is-cell-ranger)

本文書では Cell Ranger 公式ドキュメントを参照しながら AWS インスタンス上に Cell Raner 環境を構築し、サンプルデータを cellranger count を使用して解析してみるまでを解説します。

## 目次

 - [1. Cell Ranger のインストール](#)
 - [2. cellranger mkfastq を実行してみる](./02_mkfastq.html)
 - [3. cellranger count を実行してみる](./03_count.html)
 - [Option. Cell Ranger ユーザインタフェースの利用](./99_ui.html)

## 1. Cell Ranger のインストール

公式ドキュメント：[Cell Ranger Installation](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/installation)

### 1-1. AWS EC2 インスタンスを起動する

AWS コンソールにログインし、EC2 インスタンスを起動します。

Cell Ranger は以下の [システム要件](https://support.10xgenomics.com/single-cell-gene-expression/software/overview/system-requirements) となっていますので、1TB ディスクストレージ (gp2) をつけてインスタンスタイプ t3.2xlarge を選択します。  

```
System Requirements
 - 8-core Intel
 - 64GB RAM
 - 1TB free disk space
 - 64-bit CentOS/RedHat 6.0 or Ubuntu 12.04
```

セキュリティグループではポート22番と80番を開けておいてください。  
その他の設定はデフォルトのままで構いません。

詳細な手順は以下を参照してください。

 - [AWS EC2 を利用する場合](./aws_ec2_instance.html)
 - [AWS Cloud9 を利用する場合](./aws_cloud9.html)

EC2 インスタンスが起動したら、 SSH ログインし、アタッチしたストレージを初期化して `/work` ディレクトリにマウントしておきます。  
実際に使用する場合はマウント先はなんでも構いませんが、ここでは解説の記載に合わせて `/work` ディレクトリとしておきます。

```Bash
mkfs -t ext4 /dev/sdb
mkdir /work
mount /dev/sdb /work
cd /work/
```

ターミナルはこのまま使いますので、ログインしたままにしておいてください。

### 1-2. Cell Ranger ファイルをダウンロードして解凍する

Cell Rangerは tar ファイルとして公開されており、提供されています。   
必要なソフトウェア依存関係をすべてまとめたもので、さまざまなLinuxディストリビューションで動作するように事前にコンパイルされていますので、インストールはこのファイルをダウンロードして解凍するだけです。

まず、[このページ](https://support.10xgenomics.com/single-cell-gene-expression/software/downloads/latest) にアクセスし、「10x Genomics End User Software License Agreement」を確認して必要事項を入力した後、「Continue to Downloads」ボタンをクリックします。

「Continue to Downloads」ボタンをクリックすると、次のような画面が表示されます。
赤枠の中がダウンロードコマンドですので、すべて選択して、1-1 でログインしたターミナルに張り付けて実行します。

![](../image/download1.PNG)

ダウンロードしたファイルを解凍します。  
ファイル名のバージョンはダウンロードしたファイルに合わせてください。

```Bash
tar -xzvf cellranger-3.1.0.tar.gz
```

### 1-3. リファレンスファイルをダウンロードして解凍する

1-2 で開いたダウンロード画面にリファレンスのダウンロードコマンドも表示されています。  
赤枠の中をすべて選択して、ターミナルに張り付けて実行します。

![](../image/download2.PNG)

1-2 と同様にダウンロードしたファイルを解凍します。  
ファイル名のバージョンはダウンロードしたファイルに合わせてください。

```Bash
tar -xzvf refdata-cellranger-GRCh38-and-mm10-3.1.0.tar.gz
```

### 1-4. Cell Ranger にパスを通す

Cell Ranger ディレクトリを PATH に追加します。これで `cellranger` コマンドを起動することができます。

```Bash
export PATH=/work/cellranger-3.1.0:$PATH
```

### 1-5. インストールの確認

cellranger パイプラインが正しくインストールされていることを確認するために `cellranger testrun` を実行します。

```Bash
cellranger testrun --id=tiny
```

以下のように表示されれば成功です。

```
Pipestance completed successfully!
```

パイプラインの実行結果は成否にかかわらず `tiny/tiny.mri.tgz` に出力されており、10xGenomics にサポートを求めるときは次のコマンドでこのファイルを送付するようです。

```
cellranger upload your@email.edu tiny/tiny.mri.tgz
```

## 1-6. bcl2fastq2 をインストール

前述までに cellranger パイプラインをインストールしましたが、イルミナの `bcl2fastq2` は入っていませんので、別途インストールする必要があります。

```Bash
wget http://jp.support.illumina.com/content/dam/illumina-support/documents/downloads/software/bcl2fastq/bcl2fastq2-v2-20-0-linux-x86-64.zip
unzip bcl2fastq2-v2-20-0-linux-x86-64.zip
sudo yum install -y bcl2fastq2-v2.20.0.422-Linux-x86_64.rpm
```

---

[2. cellranger mkfastq を実行してみる](./02_mkfastq.html) に進んでください。
