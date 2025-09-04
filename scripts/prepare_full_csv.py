import pandas as pd

# Load Excel
df = pd.read_excel("/home/gourav_dhalwal/gita-chatbot/data/Bhagavad_Gita_Verses.xlsx")

# Naya dataframe
df_conv = pd.DataFrame()

# Agar tumhare file me Chapter info hai toh usko lo, warna manual numbering
if "Chapter" in df.columns:
    df_conv["chapter"] = df["Chapter"]
    df_conv["verse"] = df.groupby("Chapter").cumcount() + 1
else:
    # fallback if chapter column not present
    # assume continuous verses, you can manually adjust later
    df_conv["chapter"] = 1
    df_conv["verse"] = range(1, len(df) + 1)

# Map baaki columns
df_conv["sanskrit"] = df["OriginalVerse"]
df_conv["transliteration"] = df["Transliteration"]
df_conv["translation_en"] = df["Translation"]
df_conv["translation_hi"] = ""
df_conv["explanation_en"] = df["Commentary"]
df_conv["tags"] = ""

# Save CSV
df_conv.to_csv("data/gita_full_ready.csv", index=False)
print("✅ CSV ready at data/gita_full_ready.csv")
