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
出力は標準的な BAM, MEX, CSV, HDF5 と HTML であり、細胞情報が付与されています。

詳しくは以下を参考にしてください。

[What is Cell Ranger?](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/what-is-cell-ranger)

本文書では Cell Ranger 公式ドキュメントを参照しながら AWS インスタンス上に Cell Raner 環境を構築し、サンプルデータを cellranger count を使用して解析してみるまでを解説します。

## 1. Cell Ranger のインストール

公式ドキュメント：[Cell Ranger Installation](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/installation)

### 1-1. AWS EC2 インスタンスを起動

AWS コンソールにログインし、EC2 インスタンスを起動します。

Cell Ranger は以下の [システム要件](https://support.10xgenomics.com/single-cell-gene-expression/software/overview/system-requirements) となっていますので、1TByte のディスクストレージ (gp2) をつけてインスタンスタイプ t3.2xlarge を選択します。  

```
System Requirements
 - 8-core Intel
 - 64GB RAM
 - 1TB free disk space
 - 64-bit CentOS/RedHat 6.0 or Ubuntu 12.04
```

セキュリティグループではポート 22 番を開けておいてください。  
その他の設定はデフォルトのままで構いません。

詳細な手順は以下を参照してください。

 - [AWS EC2 を利用する場合](./aws_ec2_instance.html)
 - [AWS Cloud9 を利用する場合](./aws_cloud9.html)

EC2 インスタンスが起動したら、 SSH ログインし、アタッチしたストレージを初期化して `/work` ディレクトリにマウントしておきます。  
実際に使用する場合はマウント先のディレクトリ名はなんでも構いませんが、ここでは解説の記載に合わせて `/work` ディレクトリとしておきます。

```Bash
mkfs -t ext4 /dev/sdb
mkdir /work
mount /dev/sdb /work
cd /work/
```

ターミナルはこのまま使いますので、ログインしたままにしておいてください。

### 1-2. Cell Ranger ファイルをダウンロード

Cell Rangerは tar ファイルとして公開されており、提供されています。   
必要なソフトウェア依存関係をすべてまとめたもので、さまざまな Linux ディストリビューションで動作するように事前にコンパイルされていますので、インストールはこのファイルをダウンロードして解凍するだけです。

まず、[このページ](https://support.10xgenomics.com/single-cell-gene-expression/software/downloads/latest) にアクセスし、「10x Genomics End User Software License Agreement」を確認して必要事項を入力した後、「Continue to Downloads」ボタンをクリックします。

「Continue to Downloads」ボタンをクリックすると、次のような画面が表示されます。
赤枠の中がダウンロードコマンドですので、すべて選択して、1-1 でログインしたターミナルに張り付けて実行します。

![](../image/download1.PNG)

ダウンロードしたファイルを解凍します。  
ファイル名のバージョンはダウンロードしたファイルに合わせてください。

```Bash
tar -xzvf cellranger-3.1.0.tar.gz
```

### 1-3. リファレンスファイルをダウンロード

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

### 1-6. bcl2fastq2 をインストール

前述までに cellranger パイプラインをインストールしましたが、イルミナの `bcl2fastq2` は入っていませんので、別途インストールする必要があります。

```Bash
wget http://jp.support.illumina.com/content/dam/illumina-support/documents/downloads/software/bcl2fastq/bcl2fastq2-v2-20-0-linux-x86-64.zip
unzip bcl2fastq2-v2-20-0-linux-x86-64.zip
sudo yum install -y bcl2fastq2-v2.20.0.422-Linux-x86_64.rpm
```

---

## 2. cellranger mkfastq の実行

この項では `cellranger mkfastq` を使用して FASTQ を生成します。

公式ドキュメント：[Generating FASTQs with cellranger mkfastq](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/mkfastq)

### 2-1. コマンドとオプション

cellranger mkfastq コマンドの基本形は以下のどちらかです

#### --csv オプションを使用する場合 (10xGenomics 推奨)

[csv サンプルはこちら](../data/cellranger-tiny-bcl-simple-1.2.0.csv)

```Bash
cellranger mkfastq --id=tiny-bcl --run=./data/cellranger-tiny-bcl-1.2.0 --csv=./data/cellranger-tiny-bcl-simple-1.2.0.csv
```

#### --samplesheet オプションを使用する場合

samplesheet とは Illumina Experiment Manager互換のサンプルシートのことであり、ファイルのパスを指定します。

[samplesheet サンプルはこちら](../data/cellranger-tiny-bcl-samplesheet-1.2.0.csv)

```Bash
cellranger mkfastq --id=tiny-bcl2 --run=./data/cellranger-tiny-bcl-1.2.0 --samplesheet=./data/cellranger-tiny-bcl-samplesheet-1.2.0.csv
```

どちらにしても --run オプションは必須であり、 Illumina BCL へのパスを指定します。

--id は出力ディレクトリ名です。必須ではありませんが明示したほうがよいでしょう。デフォルトは --run オプションで指定されるフローセルの名前です。

また、QC を実行するには --qc オプションも合わせて指定する必要があります。

その他のオプションについては 10xGenomics のドキュメント [Arguments and Options](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/mkfastq#arguments_options) を参照してください。

サンプルが提供されていますので、ダウンロードしておきます。

```Bash
cd /work
mkdir data
cd data
wget http://cf.10xgenomics.com/supp/cell-exp/cellranger-tiny-bcl-1.2.0.tar.gz
wget http://cf.10xgenomics.com/supp/cell-exp/cellranger-tiny-bcl-simple-1.2.0.csv
wget http://cf.10xgenomics.com/supp/cell-exp/cellranger-tiny-bcl-samplesheet-1.2.0.csv
```

ダウンロードしたファイルを解答します。

```Bash
tar -xzvf cellranger-tiny-bcl-1.2.0.tar.gz
```

ここまでの作業により、データは以下のように配置されているはずです。

```
/work
├── data
│         ├── cellranger-tiny-bcl-1.2.0
│         └── cellranger-tiny-bcl-simple-1.2.0.csv
│         └── cellranger-tiny-bcl-samplesheet-1.2.0.csv
└── refdata-cellranger-GRCh38-and-mm10-3.1.0
```

### 2-2. --csv オプションを使用して mkfastq を実行

`cellranger mkfastq` コマンドを実行します。

```Bash
cd /work
cellranger mkfastq --id=tiny-bcl --run=./data/cellranger-tiny-bcl-1.2.0 --csv=./data/cellranger-tiny-bcl-simple-1.2.0.csv
```

実行ログは以下のように出力されます。 `Pipestance completed successfully!` と表示されていれば成功です。

```
$ cellranger mkfastq --id=tiny-bcl --run=./data/cellranger-tiny-bcl-1.2.0 --csv=./data/cellranger-tiny-bcl-simple-1.2.0.csv
(省略)

Outputs:
- Run QC metrics:        null
- FASTQ output folder:   /work/tiny-bcl/outs/fastq_path
- Interop output folder: /work/tiny-bcl/outs/interop_path
- Input samplesheet:     /work/tiny-bcl/outs/input_samplesheet.csv

Waiting 6 seconds for UI to do final refresh.
Pipestance completed successfully!

2019-01-29 09:49:24 Shutting down.
Saving pipestance info to tiny-bcl/tiny-bcl.mri.tgz
```

全体のログは [ここ](../data/cellranger_mkfastq_tiny-bcl.log) です。

### 2-3. 実行した csv サンプルシートを確認

サンプルシートを見てみます。  
[csv サンプルはこちら](../data/cellranger-tiny-bcl-simple-1.2.0.csv)  
Lane, Sample, Index の構成になっています。  

```
$ cat /work/data/cellranger-tiny-bcl-simple-1.2.0.csv
Lane,Sample,Index
1,test_sample,SI-P03-C9
```

構成が簡単なため、10xGenomics は CSV サンプルシートを使用することを推奨しています。

| 列名  | 説明 |
|:------|:-----|
|Lane   | 処理するフローセルのレーン。単一レーン、範囲（2〜4など）、または「*」のいずれかになります。 |
|Sample | サンプルの名前。この名前は、生成されたすべての FASTQ ファイルのprefixとなり、すべてのダウンストリーム10xパイプラインの `--sample` 引数に対応します。 サンプル名は、イルミナの bcl2fastq 命名要件に準拠している必要があります。文字、数字、アンダースコア(_)、ハイフン(-)のみが許可されています。ドット(.)を含む他の記号は使用できません。 |
|Index  | ライブラリ構築に使用した 10x のサンプルインデックスセット, e.g., SI-GA-A12. |

### 2-4. --samplesheet オプションを使用して mkfastq を実行

`cellranger mkfastq` コマンドを実行します。

```Bash
cd /work
cellranger mkfastq --id=tiny-bcl2 --run=./data/cellranger-tiny-bcl-1.2.0 --samplesheet=./data/cellranger-tiny-bcl-samplesheet-1.2.0.csv
```

### 2-5. Quality Control をつけて実行

`--qc` オプションをつけて実行します。

```
cellranger mkfastq --id=tiny-bcl3 --run=./data/cellranger-tiny-bcl-1.2.0 --samplesheet=./data/cellranger-tiny-bcl-samplesheet-1.2.0.csv --qc
```

QC 出力結果と構成については 10xGenomics のドキュメント [Reading Quality Control Metrics](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/mkfastq#qc_metrics) を参照してください。

---

## 3. cellranger count を実行

この項では `cellranger count` を使用して Single-Library Analysis を行います。

公式ドキュメント：[Single-Library Analysis with Cell Ranger](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/count)

### 3-1. 簡単なサンプルで実行

順番に実行していれば 2-5 までの結果がありますので、それを使用して `cellranger count` コマンドを実行します。  

```Bash
cd /work
cellranger count --id=tiny-bcl3-count \
--transcriptome=./refdata-cellranger-GRCh38-and-mm10-3.1.0 \
--fastqs=./tiny-bcl3/outs/fastq_path \
--expect-cells=1000
```

--fastqs オプションに前回の出力結果のうち、fastq_path ディレクトリを渡します。  
--transcriptome オプションには 1-3 でダウンロードしたリファレンスファイルのディレクトリを指定します。  
--except-cells は期待されるセル数ですが、ここでは公式ドキュメントのとおり、1000とします。（デフォルトは3000です）  

その他オプションは公式ドキュメントを参照してください。
[Command Line Argument](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/count#args)

### 3-2. 現実的なデータで実行

10xgenomics は Single Cell Gene Expression Datasets を用意していますので、ダウンロードして試してみます。

https://support.10xgenomics.com/single-cell-gene-expression/datasets


上記のうち、「1k PBMCs from a Healthy Donor (v3 chemistry)」をダウンロードします。

```Bash
wget http://cf.10xgenomics.com/samples/cell-exp/3.0.0/pbmc_1k_v3/pbmc_1k_v3_fastqs.tar
tar xvf pbmc_1k_v3_fastqs.tar
```

cellranger cout を実行します。  
--fastqs にダウンロードしたサンプルの fastq ディレクトリを指定します。  
--except-cells にはサンプルのページに `run with --expect-cells=1000` と記載がありますので、1000 を指定します。

```Bash
cellranger count --id=pbmc_1k_v3 \
--transcriptome=./refdata-cellranger-GRCh38-and-mm10-3.1.0 \
--fastqs=./pbmc_1k_v3_fastqs/ \
--expect-cells=1000
```

以下はログの一部です。  
"Pipestance completed successfully!" と表示されていれば成功です。  
全体のログは [ここ](../data/cellranger_count_pbmc_1k_v3.log) にアップロードしています。

```
$ cellranger count --id=pbmc_1k_v3 \
> --transcriptome=./refdata-cellranger-GRCh38-and-mm10-3.1.0 \
> --fastqs=./pbmc_1k_v3_fastqs/ \
> --expect-cells=1000
(省略)

Outputs:
- Run summary HTML:                         /work/pbmc_1k_v3/outs/web_summary.html
- Run summary CSV:                          /work/pbmc_1k_v3/outs/metrics_summary.csv
- BAM:                                      /work/pbmc_1k_v3/outs/possorted_genome_bam.bam
- BAM index:                                /work/pbmc_1k_v3/outs/possorted_genome_bam.bam.bai
- Filtered feature-barcode matrices MEX:    /work/pbmc_1k_v3/outs/filtered_feature_bc_matrix
- Filtered feature-barcode matrices HDF5:   /work/pbmc_1k_v3/outs/filtered_feature_bc_matrix.h5
- Unfiltered feature-barcode matrices MEX:  /work/pbmc_1k_v3/outs/raw_feature_bc_matrix
- Unfiltered feature-barcode matrices HDF5: /work/pbmc_1k_v3/outs/raw_feature_bc_matrix.h5
- Secondary analysis output CSV:            /work/pbmc_1k_v3/outs/analysis
- Per-molecule read information:            /work/pbmc_1k_v3/outs/molecule_info.h5
- CRISPR-specific analysis:                 null
- Loupe Cell Browser file:                  /work/pbmc_1k_v3/outs/cloupe.cloupe

Waiting 6 seconds for UI to do final refresh.
Pipestance completed successfully!

2019-01-30 09:08:05 Shutting down.
Saving pipestance info to pbmc_1k_v3/pbmc_1k_v3.mri.tgz
```

実行ログの最後 "Outputs:" にサマリの出力場所が記載されています。

```
Run summary HTML:                         /work/pbmc_1k_v3/outs/web_summary.html
```

 [ここ](../data/pbmc_1k_v3/outs/web_summary.html) にアップロードしていますので、興味があれば参考に見てください。

---

## Option. Cell Ranger ユーザインタフェースの利用

cellranger パイプラインにはユーザインターフェースが用意されています。  

公式ドキュメント：[The Cell Ranger User Interface](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/advanced/ui)

ユーザインターフェースの場所は実行ログに記載されています。

```
$ cellranger mkfastq --id=tiny-bcl5 --run=./data/cellranger-tiny-bcl-1.2.0 --samplesheet=./cellranger-tiny-bcl-samplesheet-1.2.0.csv --qc --uiport=80
/work/cellranger-3.0.2/cellranger-cs/3.0.2/bin
cellranger mkfastq (3.0.2)
Copyright (c) 2019 10x Genomics, Inc.  All rights reserved.
-------------------------------------------------------------------------------

Martian Runtime - '3.0.2-v3.2.0'
Serving UI at http://ip-172-31-40-38:3600?auth=sAsFRDQ4tBKJ9OGNG-7gJSWwPC9_8CfG3alhmyj0BC0 # <--- ★ ここです ★

Running preflight checks (please wait)...
（以下省略）
```

AWS インスタンスで実行している、内部ネットワークアドレスが表示されていますので、外部ネットワークアドレスに読み直してアクセスします。

インスタンスの外部ネットワークアドレスは以下のようにして取得することができます。

AWS マネジメントコンソールから ec2 サービスを選択します。  
左端のメニューから「インスタンス」を選択した後、目的のインスタンスを選択します。  
右下にインスタンスの情報が記載されていますので、そこから「IPv4 パブリック IP」を探します。  
なお、内部ネットワークアドレスは「プライベート IP」という名前で記載されています。

![](../image/ec2_34.PNG)

外部ネットワークアドレスに読み替えるとユーザインターフェースの URL は以下のようになります。

http://13.58.138.49:3600?auth=sAsFRDQ4tBKJ9OGNG-7gJSWwPC9_8CfG3alhmyj0BC0

ブラウザで開くと以下のような画面が表示されます。

![](../image/pipeline_monitoring_ui.PNG)

より詳しい解説は [The Cell Ranger User Interface](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/advanced/ui) を参照してください。

---

### 注意１ セキュリティグループの変更

インスタンス起動した AWS インスタンスは無制限に全世界に公開しているわけではなくアクセス制限を行っています。今回は 22 番ポートのみ許可しています。  
そのため、新しくアクセスするためにはセキュリティグループに対してポート番号とアクセス先を指定してアクセスを許可する必要があります。  
以下の手順で設定します。  

AWS マネジメントコンソールから ec2 サービスを選択します。  
左端のメニューから「インスタンス」を選択した後、現在のインスタンスを選択します。  
右下にインスタンスの情報が記載されていますので、そこから「セキュリティグループ」のリンクをクリックします。  

![](../image/ec2_35.PNG)

セキュリティグループの画面が表示されますので、「インバウンド」→「編集」とクリックして、セキュリティグループの編集画面を表示します。  
「ルールの追加」ボタンをクリックして行を追加し、ポート番号を入力します。  
アクセスを許可する IP アドレス範囲 (「マイIP」を選択すると、現在の自分のIPアドレスを設定できます) を入力したら「保存」を押してください。

![](../image/ec2_36.PNG)

### 注意２ 公開ポートを固定

cellranger パイプラインが設定する公開ポートはランダムなため、 `--uiport=3600` のように `--uiport` オプションをつけることで固定することができます。  

ただし、Linux では TCP/IP ポート番号のうち 1024 未満は特権ポート (privileged ports) といい、特権プロセス（CAP_NET_BIND_SERVICE ケーパビリティを持つプロセス）でないとアクセスできません。  
そのため、3600 など 1024 以上のポート番号を指定したほうがよいでしょう。  

---

以上です。
不要になった AWS インスタンスは以下を参考に適宜停止するか削除してください。

 - [AWS EC2 を利用する場合](./aws_ec2_instance.html)
 - [AWS Cloud9 を利用する場合](./aws_cloud9.html)

---

## AWS Cloud9 を使用して Linux サーバを構築する

### 1. AWS コンソールにログイン

https://aws.amazon.com を web ブラウザで開き、「コンソールにサインイン」をクリックします。

![](../image/ec2_1.PNG)

次の画面でアカウント、ユーザ名、パスワードを入力します。

![](../image/ec2_2.PNG)

AWS マネジメントコンソールで東京リージョンを選択しておきます。

![](../image/ec2_3.PNG)

### 2. EC2 インスタンスの起動

AWS マネジメントコンソールで Cloud9 サービスを選択します。

![](../image/c9_1.PNG)

「Create environment」をクリックします。

![](../image/c9_2.PNG)

まず作成する cloud9 環境に名前を付けます。  
「Name」に名前 (任意の英数字) を入力し、「Next step」をクリックします。

![](../image/c9_3.PNG)

次に cloud9 環境の設定を以下内容で設定してください。  

 - Environment type: "Create a new instance for environment (EC2)" 
 - Instance type: "Other instance type" にチェックをつけて、"t3.2xlarge" を選択
 - Platform: "Amazon Linux"
 - Cost-saving setting: "After 30 minutes (Default)

入力出来たら、ページの最後にある「Next step」をクリックします。

![](../image/c9_4.PNG)

確認画面が表示されますので、問題なければ「Create environment」をクリックしてください。

![](../image/c9_5.PNG)

作成が開始されますので、黒い画面が消えるまで待ちます。

![](../image/c9_6.PNG)

このような画面が表示されれば使用可能です。

![](../image/c9_7.PNG)

### 3. ボリュームの追加

今回は 1T のボリュームが必要ですので、追加でボリュームを作成します。

AWS マネジメントコンソールで EC2 サービスを選択します。

![](../image/ec2_4.PNG)

EC2 ダッシュボードが表示されますので、左端のメニューから「ボリューム」を選択し、「ボリュームの作成」ボタンを押します。

![](../image/c9_8.PNG)

以下内容で設定してください。  
それ以外の項目はデフォルトのままで構いません。

 - ボリュームタイプ: gp2
 - サイズ (GiB): 1000
 - キー: 「タグの追加」を押して行を追加した後、キーに「Name」、値に名前 (任意の英数字) を入力します

入力出来たら、「ボリュームの作成」ボタンを押します。

![](../image/c9_9.PNG)

「閉じる」ボタンを押します。

![](../image/c9_10.PNG)

作成したボリュームは「available」になっています。

![](../image/c9_11.PNG)

次に作成したボリュームを cloud9 環境にアタッチします。

作成したボリュームを選択した後、「アクション」→「ボリュームのアタッチ」の順にクリックします。

![](../image/c9_12.PNG)

ボリュームのアタッチするインスタンスを選択します。  
cloud9 で作成したインスタンスには "aws-cloud9-{自分で設定したcloud9の名前}-{英数字}" という名前が付けられています。

![](../image/c9_13.PNG)

アタッチ先が "/dev/sdf" であることを確認して、「アタッチ」ボタンを押します。

![](../image/c9_14.PNG)

状態が「available」から「in-use」になれば成功です。

![](../image/c9_15.PNG)

### 4. work ディレクトリの準備

ここからは作成した cloud9 でコマンドを実行します。  
黄色で囲った部分がターミナルです。

![](../image/c9_16.PNG)

まず、アタッチしたディスクが存在するかを確認します。

```Bash
$ ls /dev/sdf
/dev/sdf
```

フォーマットします。

```Bash
$ sudo mkfs -t ext4 /dev/sdf
mke2fs 1.43.5 (04-Aug-2017)
Creating filesystem with 262144000 4k blocks and 65536000 inodes
Filesystem UUID: 6e3c88af-05e2-4350-935e-6dd91301a047
Superblock backups stored on blocks: 
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 
        4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968, 
        102400000, 214990848

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (262144 blocks): done
Writing superblocks and filesystem accounting information: done     
```

work ディレクトリにマウントします。

```Bash
$ sudo mkdir /work
$ sudo mount /dev/sdf /work
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
devtmpfs         16G   60K   16G   1% /dev
tmpfs            16G     0   16G   0% /dev/shm
/dev/nvme0n1p1  9.8G  5.7G  4.0G  60% /
/dev/nvme1n1    984G   77M  934G   1% /work
```

work ディレクトリのパーミッションを変更します。

```Bash
$ touch /work/file1
touch: cannot touch ‘/work/file1’: Permission denied
$ whoami
ec2-user
$ sudo chown ec2-user /work
$ touch /work/file1
$ ls -l /work
total 16
-rw-rw-r-- 1 ec2-user ec2-user     0 Jul 31 06:51 file1
drwx------ 2 root     root     16384 Jul 31 06:50 lost+found
```

### 3. 片付け

#### 3.1 終了する

ブラウザを閉じるだけでよいです。  
AWS Cloud9 の環境はデフォルト設定で、30分無操作で停止状態になります。

![](../image/c9_17.PNG)

### 3.2 cloud9 の環境を削除する

必要のない場合は削除します。

AWS マネジメントコンソールから cloud9 サービスを選択し、作成した環境を選択した後、「Delete」をクリックします。

![](../image/c9_18.PNG)

確認画面が表示されますので、削除したい環境を十分に確認したらテキストボックスに「Delete」と入力した後、「Delete」ボタンを押します。

![](../image/c9_19.PNG)

アタッチしたボリュームを削除します。  

AWS マネジメントコンソールから ec2 サービスを選択し、左端のメニューから「ボリューム」を選択し、ボリュームを表示します。  
今回作成したボリュームを選択した後、「アクション」→「Delete Volume」をクリックします。

![](../image/ec2_32.PNG)

確認画面が表示されますので、内容を確認したら、「はい、削除する」ボタンを押します。

![](../image/ec2_33.PNG)

---

## AWS EC2 を使用して Linux サーバを構築する

### 1. AWS コンソールにログイン

https://aws.amazon.com を web ブラウザで開き、「コンソールにサインイン」をクリックします。

![](../image/ec2_1.PNG)

次の画面でアカウント、ユーザ名、パスワードを入力します。

![](../image/ec2_2.PNG)

AWS マネジメントコンソールで東京リージョンを選択しておきます。

![](../image/ec2_3.PNG)

### 2. EC2 インスタンスの起動

AWS マネジメントコンソールで EC2 サービスを選択します。

![](../image/ec2_4.PNG)

EC2 ダッシュボードが表示されますので、「インスタンスの作成」ボタンを押します。

![](../image/ec2_5.PNG)

まず最初にマシンイメージを選択します。今回はAmazon Linux2 AMI (HVM) を使用します。  
マシンイメージ名の横にある「選択」ボタンを押します。

![](../image/ec2_6.PNG)

次にインスタンスタイプを選択します。今回はt3.2xlargeを使用します。  
インスタンスタイプ名の先頭にあるチェックボックスを選択したら、ページの最後にある「次の手順」ボタンを押します。

![](../image/ec2_7.PNG)

「インスタンスの詳細の設定」では何もせず、ページの最後にある「次の手順」ボタンを押します。

![](../image/ec2_8.PNG)

「ストレージの追加」では 1T のボリュームを追加します。  
まず、「新しいボリュームの追加」ボタンを押して行を追加し、サイズを「1000」と入力します。  
入力後、ページの最後にある「次の手順」ボタンを押します。

![](../image/ec2_9.PNG)

「タグの追加」では作成するインスタンスに名前をつけます。  
必須ではありませんが、名前がついていた方が管理しやすくなります。  
まず、「タグの追加」ボタンを押して行を追加し、キーに「Name」、値に名前 (任意の英数字) を入力します。  
入力後、ページの最後にある「次の手順」ボタンを押します。

![](../image/ec2_10.PNG)

最後は「セキュリティグループの設定」です。  
今回は新しくセキュリティグループを作成しますが、既存のグループがあればそちらを選択しても構いません。  
まず「セキュリティグループ名」「説明」を入力します。  
タイプ「SSH」を選択し、ソースにアクセスを許可しようとしている IP アドレスを入力します。「マイIP」を選択すると、現在の自分のIPアドレスを設定することができます。  
入力後、ページの最後にある「確認と作成」ボタンを押します。

![](../image/ec2_11.PNG)

確認画面が表示されますので、問題なければ「起動」ボタンを押してください。

![](../image/ec2_12.PNG)

キーペアの選択画面が表示されます。  
ここでは新しいキーペアを作成しますが、既存のキーペアがある場合はそちらを使用しても構いません。  
「キーペア名」を入力し、「キーペアのダウンロード」ボタンを押します。  

![](../image/ec2_13.PNG)

今回作成するキーペアはここでしかダウンロードできません。大切に保管してください。  

![](../image/ec2_14.PNG)

キーペアをダウンロードしたら、「インスタンスの作成」ボタンを押します。

![](../image/ec2_15.PNG)

作成ステータス画面が表示されます。「インスタンスの表示」ボタンを押します。

![](../image/ec2_16.PNG)

EC2 インスタンスリストが表示されます。  
今回作成したインスタンスはまだ作成中であることが分かります。

![](../image/ec2_17.PNG)

「チェックに合格しました」と表示されれば使用可能です。

![](../image/ec2_18.PNG)

### 3. 作成したインスタンスに SSH ログイン

先ほどのインスタンスリストで今回作成したインスタンスのパブリック DNS をコピーしておきます。

![](../image/ec2_19.PNG)

ターミナルを開きます。  

1) 先ほどダウンロードしたキーペアのパーミッションを変更します。  
ここでは `~/.ssh/` の下に保存していますが、適宜読み替えてください。  

2) 次に `ssh` コマンドで作成したインスタンスにログインします。  
Amazon Linux の場合、ユーザ名は `ec2-user` 固定です。  
サーバのアドレスは先ほどコピーしたパブリック DNS を張り付けてください。

3) 続けますかと聞かれたら `yes` と入力してください。

![](../image/ec2_20.PNG)

ログインできましたか？

### 4. work ディレクトリの準備

アタッチしたディスクが存在するかを確認します。

```Bash
$ ls /dev/sdb
/dev/sdb
```

フォーマットします。

```Bash
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
```

work ディレクトリにマウントします。

```Bash
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
```

work ディレクトリのパーミッションを変更します。

```Bash
$ touch /work/file1
touch: cannot touch ‘/work/file1’: Permission denied
$ sudo chown ec2-user /work
$ touch /work/file1
$ ls -l /work
total 16
-rw-rw-r-- 1 ec2-user ec2-user     0 Jul 31 02:35 file1
drwx------ 2 root     root     16384 Jul 31 02:28 lost+found
```

### 3. 片付け

#### 3.1 ターミナルから抜ける

`exit` でログアウトします。

```Bash
$ exit
logout
Connection to ec2-52-194-226-103.ap-northeast-1.compute.amazonaws.com closed.
```

#### 3.2 インスタンスを停止する

インスタンスを起動したままでは課金対象になってしまいますので、使用しない場合は停止しておきます。  
ただし、ディスクは停止した状態であっても課金対象となりますので、無課金状態にはなりません。  

※完全に削除したい場合はこの項目を飛ばして、次の 「3.3 インスタンスを削除する」に進んでください。

AWS マネジメントコンソールから作成したインスタンスを選択し、「アクション」→「インスタンスの状態」とたどって「停止」をクリックします。

![](../image/ec2_21.PNG)

確認画面が表示されますので、停止したいインスタンスを十分に確認したら「停止する」ボタンを押します。

![](../image/ec2_22.PNG)

停止処理が始まりました。

![](../image/ec2_23.PNG)

完全に停止すると「stopped」と表示されます。

![](../image/ec2_24.PNG)

#### 3.3 インスタンスを削除する

必要のないインスタンスは削除します。

AWS マネジメントコンソールから作成したインスタンスを選択し、「アクション」→「インスタンスの状態」とたどって「終了」をクリックします。

![](../image/ec2_25.PNG)

確認画面が表示されますので、削除したいインスタンスを十分に確認したら「はい、削除する」ボタンを押します。

![](../image/ec2_26.PNG)

削除されたインスタンスは「terminated」と表示されます。一定期間表示されますが、その後リストからも消えます。

![](../image/ec2_27.PNG)

アタッチしたボリュームを削除します。  
※インスタンス削除時、一緒に削除する設定にしていた場合はすでに削除されていますので、この操作は必要ありません。

左端のメニューから「ボリューム」を選択し、ボリュームを表示します。  
今回作成したボリュームを選択した後、「アクション」→「Delete Volume」をクリックします。

![](../image/ec2_32.PNG)

確認画面が表示されますので、内容を確認したら、「はい、削除する」ボタンを押します。

![](../image/ec2_33.PNG)

今回作成したセキュリティグループを削除します。

左端のメニューから「セキュリティグループ」を選択し、セキュリティグループを表示します。  
今回作成したセキュリティグループを選択した後、「アクション」→「セキュリティグループの削除」をクリックします。

![](../image/ec2_28.PNG)

確認画面が表示されますので、内容を確認したら、「はい、削除する」ボタンを押します。

![](../image/ec2_29.PNG)

今回作成したキーペアを削除します。

左端のメニューから「キーペア」を選択しキーペアを表示します。  
今回作成したキーペアを選択した後、「削除」ボタンを押します。

![](../image/ec2_30.PNG)

確認画面が表示されますので、内容を確認したら、「はい」ボタンを押します。

![](../image/ec2_31.PNG)

