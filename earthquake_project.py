import pandas as pd
import matplotlib.pyplot as plt
import pymysql


# ==========================================================
# EARTHQUAKE DATA ANALYSIS PROJECT
# ==========================================================

print("======================================")
print("   EARTHQUAKE DATA ANALYSIS PROJECT")
print("======================================")


# ==========================================================
# 1. READ EARTHQUAKE DATA
# ==========================================================

df = pd.read_csv("earthquake_5_year_data.csv")

print("\nProject Started Successfully")

print("\nTotal rows:", len(df))
print("Total columns:", len(df.columns))

print("\nFirst 5 rows:")
print(df.head())


# ==========================================================
# 2. COLUMN NAMES
# ==========================================================

print("\nColumn Names:")
print(df.columns.tolist())


# ==========================================================
# 3. DATA TYPES
# ==========================================================

print("\nData Types:")
print(df.dtypes)


# ==========================================================
# 4. NULL VALUES
# ==========================================================

print("\nNull Values:")
print(df.isnull().sum())


# ==========================================================
# 5. REMOVE DUPLICATES
# ==========================================================

duplicate_count = df.duplicated().sum()

print("\nDuplicate Rows:", duplicate_count)

df = df.drop_duplicates()

print("Rows after removing duplicates:", len(df))


# ==========================================================
# 6. BASIC STATISTICS
# ==========================================================

print("\n======================================")
print("BASIC STATISTICS")
print("======================================")

print(df.describe())


# ==========================================================
# 7. DATA CLEANING
# ==========================================================

# Convert time column
df["time"] = pd.to_datetime(
    df["time"],
    errors="coerce",
    utc=True
)

