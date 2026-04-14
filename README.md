# leetcode_data_ETL

一系列的從 Leetcode request 爬蟲(Extract)、整理取出資料(Transform)、到載入(Load)資料視覺化的過程。最後成品採用 Neon DB(Postgress)連線 Grafana Cloud，分析 Leetcode 題目的部分數據。

Grafana 視覺化連結:[https://yungyicool.grafana.net/public-dashboards/88dd7af9b3a54efaba7401680acf3172]

![Grafana Dashboard](image/leetcode%20etl.png)

Extract:
包含爬蟲程式碼，以及拿到的原始資料

Transform:
透過 column extract.py 爬取各題目的基本資訊，整合到 csv 與 Excel

Load:
將 csv 資料上傳到 neon 上，然後連結 grafana
