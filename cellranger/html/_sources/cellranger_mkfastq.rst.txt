cellranger mkfastq の実行
----------------------------

この項では cellranger mkfastq を使用して FASTQ を生成します。

公式ドキュメント： `Generating FASTQs with cellranger mkfastq <https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/mkfastq>`__

コマンドとオプション
~~~~~~~~~~~~~~~~~~~~~~~~~

設定ファイルのサンプルが提供されていますので、ダウンロードしておきます。

.. code:: bash

   cd /work
   mkdir data
   cd data
   wget http://cf.10xgenomics.com/supp/cell-exp/cellranger-tiny-bcl-1.2.0.tar.gz
   wget http://cf.10xgenomics.com/supp/cell-exp/cellranger-tiny-bcl-simple-1.2.0.csv
   wget http://cf.10xgenomics.com/supp/cell-exp/cellranger-tiny-bcl-samplesheet-1.2.0.csv

ダウンロードしたファイルを解凍します。

.. code:: bash

   tar -xzvf cellranger-tiny-bcl-1.2.0.tar.gz

ここまでの作業により、データは以下のように配置されているはずです。

::

    /work/
    ├── cellranger-3.1.0/
    │
    ├── data/
    │   ├── cellranger-tiny-bcl-1.2.0/
    │   ├── cellranger-tiny-bcl-samplesheet-1.2.0.csv
    │   └── cellranger-tiny-bcl-simple-1.2.0.csv
    │
    └── refdata-cellranger-GRCh38-and-mm10-3.1.0/

cellranger mkfastq コマンドの基本形は以下のどちらかです

csv オプションを使用する場合 (10xGenomics 推奨)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`csv サンプルはこちら <../data/cellranger-tiny-bcl-simple-1.2.0.csv>`__

::

    # 実行コマンドの例
    
    cellranger mkfastq \
    --id=tiny-bcl \
    --run=./data/cellranger-tiny-bcl-1.2.0 \
    --csv=./data/cellranger-tiny-bcl-simple-1.2.0.csv

"--run" オプションは必須です。Illumina BCL へのパスを指定します。

samplesheet オプションを使用する場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

samplesheet とは Illumina Experiment Manager 互換のサンプルシートのことであり、ファイルのパスを指定します。

`samplesheetサンプルはこちら <../data/cellranger-tiny-bcl-samplesheet-1.2.0.csv>`__

::

    # 実行コマンドの例
    
    cellranger mkfastq \
    --id=tiny-bcl2 \
    --run=./data/cellranger-tiny-bcl-1.2.0 \
    --samplesheet=./data/cellranger-tiny-bcl-samplesheet-1.2.0.csv

"--run" オプションは必須です。Illumina BCL へのパスを指定します。

その他オプション
^^^^^^^^^^^^^^^^^^^^^^^

:--id: 出力ディレクトリ名です。必須ではありませんが明示したほうがよいでしょう。デフォルトは "--run" オプションで指定されるフローセルの名前です。
:--qc: QC を実行します。デフォルトでは実行されません。

その他のオプションについては 10xGenomics のドキュメント `Arguments and Options <https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/mkfastq#arguments_options>`__ を参照してください。

csv オプションで実行
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"--csv" オプションを使用して cellranger mkfastq コマンドを実行します。

.. code:: bash

   cd /work
   
   cellranger mkfastq \
   --id=tiny-bcl \
   --run=./data/cellranger-tiny-bcl-1.2.0 \
   --csv=./data/cellranger-tiny-bcl-simple-1.2.0.csv

| 実行ログは以下のように出力されます。
| "Pipestance completed successfully!" と表示されていれば成功です。

::

    # (途中省略)
    
    Outputs:
    - Run QC metrics:        null
    - FASTQ output folder:   /work/tiny-bcl/outs/fastq_path
    - Interop output folder: /work/tiny-bcl/outs/interop_path
    - Input samplesheet:     /work/tiny-bcl/outs/input_samplesheet.csv
    
    Waiting 6 seconds for UI to do final refresh.
    Pipestance completed successfully!
    
    2019-01-29 09:49:24 Shutting down.
    Saving pipestance info to tiny-bcl/tiny-bcl.mri.tgz

全体のログは `ここ <../data/cellranger_mkfastq_tiny-bcl.log>`__ です。

csv サンプルシートを確認
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| サンプルシートを見てみます。
| `csv サンプルはこちら <../data/cellranger-tiny-bcl-simple-1.2.0.csv>`__
| Lane, Sample, Index の構成になっています。

.. code:: bash

   cat /work/data/cellranger-tiny-bcl-simple-1.2.0.csv

|image0|


構成が簡単なため、10xGenomics は CSV サンプルシートを使用することを推奨しています。

+---------+---------------------------------------------------------------------------------------------------------------------+
| 列名    | 説明                                                                                                                |
+=========+=====================================================================================================================+
| Lane    | 処理するフローセルのレーン。単一レーン、範囲（2〜4など）、または「*」のいずれかになります。                         |
+---------+---------------------------------------------------------------------------------------------------------------------+
| Sample  | サンプルの名前。                                                                                                    |
|         | この名前は生成する FASTQ ファイルの prefix となり、すべての 10xGenomics パイプラインの `--sample` 引数に対応します。|
|         | サンプル名は、イルミナの bcl2fastq 命名要件に準拠している必要があります。                                           |
|         | 文字、数字、アンダースコア(_)、ハイフン(-)のみが許可されています。ドット(.)を含む他の記号は使用できません。         |
+---------+---------------------------------------------------------------------------------------------------------------------+
| Index   | ライブラリ構築に使用した 10xGenomics のサンプルインデックスセット。 e.g., SI-GA-A12.                                |
+---------+---------------------------------------------------------------------------------------------------------------------+


samplesheet オプションで実行
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"--samplesheet" オプションを使用して cellranger mkfastq コマンドを実行します。

.. code:: bash

   cd /work
   
   cellranger mkfastq \
   --id=tiny-bcl2 \
   --run=./data/cellranger-tiny-bcl-1.2.0 \
   --samplesheet=./data/cellranger-tiny-bcl-samplesheet-1.2.0.csv

Quality Control をつけて実行
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"--qc" オプションをつけて実行します。

.. code:: bash

   cellranger mkfastq \
   --id=tiny-bcl3 \
   --run=./data/cellranger-tiny-bcl-1.2.0 \
   --samplesheet=./data/cellranger-tiny-bcl-samplesheet-1.2.0.csv \
   --qc

QC 出力結果と構成については 10xGenomics のドキュメント `Reading Quality Control Metrics <https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/mkfastq#qc_metrics>`__ を参照してください。

.. |image0| image:: ../image/fq_1.PNG
