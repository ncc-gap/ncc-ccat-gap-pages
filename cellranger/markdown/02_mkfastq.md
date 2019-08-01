2019.7.31　作成　NCC

## 2. cellranger mkfastq を実行してみる

この項では `cellranger mkfastq` を使用して FASTQ を生成します。

公式ドキュメント：[Generating FASTQs with cellranger mkfastq](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/mkfastq)

### 2-1. コマンドとオプション

cellranger mkfastq コマンドの基本形は以下のどちらかです

#### --csv オプションを使用する場合 (10xGenomics 推奨)

[csv サンプルはこちら](../data/cellranger-tiny-bcl-simple-1.2.0.csv)

```
cellranger mkfastq --id=tiny-bcl --run=./data/cellranger-tiny-bcl-1.2.0 --csv=./data/cellranger-tiny-bcl-simple-1.2.0.csv
```

#### --samplesheet オプションを使用する場合

samplesheet とは Illumina Experiment Manager互換のサンプルシートのことであり、ファイルのパスを指定します。

[samplesheet サンプルはこちら](../data/cellranger-tiny-bcl-samplesheet-1.2.0.csv)

```
cellranger mkfastq --id=tiny-bcl2 --run=./data/cellranger-tiny-bcl-1.2.0 --samplesheet=./data/cellranger-tiny-bcl-samplesheet-1.2.0.csv
```

どちらにしても --run オプションは必須であり、 Illumina BCL へのパスを指定します。

--id は出力ディレクトリです。必須ではありませんが明示したほうがよいでしょう。デフォルトは--runオプションで指定されるフローセルの名前です。

また、qcを実行するには --qc オプションも合わせて指定する必要があります。

その他のオプションについては 10xGENOMICS のドキュメント [Arguments and Options](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/mkfastq#arguments_options) を参照してください。

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

```Bash

/work
├── data
│         ├── cellranger-tiny-bcl-1.2.0
│         └── cellranger-tiny-bcl-simple-1.2.0.csv
│         └── cellranger-tiny-bcl-samplesheet-1.2.0.csv
└── refdata-cellranger-GRCh38-and-mm10-3.1.0
```

### 2-2. 簡単な csv サンプルシートを使用して mkfastq を実行する

`cellranger mkfastq` コマンドを実行します。

```Bash
cd /work
cellranger mkfastq --id=tiny-bcl --run=./data/cellranger-tiny-bcl-1.2.0 --csv=./data/cellranger-tiny-bcl-simple-1.2.0.csv
```

実行ログは以下のように出力されます。 `Pipestance completed successfully!` と表示されていれば成功です。

```Bash
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

### 2-3. 実行した csv サンプルシートを確認する

サンプルシートを見てみます。
Lane, Sample, Index の構成になっています。

```
$ cat /work/data/cellranger-tiny-bcl-simple-1.2.0.csv
Lane,Sample,Index
1,test_sample,SI-P03-C9
```

単純な構成なので、10xGenomics は CSV サンプルシートを使用することを推奨しています。

| 列名  | 説明 |
|:------|:-----|
|Lane   | 処理するフローセルのレーン。単一レーン、範囲（2〜4など）、または「*」のいずれかになります。 |
|Sample | サンプルの名前。この名前は、生成されたすべての FASTQ ファイルのprefixとなり、すべてのダウンストリーム10xパイプラインの `--sample` 引数に対応します。 サンプル名は、イルミナの bcl2fastq 命名要件に準拠している必要があります。文字、数字、アンダースコア(_)、ハイフン(-)のみが許可されています。ドット(.)を含む他の記号は使用できません。 |
|Index  | ライブラリ構築に使用した 10x のサンプルインデックスセット, e.g., SI-GA-A12. |

### 2-4. --samplesheet オプション を使用して mkfastq を実行する

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

QC出力結果と構成については 10xGENOMICS のドキュメント [Reading Quality Control Metrics](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/mkfastq#qc_metrics) を参照してください。

---

[3. cellranger count を実行してみる](./03_count.html) に進んでください。
