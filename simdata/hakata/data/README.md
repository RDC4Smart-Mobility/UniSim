# シミュレーション用データ

## シミュレーションコンフィグデータ : hakata-tenjin.sumocfg, hakata-tenjin_navi_test.sumofg

シミュレーション実行用コンフィグファイル

| file                            | 用途                                            |
|:--------------------------------|:------------------------------------------------|
| hakata-tenjin.sumocfg           | 博多 - 天神エリアの基本シミュレーションの実施用 |
| hakata-tenjin_navi_test.sumocfg | 基本シミュレーションデータ + ナビ搭載車(赤い車両)の行動チェック用 |

また、hakata-tenjin_navi_test.sumocfg は、`../script/navi_test.py` スクリプトから呼び出されるシミュレーションコンフィグファイルでもある。

### input タグ

シミュレーションの入力データを記述

| タグ             | 概要                 | 属性値の書き方例                            |
|:-----------------|:---------------------|:--------------------------------------------|
| net-file         | ネットワークファイル | value="hakata-tenjin.net.xml"               |
| route-files      | 車両のルートファイル | value="route.rou.xml, vehicle_with_rou.xml" |
| additional-files | 追加データ：建物ポリゴンデータ、バス停・駅データ、電車ダイヤデータなど | value="station.add.xml, hakata-tenjin.poly.xml" |

### time タグ

シミュレーション世界での開始時間を指定

| タグ  | 概要     | 属性値の書き方例                                                         |
|:------|:---------|:-------------------------------------------------------------------------|
| begin | 開始時刻 | value="0" (0sec から開始)、 value="25200" (25200sec つまり 7:00:00 開始) |
| end   | 終了時刻 | value="30600" (30600sec つまり 8:30:00 終了)                             |

## ネットワークデータ : hakata-tenjin.net.xml

シミュレータの入力となるネットワークデータ。  
OpenStreetMap形式のファイルを `netconvert` にコンフィグファイル　`hakata-tenjin.netc.cfg` を入力することで生成したネットワークデータ。

```bash
netconvert -c hakata-tenjin.netc.cfg
```

### hakata-tenjin.netc.cfg

OSM地図データからネットワークデータを生成するためのコンフィグファイル

### hakata-tenjin.osm

博多 - 天神エリアを切り出してきたOpenStreetMap(OSM)形式の地図データ。  
JOSMなどのツールでネット上のOSMデータを切り出してきたもの。

### 信号現示タイミングデータ


## 移動体のルート情報データ : routes.rou.xml

シミュレータの入力となる移動体ルート情報データ。  
博多 - 天神エリアのシミュレーションの場合は、交差点からの流入量を記述した flow データと、交差点の直進率・右左折率データから `jtrrouter` を利用して生成する。

```bash
jtrrouter -c turns.jtrrcfg
```

### turns.jtrrcfg

jtrrouter を使ってルート情報を生成するためのコンフィグファイル

#### input タグ

| タグ              | 概要                                   | 属性値の書き方例                       |
|:------------------|:---------------------------------------|:---------------------------------------|
| net-file          | 道路ネットワークファイル               | value="hakata-tenjin.net.xml"          |
| route-files       | フローデータファイル (複数可能)        | value="flow_data/Nanotsu-Area.flows.xml, flow_data/Akasaka.flows.xml" |
| turn-ratio-files | 交差点の直進率・右左折率データファイル | value="junction-turn-ratio.turns.xml" |

#### output タグ

| タグ        | 概要                         | 属性の書き方例         |
|:------------|:-----------------------------|:-----------------------|
| output-file | 出力するルート情報ファイル名 | value="routes.rou.xml" |

#### processing タグ

| タグ                    | 概要                   | 属性の書き方例       |
|:------------------------|:-----------------------|:---------------------|
| remove-loops            | ルート内のループを削除 | value="true"         |
| accept-all-destinations | すべてのエッジをシンクエッジ(車両が消えて良いエッジ)にすることを許可するかどうか | value="true" |
| sink-edges              | シンクエッジのリスト   | value="-493376596#2" |

### 交差点流入交通量データ : flow_data/xxx.flows.xml

- data ディレクトリ以下に xxx.flows.xml の

### 交差点 直進率・右左折率データ : junction-turn-ratio.turns.xml
交差点交通流の 直進率・右左折率データ を1時間毎に纏めたもの  
**このファイルに不備がある場合**、上記の `jtrroute` の実行でエラーが出る。この場合は、エラーメッセージにあるエッジIDを頼りに、**`fromEdge` と `toEdge` がネットワークデータ上では直接接続されていない記述が含まれている**事を確認し修正する

## 鉄道ダイヤデータ : subway-kuko-xxx-line.add.xml

## バス停・駅データ : station.add.xml
NETEDIT で BusStop をバス停、駅のホームのある場所に設置し、additional file として出力したもの


## 建物ポリゴンデータ : hakata-tenjin.poly.xml

## ナビ搭載車のルート情報データ : vehicle_with_navi.rou.xml

ナビ搭載車のデフォルトのルートのみが書かれたファイル  
`duarouter` に、フローファイル `vehicle_with_navi.flows.xml` を入力として与え、以下のコマンドで生成

```bash
duarouter -n hakata-tenjin.net.xml -t vehicle_with_navi.flows.xml -o vehicle_with_navi.rou.xml
```
