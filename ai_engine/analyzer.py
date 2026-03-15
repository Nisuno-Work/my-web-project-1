import pandas as pd

df = pd.read_csv("../data_collector/trend_data.csv")

def generate_content_ideas(keyword):

    ideas = [
        f"5 เรื่องที่ต้องรู้เกี่ยวกับ {keyword}",
        f"รีวิว {keyword} ที่กำลังเป็นกระแส",
        f"{keyword} ดีจริงไหม?",
        f"มือใหม่ควรรู้อะไรเกี่ยวกับ {keyword}",
        f"เทรนด์ใหม่เกี่ยวกับ {keyword}"
    ]

    return ideas


content_data = []

for index, row in df.iterrows():

    trend = row["query"]
    ideas = generate_content_ideas(trend)

    for idea in ideas:
        content_data.append({
            "trend": trend,
            "content_idea": idea
        })

result = pd.DataFrame(content_data)

result.to_csv("../database/content_ideas.csv", index=False)

print("\nContent ideas saved to database/content_ideas.csv")