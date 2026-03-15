from pytrends.request import TrendReq
import time
import pandas as pd

# -----------------------
# 1. เชื่อม Google Trends
# -----------------------

pytrends = TrendReq(hl='th-TH', tz=360)

keywords = ["skincare", "บ้าน", "อาหารเสริม", "แฟชั่น", "บันเทิง"]

all_trends = []

# -----------------------
# 2. ดึง trend ทุก keyword
# -----------------------

for kw in keywords:

    print(f"\nSearching trend for: {kw}")

    pytrends.build_payload([kw], timeframe='now 7-d', geo='TH')

    time.sleep(5)

    related = pytrends.related_queries()

    rising = related[kw]["rising"]

    if rising is not None:

        rising = rising.head(10)

        for i in range(len(rising)):

            all_trends.append({
                "query": rising.iloc[i]["query"],
                "value": rising.iloc[i]["value"],
                "source_keyword": kw
            })

# -----------------------
# 3. บันทึก CSV
# -----------------------

trend_df = pd.DataFrame(all_trends)

trend_df.to_csv("trend_data.csv", index=False)

print("\nSaved file: trend_data.csv")
print(trend_df.head())