# Numerical columns
numeric_columns = [
    "latitude",
    "longitude",
    "depth",
    "mag",
    "nst",
    "gap",
    "dmin",
    "rms",
    "horizontalError",
    "depthError",
    "magError",
    "magNst"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# Fill numerical missing values with median
for column in numeric_columns:

    if column in df.columns:

        if df[column].isnull().any():

            median_value = df[column].median()

            df[column] = df[column].fillna(
                median_value
            )


# Fill categorical missing values with mode
categorical_columns = df.select_dtypes(
    include=["object"]
).columns

for column in categorical_columns:

    if df[column].isnull().any():

        mode_value = df[column].mode()

        if not mode_value.empty:

            df[column] = df[column].fillna(
                mode_value[0]
            )


# ==========================================================
# 8. MAGNITUDE ANALYSIS
# ==========================================================

print("\n======================================")
print("MAGNITUDE ANALYSIS")
print("======================================")

print(
    "Minimum Magnitude:",
    df["mag"].min()
)

print(
    "Maximum Magnitude:",
    df["mag"].max()
)

print(
    "Average Magnitude:",
    df["mag"].mean()
)


# Strongest earthquake
strongest = df.loc[
    df["mag"].idxmax()
]

print("\nStrongest Earthquake:")
print(strongest)


# ==========================================================
# 9. DEPTH ANALYSIS
# ==========================================================

print("\n======================================")
print("DEPTH ANALYSIS")
print("======================================")

print(
    "Minimum Depth:",
    df["depth"].min()
)

print(
    "Maximum Depth:",
    df["depth"].max()
)

print(
    "Average Depth:",
    df["depth"].mean()
)


# ==========================================================
# 10. MAGNITUDE CATEGORY
# ==========================================================

def magnitude_category(magnitude):

    if magnitude < 4:
        return "Below 4"

    elif magnitude < 5:
        return "4 to below 5"

    elif magnitude < 6:
        return "5 to below 6"

    else:
        return "6 and above"


df["magnitude_category"] = df[
    "mag"
].apply(magnitude_category)


print("\n======================================")
print("MAGNITUDE CATEGORY")
print("======================================")

print(
    df["magnitude_category"].value_counts()
)


# ==========================================================
# 11. TOP 10 STRONGEST EARTHQUAKES
# ==========================================================

print("\n======================================")
print("TOP 10 STRONGEST EARTHQUAKES")
print("======================================")

top_10 = df.nlargest(
    10,
    "mag"
)

print(
    top_10[
        [
            "time",
            "latitude",
            "longitude",
            "depth",
            "mag",
            "place"
        ]
    ]
)


# ==========================================================
# 12. YEAR / MONTH / HOUR
# ==========================================================

df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["hour"] = df["time"].dt.hour


print("\n======================================")
print("EARTHQUAKES BY YEAR")
print("======================================")

print(
    df["year"].value_counts().sort_index()
)


print("\n======================================")
print("EARTHQUAKES BY MONTH")
print("======================================")

print(
    df["month"].value_counts().sort_index()
)


print("\n======================================")
print("EARTHQUAKES BY HOUR")
print("======================================")

print(
    df["hour"].value_counts().sort_index()
)


# ==========================================================
# 13. TOP EARTHQUAKE LOCATIONS
# ==========================================================

print("\n======================================")
print("TOP EARTHQUAKE LOCATIONS")
print("======================================")

print(
    df["place"].value_counts().head(10)
)


# ==========================================================
# 14. EARTHQUAKE TYPES
# ==========================================================

print("\n======================================")
print("EARTHQUAKE TYPES")
print("======================================")

print(
    df["type"].value_counts()
)


# ==========================================================
# 15. GRAPH 1 - MAGNITUDE HISTOGRAM
# ==========================================================

print("\nCreating Magnitude Histogram...")

plt.figure(figsize=(8, 5))

plt.hist(
    df["mag"],
    bins=30
)

plt.title(
    "Earthquake Magnitude Distribution"
)

plt.xlabel("Magnitude")
plt.ylabel("Number of Earthquakes")

plt.show()


# ==========================================================
# 16. GRAPH 2 - YEARLY EARTHQUAKE GRAPH
# ==========================================================

print("\nCreating Yearly Earthquake Graph...")

year_counts = (
    df["year"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(8, 5))

plt.plot(
    year_counts.index,
    year_counts.values,
    marker="o"
)

plt.title(
    "Earthquakes by Year"
)

plt.xlabel("Year")
plt.ylabel("Number of Earthquakes")

plt.show()


# ==========================================================
# 17. GRAPH 3 - MAGNITUDE VS DEPTH
# ==========================================================

print("\nCreating Magnitude vs Depth Graph...")

plt.figure(figsize=(8, 5))

plt.scatter(
    df["depth"],
    df["mag"],
    s=2
)

plt.title(
    "Magnitude vs Depth"
)

plt.xlabel("Depth")
plt.ylabel("Magnitude")

plt.show()


# ==========================================================
# 18. FINAL DATA INFORMATION
# ==========================================================

print("\n======================================")
print("FINAL DATA INFORMATION")
print("======================================")

print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

print("\nFinal Column Names:")
print(df.columns.tolist())


# ==========================================================
# MYSQL CONNECTION
# ==========================================================

print("\n======================================")
print("MYSQL CONNECTION")
print("======================================")


MYSQL_USER = "root"
MYSQL_PASSWORD = "12345"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
DATABASE_NAME = "earthquake_db"


# ==========================================================
# 19. CONNECT TO MYSQL SERVER
# ==========================================================

try:

    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT
    )

    print("MySQL server connection successful!")


except Exception as e:

    print("\nMySQL connection failed!")
    print("Error:", e)

    exit()


# ==========================================================
# 20. CREATE DATABASE
# ==========================================================

try:

    cursor = connection.cursor()

    cursor.execute(
        f"""
        CREATE DATABASE IF NOT EXISTS
        `{DATABASE_NAME}`
        """
    )

    connection.commit()

    print(
        f"Database '{DATABASE_NAME}' ready!"
    )

    cursor.close()
    connection.close()


except Exception as e:

    print("\nDatabase creation failed!")
    print("Error:", e)

    exit()


# ==========================================================
# 21. CONNECT TO EARTHQUAKE DATABASE
# ==========================================================

try:

    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT,
        database=DATABASE_NAME
    )

    print(
        "Connected to earthquake database!"
    )


