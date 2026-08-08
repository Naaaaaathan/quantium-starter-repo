import csv
from typing import Any, Dict, List


def import_csv(file_path: str) -> List[Dict[str, Any]]:
    """Read a CSV file into a list of dictionaries."""
    with open(file_path, mode="r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def export_csv(rows: List[Dict[str, Any]], file_path: str) -> None:
    """Write a list of dictionaries to a CSV file."""
    with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        if not rows:
            csv_file.write("")
            return

        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def main():
    data0 = import_csv("data/daily_sales_data_0.csv")
    data1 = import_csv("data/daily_sales_data_1.csv")
    data2 = import_csv("data/daily_sales_data_2.csv")

    mergedData = data0 + data1 + data2
    cleanData = []
    for record in mergedData:
        # Filter to Pink Morsels
        if record["product"] != "pink morsel":
            continue

        newRecord = {}
        newRecord["date"] = record["date"]
        newRecord["region"] = record['region']

        # Merge quantity and price
        newRecord["sales"] = float(record["price"].lstrip("$"))*int(record["quantity"])

        # insert
        cleanData.append(newRecord)


    export_csv(cleanData, "data/output.csv")

if __name__ == "__main__":
    main()