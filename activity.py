import requests

def get_base_transactions(address):
    url = f"https://api.basescan.org/api?module=account&action=txlist&address={address}&sort=desc"
    response = requests.get(url)

    if response.status_code != 200:
        return "Error fetching data."

    data = response.json()

    if data.get("status") != "1":
        return "No transactions found or invalid address."

    txs = data.get("result", [])
    summary = {
        "total_txs": len(txs),
        "swaps": 0,
        "bridges": 0,
        "mints": 0,
        "lp_actions": 0
    }

    for tx in txs:
        input_data = tx.get("input", "").lower()

        if "swap" in input_data:
            summary["swaps"] += 1
        if "bridge" in input_data:
            summary["bridges"] += 1
        if "mint" in input_data:
            summary["mints"] += 1
        if "liquidity" in input_data or "addliquidity" in input_data:
            summary["lp_actions"] += 1

    return summary


if __name__ == "__main__":
    wallet = input("Enter Base wallet address: ")
    print(get_base_transactions(wallet))