except Exception as e:

    print("\nDatabase connection failed!")
    print("Error:", e)

    exit()


# ==========================================================
# 22. PREPARE DATA FOR MYSQL
# ==========================================================

print("\n======================================")
print("PREPARING DATA FOR MYSQL")
print("======================================")


# Convert datetime columns to string
for column in df.columns:

    if pd.api.types.is_datetime64_any_dtype(
        df[column]
    ):

        df[column] = df[column].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )


# Replace NaN with None
df = df.where(
    pd.notnull(df),
    None
)


# ==========================================================
# 23. CREATE MYSQL TABLE
# ==========================================================

cursor = connection.cursor()


# Delete old table if exists
cursor.execute(
    "DROP TABLE IF EXISTS earthquake_data"
)


# Create column definitions
column_definitions = []

for column in df.columns:

    if pd.api.types.is_integer_dtype(
        df[column]
    ):

        sql_type = "BIGINT"

    elif pd.api.types.is_float_dtype(
        df[column]
    ):

        sql_type = "DOUBLE"

    elif column == "time":

        sql_type = "DATETIME"

    else:

        sql_type = "TEXT"

    column_definitions.append(
        f"`{column}` {sql_type}"
    )


create_table_query = f"""
CREATE TABLE earthquake_data (
    {", ".join(column_definitions)}
)
"""


cursor.execute(
    create_table_query
)

connection.commit()

print(
    "Table 'earthquake_data' created successfully!"
)


# ==========================================================
# 24. INSERT DATA INTO MYSQL
# ==========================================================

print("\n======================================")
print("UPLOADING DATA TO MYSQL")
print("======================================")

columns = list(df.columns)

column_names = ", ".join(
    f"`{column}`"
    for column in columns
)

placeholders = ", ".join(
    ["%s"] * len(columns)
)

insert_query = f"""
INSERT INTO earthquake_data
({column_names})
VALUES
({placeholders})
"""


# Convert DataFrame to tuples
data = list(
    df.itertuples(
        index=False,
        name=None
    )
)


# Insert in batches
batch_size = 5000

total_rows = len(data)

for start in range(
    0,
    total_rows,
    batch_size
):

    end = min(
        start + batch_size,
        total_rows
    )

    batch = data[start:end]

    cursor.executemany(
        insert_query,
        batch
    )

    connection.commit()

    print(
        f"Inserted {end} / {total_rows} rows"
    )


# ==========================================================
# 25. VERIFY MYSQL DATA
# ==========================================================

print("\n======================================")
print("MYSQL VERIFICATION")
print("======================================")


cursor.execute(
    "SELECT COUNT(*) FROM earthquake_data"
)

result = cursor.fetchone()

print(
    "Total rows in MySQL:",
    result[0]
)


# ==========================================================
# 26. SHOW FIRST 5 ROWS
# ==========================================================

cursor.execute(
    """
    SELECT *
    FROM earthquake_data
    LIMIT 5
    """
)

rows = cursor.fetchall()

print("\nFirst 5 rows from MySQL:")

for row in rows:

    print(row)


# ==========================================================
# 27. CLOSE CONNECTION
# ==========================================================

cursor.close()
connection.close()


# ==========================================================
# PROJECT COMPLETED
# ==========================================================

print("\n======================================")
print("PYTHON + MYSQL COMPLETED SUCCESSFULLY!")
print("======================================")

print("\nDatabase:")
print("earthquake_db")

print("\nTable:")
print("earthquake_data")

print("\nTotal Rows Uploaded:")
print(len(df))

print("\n======================================")
print("       END OF EARTHQUAKE PROJECT")
print("======================================")