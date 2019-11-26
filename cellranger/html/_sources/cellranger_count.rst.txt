cellranger count の実行
--------------------------

この項では cellranger count を使用して Single-Library Analysis を行います。

公式ドキュメント： `Single-Library Analysis with Cell Ranger <https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/count>`__

簡単なサンプルで実行
~~~~~~~~~~~~~~~~~~~~~~~~~

順番に実行していれば `2-5 <./cellranger_mkfastq.html#quality-control>`__ までの結果がありますので、それを使用して cellranger count コマンドを実行します。

.. code:: bash

    cd /work
    cellranger count --id=tiny-bcl3-count \
    --transcriptome=./refdata-cellranger-GRCh38-and-mm10-3.1.0 \
    --fastqs=./tiny-bcl3/outs/fastq_path \
    --expect-cells=1000 \
    --chemistry=threeprime

:--fastqs: 前回の出力結果のうち、"fastq_path  ディレクトリを渡します。
:--transcriptome: `1-3 <./setup.html#id2>`__ でダウンロードしたリファレンスファイルのディレクトリを指定します。
:--except-cells: 期待されるセル数ですが、ここでは公式ドキュメントのとおり、1000とします。（デフォルトは3000です）

その他オプションは公式ドキュメントを参照してください。 `Command Line Argument <https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/count#args>`__

以下のように表示されれば成功です。

::

    Outputs:
    - Run summary HTML:                         /work/tiny/outs/web_summary.html
    - Run summary CSV:                          /work/tiny/outs/metrics_summary.csv
    - BAM:                                      /work/tiny/outs/possorted_genome_bam.bam
    - BAM index:                                /work/tiny/outs/possorted_genome_bam.bam.bai
    - Filtered feature-barcode matrices MEX:    /work/tiny/outs/filtered_feature_bc_matrix
    - Filtered feature-barcode matrices HDF5:   /work/tiny/outs/filtered_feature_bc_matrix.h5
    - Unfiltered feature-barcode matrices MEX:  /work/tiny/outs/raw_feature_bc_matrix
    - Unfiltered feature-barcode matrices HDF5: /work/tiny/outs/raw_feature_bc_matrix.h5
    - Secondary analysis output CSV:            /work/tiny/outs/analysis
    - Per-molecule read information:            /work/tiny/outs/molecule_info.h5
    - CRISPR-specific analysis:                 null
    - Loupe Cell Browser file:                  /work/tiny/outs/cloupe.cloupe
    - Feature Reference:                        null
    
    Waiting 6 seconds for UI to do final refresh.
    Pipestance completed successfully!
    
    2019-11-26 09:18:10 Shutting down.
    Saving pipestance info to "tiny/tiny.mri.tgz"


現実的なデータで実行
~~~~~~~~~~~~~~~~~~~~~~~~~

※ **実行には約3時間かかります。**

10xgenomics は Single Cell Gene Expression Datasets を用意していますので、ダウンロードして試してみます。

https://support.10xgenomics.com/single-cell-gene-expression/datasets

上記のうち、「1k PBMCs from a Healthy Donor (v3 chemistry)」をダウンロードします。

.. code:: bash

    wget http://cf.10xgenomics.com/samples/cell-exp/3.0.0/pbmc_1k_v3/pbmc_1k_v3_fastqs.tar
    tar xvf pbmc_1k_v3_fastqs.tar

cellranger cout を実行します。

:--fastqs: ダウンロードしたサンプルの fastq ディレクトリを指定します。
:--except-cells: サンプルのページに run with --expect-cells=1000 と記載がありますので、1000 を指定します。

.. code:: bash

    cellranger count --id=pbmc_1k_v3 \
    --transcriptome=./refdata-cellranger-GRCh38-and-mm10-3.1.0 \
    --fastqs=./pbmc_1k_v3_fastqs/ \
    --expect-cells=1000

| 以下はログの一部です。
| "Pipestance completed successfully!" と表示されていれば成功です。
| 全体のログは `ここ <../data/cellranger_count_pbmc_1k_v3.log>`__ にアップロードしています。

::

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

実行ログの最後 "Outputs:" にサマリの出力場所が記載されています。

::

    Run summary HTML:                         /work/pbmc_1k_v3/outs/web_summary.html

`ここ <../data/pbmc_1k_v3/outs/web_summary.html>`__ にアップロードしていますので、興味があれば参考にしてください。
