# シミュレーション統合環境 UniSim for Docker

## UniSim について
シミュレータ SUMO と外部のアプリケーションを接続し、シミュレーション環境を作成するためのpythonで記述されたフレームワーク。
実際の外部アプリと接続されたシミュレーション統合環境は、このフレームワークを利用したpythonスクリプトを記述することで構築する。


## UniSim の Docker イメージ
Ubuntu をベースとし、python 実行環境、SUMO シミュレータ、UniSim フレームワークを含む。SUMOのシミュレーション用データや、UniSimを利用したスクリプトはホスト側に置かれており、それらのデータはコンテナがアクティブになるとコンテナ側の /simdata ディレクトリ以下にマウントされることを前提としている。

### Docker イメージの作成手法
Dockerfile のおいてあるディレクトリで以下のコマンドを実行することで UniSim 環境のDockerイメージが作成される。成功すると unisim という名前の Docker イメージが作成される。  
Dokcerfile および UniSim ディレクトリが作成に利用される。

```bash
docker build -t unisim .
```

## WebAPIモックサーバ(json-server)との連携サンプル (sample 1)
UniSim から外部アプリの WebAPI をたたいて情報を取得し、実行中のシミュレーションにその結果を反映させるサンプル。
WebAPI のモックサーバとして json-server を利用し、json-server 実行用のコンテナは既存の Docker イメージをそのまま利用する。

### サンプルの実行法
docker-compose.yml ファイルのあるディレクトリで以下のコマンドを実行することで、UniSim 環境と、WebAPIモックサーバの連携サンプルが実行される。ただし、利用する環境に応じて docker-compose.yml の記述を調整する必要がある。(ファイル内の sample 1 の項目を参照)

```bash
docker-compose up
```

上記のコマンドを実行すると、UniSim 環境のコンテナと、UniSim コンテナとは別に json-server が走るコンテナがアクティブとなる。
UniSim 環境で実行されるシミュレーション用の各種データ、スクリプトは simdata ディレクトリ内に置かれている。本サンプルでは、上記コマンドで UniSim コンテナがアクティブになると simdata/hakata/script ディレクトリ内の navi_test.py が実行される。
また、json-server 側のコンテナで利用される json データは simdata/hakata/json_data ディレクトリ内に置かれている。

### サンプルスクリプト
simdata/hakata/script 内のpythonスクリプトについて…

#### navi_test.py
統合シミュレーション環境の初期化、実行開始用スクリプト

#### navi_agent_unisim.py
シミュレータ上の移動体を制御するエージェントとそのメンタルモデル（思考ルーチン）。
メンタルモデルは、エージェントが手に入れた情報を受け入れるか否かなど判断する。
エージェントは外部アプリと情報のやりとりをし、メンタルモデルの判断結果をもとに移動体の制御を行う。

#### navi_interface_unisim.py
外部アプリと情報のやりとりをおこなうオブジェクト。エージェントがアプリとの情報のやりとりで使う端末を模したオブジェクト。

## 3DTrafficSimulatorとの連携サンプル (sample 2)
別レポジトリで提供している 3DTrafficSimulator との連携サンプル。
UniSim に搭載されているデータベース機能を活用して、シミュレーション状況をステップ毎にデータベースに記録し、Python用ウェブアプリケーションフレームワークであるFlaskを用いたサーバを設置することで、外部のサービスからシミュレーション結果の情報をREST APIで取得することができる。

### サンプルの実行法
sample 1 と同様に docker-compose.yml の記述を調整する必要がある。(ファイル内の sample 2 の項目を参照)
また、SUMOのGUI機能を用いる際には、Xサーバのインストールが必要となることがある。
