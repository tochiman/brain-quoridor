# brain-quoridor
## 概要
コリドールをWebで遊べるようにしたもの。AIあるいはオンライン対戦ができます。
オリジナル要素としてアイテム機能を追加予定。

## 規定
- `main`ブランチへの直接Pushの禁止
- `dev`ブランチへPRして、検証後に`main`ブランチへ
- 基本的に`feat/...`という名前でブランチを作成
- 不要になったブランチは削除すること

## 起動方法
### 本番環境版
1. このリポジトリを持ってくる
```bash
git clone https://github.com/tochiman/brain-quoridor.git
```
2. コンテナの起動(本番環境版)
```bash
docker compose up -d -f compose-prod.yaml
```
### 開発環境版
1. このリポジトリを持ってくる
```bash
git clone https://github.com/tochiman/brain-quoridor.git
```
2. コンテナの起動(本番環境版)
```bash
docker compose up -d
```
