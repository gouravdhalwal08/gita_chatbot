import pandas as pd
import json
import argparse

def convert_csv_to_json(input_file, output_file):
    # CSV load karo
    df = pd.read_csv(input_file)

    # Dict me convert
    records = df.to_dict(orient="records")

    # JSON save
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON saved at {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_file", required=True, help="Input CSV file")
    parser.add_argument("--out", dest="output_file", required=True, help="Output JSON file")
    args = parser.parse_args()

    convert_csv_to_json(args.input_file, args.output_file)
