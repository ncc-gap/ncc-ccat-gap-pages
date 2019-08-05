AWS 環境で Cell Ranger 環境を構築する
=====================================

Cell Ranger とは
----------------

| Cell Ranger は single-cell の RNA-seq
  に対する解析パイプラインであり、Chromium single-cell RNA-seq
  によるシーケンスデータをアラインメントし、feature-barcode
  行列を生成してクラスタリングと遺伝子発現分析を行います。
| Cell Ranger には、single-cell
  遺伝子発現実験に関連する4つのパイプラインが含まれています。

-  **cellranger mkfastq** は Illumina シーケンサによって生成された Raw
   Base Call (BCL) ファイルを FASTQ ファイルに逆多重化します。
-  **cellranger count** は cellranger mkfastq で作成した FASTQ
   ファイルを使用して、アライメント、フィルタリング、バーコードカウント、および
   UMI カウントを実行します。
-  **cellranger aggr**
   は複数回の実行結果を集約し、結合データを分析します。
-  **cellranger reanalyze** は cellranger count または cellranger aggr
   によって生成された機能バーコード行列を取得し、調整可能なパラメータ設定を使用して次元削減、クラスタリング、および遺伝子発現アルゴリズムを再実行します。

| これらのパイプラインは、Chromium-specific algorithms と RNA
  解析に広く使用されているアラインメントルール STAR
  とを組み合わせたものです。
| 出力は標準的な BAM, MEX, CSV, HDF5 と HTML
  であり、細胞情報が付与されています。

詳しくは以下を参考にしてください。

`What is Cell
Ranger? <https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/what-is-cell-ranger>`__

本文書では Cell Ranger 公式ドキュメントを参照しながら AWS
インスタンス上に Cell Raner 環境を構築し、サンプルデータを cellranger
count を使用して解析してみるまでを解説します。

.. toctree::
   :maxdepth: 2
   :numbered:
   
   setup.rst
   cellranger_mkfastq.rst
   cellranger_count.rst
   cellranger_ui.rst
   aws_cloud9.rst
   aws_ec2.rst

