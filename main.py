import requests
import pandas as pd
from urllib.parse import quote


def search_pchome_products(keyword, limit=10):
    encoded_keyword = quote(keyword)
    url = f"https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={encoded_keyword}&page=1&sort=rnk/dc"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)

    try:
        data = response.json()
    except Exception as e:
        print("❌ 無法解析 JSON：", e)
        print("伺服器回應：", response.text)
        return

    if "prods" not in data:
        print("⚠️ 沒有找到商品，請換個關鍵字看看")
        return

    products = data["prods"][:limit]
    results = []

    for i, product in enumerate(products, 1):
        name = product["name"]
        price = product["price"]
        pid = product["Id"]
        link = f"https://24h.pchome.com.tw/prod/{pid}"

        results.append({
            "商品名稱": name,
            "價格": price,
            "連結": link
        })

    df = pd.DataFrame(results)
    print(df)
    df.to_csv(f"{keyword}_pchome.csv", index=False, encoding="utf-8-sig")
    print(f"\n✅ 已將結果儲存為「{keyword}_pchome.csv」")


# 主程式區塊
if __name__ == "__main__":
    keyword = input("請輸入商品關鍵字：")
    search_pchome_products(keyword)
