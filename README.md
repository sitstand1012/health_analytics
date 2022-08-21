# health_analytics
Health_Analyticsタスク関連のあれこれ

## data_structure.txt
  - データ構造についてまとめた.txtファイル

## fa_analytics.py
  - 因子分析のためのpythonファイル

### Requirement
- conda==4.12.0
- python==3.9.12
- factor-analyzer==0.4.0
- pandas==1.4.2
- scipy==1.7.3

(だとおもう)
(追加で必要そうなのあったら教えてください)

### かんたんなつかいかた
1. [ここ](https://www.kaggle.com/datasets/rajanand/key-indicators-of-annual-health-survey) からzipをおとす
2. 解凍する、すると「archive」というファイルができているはず
3. そのファイル内にある「Key_indicator_statewise.csv」へのパスをl.10のdirに代入する(また、l.43のshapedfilenameは適当に設定してください)
4. conda環境下で、fa_analytics.pyのあるディレクトリにて```python fa_analytics.py```する
