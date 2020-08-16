# covid19 comformed case estimation

COVID19に関する分析をまとめたものです．

## 目次
- 日本の感染者数推定
- 世界の感染者数推定

## 日本の感染者数推定
1. 感染者数のデータをダウンロード  
[新型コロナウイルス(COVID-19)感染症の対応について｜内閣官房新型コロナウイルス感染症対策推進室](https://corona.go.jp/dashboard/)

2. EnKFにより感染者数を推定
  - 観測値から局所的にパラメータ推定
  - 推定したパラメータを使って観測値なしで未来の感染者数推定
  
## 世界の感染数推定
### 予定
- whoのサイトから毎日のレポートをスクレイピング.
- サイトからとってきたpdfの表からデータを抽出してcsvとして保存.
- 上記のように作成したdatasetを使ってなんらかの予測を行う.
