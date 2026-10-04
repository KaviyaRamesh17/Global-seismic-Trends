import pandas as pd

print("Data Cleaning Started")

# Load earthquake data
df = pd.read_csv("earthquake_5_year_api_data.csv")

print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())
# Convert time columns to datetime
df["time"] = pd.to_datetime(df["time"], unit="ms")
df["updated"] = pd.to_datetime(df["updated"], unit="ms")

# Fill missing numeric values
numeric_columns = [
    "mag", "nst", "dmin", "rms", "gap",
    "magError", "depthError", "magNst"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Fill missing values with 0
df[numeric_columns] = df[numeric_columns].fillna(0)

# Create year and month columns
df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month

print("\nData Cleaning Completed")

print("\nNew Columns:")
print(df.columns.tolist())

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())
# Create day and day of week
df["day"] = df["time"].dt.day
df["day_of_week"] = df["time"].dt.day_name()

# Create depth category
df["depth_category"] = pd.cut(
    df["depth_km"],
    bins=[-1, 50, 300, float("inf")],
    labels=["Shallow", "Intermediate", "Deep"]
)

# Create magnitude category
df["magnitude_category"] = pd.cut(
    df["mag"],
    bins=[-float("inf"), 2, 4, 6, float("inf")],
    labels=["Below 2", "2 to 4", "4 to 6", "Above 6"]
)

print("\nDerived Columns Created")

print("\nDepth Category Count:")
print(df["depth_category"].value_counts())

print("\nMagnitude Category Count:")
print(df["magnitude_category"].value_counts())
import re

# Extract location/region from place using Regex
def extract_region(place):
    if pd.isna(place):
        return "Unknown"

    match = re.search(r",\s*([^,]+)$", str(place))

    if match:
        return match.group(1).strip()

    return str(place).strip()


df["region"] = df["place"].apply(extract_region)

print("\nRegex Region Extraction Completed")

print("\nSample Place and Region:")
print(df[["place", "region"]].head(10))
# Save cleaned data
df.to_csv("earthquake_cleaned_data.csv", index=False)

print("\nCleaned CSV file created successfully!")
print("File Name: earthquake_cleaned_data.csv")