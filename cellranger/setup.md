# Cell Ranger 

## 準備

```Bash
virtualenv -p python3 ~/virtenv/py3-shpinx
source virtenv/py3-shpinx/bin/activate
pip install -U Sphinx
```


## プロジェクト作成

```bash
$ cd /home/Okada/github/ncc-ccat-gap-pages/
$ mkdir cellranger
$ cd cellranger
$ sphinx-quickstart
Welcome to the Sphinx 2.0.1 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: .

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
> Separate source and build directories (y/n) [n]: y

The project name will occur in several places in the built documentation.
> Project name: cellranger
> Author name(s): Ai Okada
> Project release []: 1.0.0

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
http://sphinx-doc.org/config.html#confval-language.
> Project language [en]: ja

Creating file ./source/conf.py.
Creating file ./source/index.rst.
Creating file ./Makefile.
Creating file ./make.bat.

Finished: An initial directory structure has been created.

You should now populate your master file ./source/index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.
```


## ビルド

```bash
make html
```

