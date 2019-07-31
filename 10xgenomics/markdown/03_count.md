2019.7.31　作成　NCC

## 3. cellranger count を実行してみる

この項では `cellranger count` を使用して Single-Library Analysis を行います。

公式ドキュメント：[Single-Library Analysis with Cell Ranger](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/count)

### 3-1. サンプルを使用して実行する

順番に実行していれば 2-5 までの結果がありますので、それを使用して `cellranger count` コマンドを実行します。  

```
cd /work
cellranger count --id=tiny-bcl3-count \
--transcriptome=./refdata-cellranger-GRCh38-3.0.0 \
--fastqs=./tiny-bcl3/outs/fastq_path \
--expect-cells=1000
```

--fastqs オプションに前回の出力結果のうち、fastq_path ディレクトリを渡します。  
--transcriptome オプションには 1-3 でダウンロードしたリファレンスファイルのディレクトリを指定します。  
--except-cells は期待されるセル数ですが、ここでは公式ドキュメントのとおり、1000とします。（デフォルトは3000です）  

その他オプションは公式ドキュメントを参照してください。
[Command Line Argument](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/count#args)

### 3-2. 現実的なデータで実行する

10xgenomicsが Single Cell Gene Expression Datasets を用意していますので、ダウンロードして試してみます。

https://support.10xgenomics.com/single-cell-gene-expression/datasets


上記のうち、「1k PBMCs from a Healthy Donor (v3 chemistry)」をダウンロードします。

```
wget http://cf.10xgenomics.com/samples/cell-exp/3.0.0/pbmc_1k_v3/pbmc_1k_v3_fastqs.tar
tar xvf pbmc_1k_v3_fastqs.tar
```

cellranger cout を実行します。  
--fastqs にダウンロードしたサンプルのfastqディレクトリを指定します。  
--except-cells にはサンプルのページに `run with --expect-cells=1000` と記載がありますので、1000を指定します。

```Bash
cellranger count --id=pbmc_1k_v3 \
--transcriptome=./refdata-cellranger-GRCh38-3.0.0 \
--fastqs=./pbmc_1k_v3_fastqs/ \
--expect-cells=1000
```

以下はログです。

```
$ cellranger count --id=pbmc_1k_v3 \
> --transcriptome=./refdata-cellranger-GRCh38-3.0.0 \
> --fastqs=./pbmc_1k_v3_fastqs/ \
> --expect-cells=1000 \
> --uiport=80
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

全体のログは [ここ](../data/cellranger_count_pbmc_1k_v3.log) です。

実行ログに記載されているサマリは [ここ](../data/pbmc_1k_v3/outs/web_summary.html) にアップロードしています。

```
Run summary HTML:                         /work/pbmc_1k_v3/outs/web_summary.html
```

---

[Option. Cell Ranger ユーザインタフェースの利用](./99_ui.html) に進んでください。
