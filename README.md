# BM Analytic
- [BM Analytic](#bm-analytic)
  - [1 Purpose](#1-purpose)
    - [1.1 移転価格税制の目的](#11-移転価格税制の目的)
    - [1.2 移転価格税制に関するベンチマーク業務(マスターファイル,ローカルファイル作成)](#12-移転価格税制に関するベンチマーク業務マスターファイルローカルファイル作成)
    - [1.3 PLI](#13-pli)
  - [2 Approach](#2-approach)
  - [3 How to use it](#3-how-to-use-it)
    - [3.1 Software dependencies](#31-software-dependencies)
    - [3.2 Setup procedure](#32-setup-procedure)

----
## 1 Purpose
移転価格税制, ベンチマーク分析業務で利用するPlatform

### 1.1 移転価格税制の目的

国境をまたぐ取引で発生する所得に対しては、一方の国が関連会社間の価格調整によって他国に流れた税金を自国に取り戻す。

例)
$$
A :{国内 → 仕入 50 → [親会社:利益=70-50=『20』]} → 子会社との取引価格 70 → {海外 → 海外子会社:利益150-70=『80』→ 売上 150}
$$
vs
$$
B: {国内 → 仕入 50 → [親会社:利益=100-50=『50』]} → 子会社との取引価格 100 → {海外 → 海外子会社:利益150-100=『50』→ 売上 150}
$$
A.  実際の取引
B.  あるべき取引

差額の30について、日本で納税が洩れているとみなされ、日本で課税

### 1.2 移転価格税制に関するベンチマーク業務(マスターファイル,ローカルファイル作成)

類似企業を抽出し検証する。

1. 25万件の会社データからスクリーニング
2. 機能の類似性を加味するため、一つ一つ文章を読み適切か検討する
3. 適切な価格で取引されているか利益水準指標(PLI)を利用して検証を行う

### 1.3 PLI

- 売上高営業利益率
$$
Operating Profit Margin (OM)  = Operating Profit / Sales
$$
- フルコストマークアップ率
$$
Total Cost Markup(TCM) = Operating Profit/Sales-Operating Profit
$$
- Berry Ration
$$
Berry Ration = Gross Profit/Selling, General,Administrative Expenses
$$

---

## 2 Approach
- DataをDashを利用し動的に操作・検索できるPlatformを作成する
- 機能の類似性を調査するサポートを行うため、会社概要が書かれた文章をDoc2Vecを利用し近似度評価を行う
- 近似評価を行ったものを利用し、テキストで入力した機能・製品と各会社の近似度をグラフで表示する
- グラフには近似度とPLIをプロットし候補となりうる企業一覧を可視化する

---
## 3 How to use it
### 3.1 Software dependencies
Based on python 3.8 or later and poetry <https://python-poetry.org/>
- Front End : Dash <https://dash.plotly.com/>
- Back End : python and Doc2Vec <https://radimrehurek.com/gensim/models/doc2vec.html>
- python library dependencies : ```prproject.toml```に記載
### 3.2 Setup procedure 
pyenvを利用しpython, poetryのインストール例(mac)
```
pyenv install 3.8.7
pyenv global 3.8.7
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry config virtualenvs.in-project true
poetry install
```

run app command
```
$ ~/bm_analytic/bm_analytic poetry run python app.py
```

run creat doc2vec model comand
```
$ ~/bm_analytic/modeling poetry run python doc2vec_model.py
```