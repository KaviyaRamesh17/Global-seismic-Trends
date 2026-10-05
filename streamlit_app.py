import streamlit as st
import pandas as pd
import pymysql

st.title("Global Seismic Trends")
st.write("Earthquake Data Analysis Dashboard")

# MySQL Connection
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="12345",
    database="earthquake_db",
    port=3306
)

st.success("MySQL Database Connected Successfully!")
st.subheader("Earthquake Data")

cursor = connection.cursor()

cursor.execute("""
    SELECT time, place, mag, depth, latitude, longitude
    FROM earthquake_data
    LIMIT 10
""")

data = cursor.fetchall()

st.dataframe(data)
st.subheader("Earthquake Summary")

cursor.execute("""
    SELECT 
        COUNT(*) AS total_earthquakes,
        MAX(mag) AS max_magnitude,
        AVG(mag) AS avg_magnitude
    FROM earthquake_data
""")

summary = cursor.fetchone()

col1, col2, col3 = st.columns(3)

col1.metric("Total Earthquakes", summary[0])
col2.metric("Maximum Magnitude", round(summary[1], 2))
col3.metric("Average Magnitude", round(summary[2], 2))
st.subheader("Earthquake Magnitude Categories")

cursor.execute("""
    SELECT magnitude_category, COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE magnitude_category IS NOT NULL
    GROUP BY magnitude_category
    ORDER BY earthquake_count DESC
""")

category_data = cursor.fetchall()

category_df = pd.DataFrame(
    category_data,
    columns=["Magnitude Category", "Earthquake Count"]
)

st.bar_chart(category_df.set_index("Magnitude Category"))
st.subheader("Earthquake Depth Analysis")

cursor.execute("""
    SELECT
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE depth IS NOT NULL
    GROUP BY depth_category
    ORDER BY earthquake_count DESC
""")

depth_data = cursor.fetchall()

depth_df = pd.DataFrame(
    depth_data,
    columns=["Depth Category", "Earthquake Count"]
)

st.bar_chart(depth_df.set_index("Depth Category"))
st.subheader("Year-wise Earthquake Count")

cursor.execute("""
    SELECT year, COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE year IS NOT NULL
    GROUP BY year
    ORDER BY year
""")

year_data = cursor.fetchall()

year_df = pd.DataFrame(
    year_data,
    columns=["Year", "Earthquake Count"]
)

st.line_chart(year_df.set_index("Year"))
st.subheader("Month-wise Earthquake Count")

cursor.execute("""
    SELECT month, COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE month IS NOT NULL
    GROUP BY month
    ORDER BY month
""")

month_data = cursor.fetchall()

month_df = pd.DataFrame(
    month_data,
    columns=["Month", "Earthquake Count"]
)

st.line_chart(month_df.set_index("Month"))
st.subheader("Top 10 Strongest Earthquakes")

cursor.execute("""
    SELECT place, mag
    FROM earthquake_data
    WHERE mag IS NOT NULL
    ORDER BY mag DESC
    LIMIT 10
""")

strongest_data = cursor.fetchall()

strongest_df = pd.DataFrame(
    strongest_data,
    columns=["Place", "Magnitude"]
)

st.bar_chart(strongest_df.set_index("Place"))
st.subheader("Top 10 Deepest Earthquakes")

cursor.execute("""
    SELECT place, depth
    FROM earthquake_data
    WHERE depth IS NOT NULL
    ORDER BY depth DESC
    LIMIT 10
""")

deepest_data = cursor.fetchall()

deepest_df = pd.DataFrame(
    deepest_data,
    columns=["Place", "Depth (km)"]
)

st.bar_chart(deepest_df.set_index("Place"))
st.subheader("Shallow Earthquakes with Magnitude > 7")

cursor.execute("""
    SELECT place, mag, depth
    FROM earthquake_data
    WHERE depth < 50
      AND mag > 7
    ORDER BY mag DESC
""")

shallow_data = cursor.fetchall()

shallow_df = pd.DataFrame(
    shallow_data,
    columns=["Place", "Magnitude", "Depth (km)"]
)

st.dataframe(shallow_df)
st.subheader("Year-wise Average Magnitude")

cursor.execute("""
    SELECT year, ROUND(AVG(mag), 2) AS average_magnitude
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY year
    ORDER BY year
""")

avg_mag_data = cursor.fetchall()

avg_mag_df = pd.DataFrame(
    avg_mag_data,
    columns=["Year", "Average Magnitude"]
)

st.line_chart(avg_mag_df.set_index("Year"))
st.subheader("Month-wise Average Magnitude")

cursor.execute("""
    SELECT month, ROUND(AVG(mag), 2) AS average_magnitude
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY month
    ORDER BY month
""")

monthly_avg_data = cursor.fetchall()

monthly_avg_df = pd.DataFrame(
    monthly_avg_data,
    columns=["Month", "Average Magnitude"]
)

st.line_chart(monthly_avg_df.set_index("Month"))
st.subheader("Top 10 Earthquake Locations")

cursor.execute("""
    SELECT place, COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE place IS NOT NULL
    GROUP BY place
    ORDER BY earthquake_count DESC
    LIMIT 10
""")

location_data = cursor.fetchall()

location_df = pd.DataFrame(
    location_data,
    columns=["Place", "Earthquake Count"]
)

st.bar_chart(location_df.set_index("Place"))
st.subheader("Earthquake Locations Map")

cursor.execute("""
    SELECT latitude, longitude
    FROM earthquake_data
    WHERE latitude IS NOT NULL
      AND longitude IS NOT NULL
    LIMIT 5000
""")

map_data = cursor.fetchall()

map_df = pd.DataFrame(
    map_data,
    columns=["latitude", "longitude"]
)

st.map(map_df)
st.subheader("Average Depth by Magnitude Category")

cursor.execute("""
    SELECT magnitude_category,
           ROUND(AVG(depth), 2) AS average_depth
    FROM earthquake_data
    WHERE magnitude_category IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY magnitude_category
    ORDER BY average_depth DESC
""")

avg_depth_data = cursor.fetchall()

avg_depth_df = pd.DataFrame(
    avg_depth_data,
    columns=["Magnitude Category", "Average Depth"]
)

st.bar_chart(avg_depth_df.set_index("Magnitude Category"))
st.subheader("Magnitude vs Depth")

cursor.execute("""
    SELECT mag, depth
    FROM earthquake_data
    WHERE mag IS NOT NULL
      AND depth IS NOT NULL
    LIMIT 5000
""")

magnitude_depth_data = cursor.fetchall()

magnitude_depth_df = pd.DataFrame(
    magnitude_depth_data,
    columns=["Magnitude", "Depth"]
)

st.scatter_chart(
    magnitude_depth_df,
    x="Magnitude",
    y="Depth")
st.subheader("Year-wise Maximum Magnitude")

cursor.execute("""
    SELECT year, ROUND(MAX(mag), 2) AS maximum_magnitude
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY year
    ORDER BY year
""")

max_mag_data = cursor.fetchall()

max_mag_df = pd.DataFrame(
    max_mag_data,
    columns=["Year", "Maximum Magnitude"]
)

st.line_chart(max_mag_df.set_index("Year"))
st.subheader("Month-wise Maximum Magnitude")

cursor.execute("""
    SELECT month, ROUND(MAX(mag), 2) AS maximum_magnitude
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY month
    ORDER BY month
""")

month_max_data = cursor.fetchall()

month_max_df = pd.DataFrame(
    month_max_data,
    columns=["Month", "Maximum Magnitude"]
)

st.line_chart(month_max_df.set_index("Month"))
st.subheader("Depth Category-wise Average Magnitude")

cursor.execute("""
    SELECT
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        ROUND(AVG(mag), 2) AS average_magnitude
    FROM earthquake_data
    WHERE depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY depth_category
    ORDER BY average_magnitude DESC
""")

depth_avg_data = cursor.fetchall()

depth_avg_df = pd.DataFrame(
    depth_avg_data,
    columns=["Depth Category", "Average Magnitude"]
)

st.bar_chart(depth_avg_df.set_index("Depth Category"))
st.subheader("Year-wise Average Depth")

cursor.execute("""
    SELECT year, ROUND(AVG(depth), 2) AS average_depth
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY year
    ORDER BY year
""")

year_depth_data = cursor.fetchall()

year_depth_df = pd.DataFrame(
    year_depth_data,
    columns=["Year", "Average Depth"]
)

st.line_chart(year_depth_df.set_index("Year"))
st.subheader("Depth Category-wise Earthquake Count")

cursor.execute("""
    SELECT
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE depth IS NOT NULL
    GROUP BY depth_category
    ORDER BY earthquake_count DESC
""")

depth_count_data = cursor.fetchall()

depth_count_df = pd.DataFrame(
    depth_count_data,
    columns=["Depth Category", "Earthquake Count"]
)

st.bar_chart(depth_count_df.set_index("Depth Category"))
st.subheader("Magnitude Category-wise Earthquake Count")

cursor.execute("""
    SELECT magnitude_category, COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE magnitude_category IS NOT NULL
    GROUP BY magnitude_category
    ORDER BY earthquake_count DESC
""")

mag_count_data = cursor.fetchall()

mag_count_df = pd.DataFrame(
    mag_count_data,
    columns=["Magnitude Category", "Earthquake Count"]
)

st.bar_chart(mag_count_df.set_index("Magnitude Category"))
st.subheader("Magnitude Category-wise Average Depth")

cursor.execute("""
    SELECT magnitude_category,
           ROUND(AVG(depth), 2) AS average_depth
    FROM earthquake_data
    WHERE magnitude_category IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY magnitude_category
    ORDER BY average_depth DESC
""")

mag_depth_data = cursor.fetchall()

mag_depth_df = pd.DataFrame(
    mag_depth_data,
    columns=["Magnitude Category", "Average Depth"]
)

st.bar_chart(mag_depth_df.set_index("Magnitude Category"))
st.subheader("Year-wise Maximum Depth")

cursor.execute("""
    SELECT year, ROUND(MAX(depth), 2) AS maximum_depth
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY year
    ORDER BY year
""")

year_max_depth_data = cursor.fetchall()

year_max_depth_df = pd.DataFrame(
    year_max_depth_data,
    columns=["Year", "Maximum Depth"]
)

st.line_chart(year_max_depth_df.set_index("Year"))
st.subheader("Year-wise Minimum Depth")

cursor.execute("""
    SELECT year, ROUND(MIN(depth), 2) AS minimum_depth
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY year
    ORDER BY year
""")

year_min_depth_data = cursor.fetchall()

year_min_depth_df = pd.DataFrame(
    year_min_depth_data,
    columns=["Year", "Minimum Depth"]
)

st.line_chart(year_min_depth_df.set_index("Year"))
st.subheader("Month-wise Average Depth")

cursor.execute("""
    SELECT month, ROUND(AVG(depth), 2) AS average_depth
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY month
    ORDER BY month
""")

month_depth_data = cursor.fetchall()

month_depth_df = pd.DataFrame(
    month_depth_data,
    columns=["Month", "Average Depth"]
)

st.line_chart(month_depth_df.set_index("Month"))
st.subheader("Hour-wise Earthquake Count")

cursor.execute("""
    SELECT hour, COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE hour IS NOT NULL
    GROUP BY hour
    ORDER BY hour
""")

hour_data = cursor.fetchall()

hour_df = pd.DataFrame(
    hour_data,
    columns=["Hour", "Earthquake Count"]
)

st.line_chart(hour_df.set_index("Hour"))
st.subheader("Magnitude Category-wise Maximum Magnitude")

cursor.execute("""
    SELECT magnitude_category,
           ROUND(MAX(mag), 2) AS maximum_magnitude
    FROM earthquake_data
    WHERE magnitude_category IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY magnitude_category
    ORDER BY maximum_magnitude DESC
""")

mag_max_data = cursor.fetchall()

mag_max_df = pd.DataFrame(
    mag_max_data,
    columns=["Magnitude Category", "Maximum Magnitude"]
)

st.bar_chart(mag_max_df.set_index("Magnitude Category"))
st.subheader("Top 10 Locations by Maximum Magnitude")

cursor.execute("""
    SELECT place,
           ROUND(MAX(mag), 2) AS maximum_magnitude
    FROM earthquake_data
    WHERE place IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY place
    ORDER BY maximum_magnitude DESC
    LIMIT 10
""")

location_max_data = cursor.fetchall()

location_max_df = pd.DataFrame(
    location_max_data,
    columns=["Place", "Maximum Magnitude"]
)

st.bar_chart(location_max_df.set_index("Place"))
st.subheader("Top 10 Locations by Average Magnitude")

cursor.execute("""
    SELECT place,
           ROUND(AVG(mag), 2) AS average_magnitude
    FROM earthquake_data
    WHERE place IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY place
    ORDER BY average_magnitude DESC
    LIMIT 10
""")

location_avg_data = cursor.fetchall()

location_avg_df = pd.DataFrame(
    location_avg_data,
    columns=["Place", "Average Magnitude"]
)

st.bar_chart(location_avg_df.set_index("Place"))
st.subheader("Month-wise Maximum Depth")

cursor.execute("""
    SELECT month, ROUND(MAX(depth), 2) AS maximum_depth
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY month
    ORDER BY month
""")

month_max_depth_data = cursor.fetchall()

month_max_depth_df = pd.DataFrame(
    month_max_depth_data,
    columns=["Month", "Maximum Depth"]
)

st.line_chart(month_max_depth_df.set_index("Month"))
st.subheader("Magnitude Category-wise Minimum Magnitude")

cursor.execute("""
    SELECT magnitude_category,
           ROUND(MIN(mag), 2) AS minimum_magnitude
    FROM earthquake_data
    WHERE magnitude_category IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY magnitude_category
    ORDER BY minimum_magnitude
""")

mag_min_data = cursor.fetchall()

mag_min_df = pd.DataFrame(
    mag_min_data,
    columns=["Magnitude Category", "Minimum Magnitude"]
)

st.bar_chart(mag_min_df.set_index("Magnitude Category"))
st.subheader("Depth Category-wise Maximum Magnitude")

cursor.execute("""
    SELECT
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        ROUND(MAX(mag), 2) AS maximum_magnitude
    FROM earthquake_data
    WHERE depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY depth_category
    ORDER BY maximum_magnitude DESC
""")

depth_max_mag_data = cursor.fetchall()

depth_max_mag_df = pd.DataFrame(
    depth_max_mag_data,
    columns=["Depth Category", "Maximum Magnitude"]
)

st.bar_chart(depth_max_mag_df.set_index("Depth Category"))
st.subheader("Depth Category-wise Minimum Magnitude")

cursor.execute("""
    SELECT
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        ROUND(MIN(mag), 2) AS minimum_magnitude
    FROM earthquake_data
    WHERE depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY depth_category
    ORDER BY minimum_magnitude
""")

depth_min_mag_data = cursor.fetchall()

depth_min_mag_df = pd.DataFrame(
    depth_min_mag_data,
    columns=["Depth Category", "Minimum Magnitude"]
)

st.bar_chart(depth_min_mag_df.set_index("Depth Category"))
st.subheader("Depth Category-wise Minimum Magnitude")

cursor.execute("""
    SELECT
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        ROUND(MIN(mag), 2) AS minimum_magnitude
    FROM earthquake_data
    WHERE depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY depth_category
    ORDER BY minimum_magnitude
""")

depth_min_mag_data = cursor.fetchall()

depth_min_mag_df = pd.DataFrame(
    depth_min_mag_data,
    columns=["Depth Category", "Minimum Magnitude"]
)

st.bar_chart(depth_min_mag_df.set_index("Depth Category"))
st.subheader("Hour-wise Average Magnitude")

cursor.execute("""
    SELECT hour, ROUND(AVG(mag), 2) AS average_magnitude
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY hour
    ORDER BY hour
""")

hour_avg_data = cursor.fetchall()

hour_avg_df = pd.DataFrame(
    hour_avg_data,
    columns=["Hour", "Average Magnitude"]
)

st.line_chart(hour_avg_df.set_index("Hour"))
st.subheader("Hour-wise Maximum Magnitude")

cursor.execute("""
    SELECT hour, ROUND(MAX(mag), 2) AS maximum_magnitude
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY hour
    ORDER BY hour
""")

hour_max_data = cursor.fetchall()

hour_max_df = pd.DataFrame(
    hour_max_data,
    columns=["Hour", "Maximum Magnitude"]
)

st.line_chart(hour_max_df.set_index("Hour"))
st.subheader("Hour-wise Minimum Magnitude")

cursor.execute("""
    SELECT hour, ROUND(MIN(mag), 2) AS minimum_magnitude
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY hour
    ORDER BY hour
""")

hour_min_data = cursor.fetchall()

hour_min_df = pd.DataFrame(
    hour_min_data,
    columns=["Hour", "Minimum Magnitude"]
)

st.line_chart(hour_min_df.set_index("Hour"))
st.subheader("Month-wise Minimum Magnitude")

cursor.execute("""
    SELECT month, ROUND(MIN(mag), 2) AS minimum_magnitude
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY month
    ORDER BY month
""")

month_min_data = cursor.fetchall()

month_min_df = pd.DataFrame(
    month_min_data,
    columns=["Month", "Minimum Magnitude"]
)

st.line_chart(month_min_df.set_index("Month"))
st.subheader("Month-wise Minimum Depth")

cursor.execute("""
    SELECT month, ROUND(MIN(depth), 2) AS minimum_depth
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY month
    ORDER BY month
""")

month_min_depth_data = cursor.fetchall()

month_min_depth_df = pd.DataFrame(
    month_min_depth_data,
    columns=["Month", "Minimum Depth"]
)

st.line_chart(month_min_depth_df.set_index("Month"))
st.subheader("Magnitude Category-wise Maximum Depth")

cursor.execute("""
    SELECT magnitude_category,
           ROUND(MAX(depth), 2) AS maximum_depth
    FROM earthquake_data
    WHERE magnitude_category IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY magnitude_category
    ORDER BY maximum_depth DESC
""")

mag_max_depth_data = cursor.fetchall()

mag_max_depth_df = pd.DataFrame(
    mag_max_depth_data,
    columns=["Magnitude Category", "Maximum Depth"]
)

st.bar_chart(mag_max_depth_df.set_index("Magnitude Category"))
st.subheader("Magnitude Category-wise Minimum Depth")

cursor.execute("""
    SELECT magnitude_category,
           ROUND(MIN(depth), 2) AS minimum_depth
    FROM earthquake_data
    WHERE magnitude_category IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY magnitude_category
    ORDER BY minimum_depth
""")

mag_min_depth_data = cursor.fetchall()

mag_min_depth_df = pd.DataFrame(
    mag_min_depth_data,
    columns=["Magnitude Category", "Minimum Depth"]
)

st.bar_chart(mag_min_depth_df.set_index("Magnitude Category"))
st.subheader("Year-wise Minimum Magnitude")

cursor.execute("""
    SELECT year, ROUND(MIN(mag), 2) AS minimum_magnitude
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY year
    ORDER BY year
""")

year_min_mag_data = cursor.fetchall()

year_min_mag_df = pd.DataFrame(
    year_min_mag_data,
    columns=["Year", "Minimum Magnitude"]
)

st.line_chart(year_min_mag_df.set_index("Year"))
st.subheader("Year-wise Maximum Magnitude by Magnitude Category")

cursor.execute("""
    SELECT year,
           magnitude_category,
           ROUND(MAX(mag), 2) AS maximum_magnitude
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND magnitude_category IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY year, magnitude_category
    ORDER BY year, magnitude_category
""")

year_cat_max_data = cursor.fetchall()

year_cat_max_df = pd.DataFrame(
    year_cat_max_data,
    columns=["Year", "Magnitude Category", "Maximum Magnitude"]
)

chart_df = year_cat_max_df.pivot(
    index="Year",
    columns="Magnitude Category",
    values="Maximum Magnitude"
)

st.line_chart(chart_df)
st.subheader("Year-wise Minimum Magnitude by Magnitude Category")

cursor.execute("""
    SELECT year,
           magnitude_category,
           ROUND(MIN(mag), 2) AS minimum_magnitude
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND magnitude_category IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY year, magnitude_category
    ORDER BY year, magnitude_category
""")

year_cat_min_data = cursor.fetchall()

year_cat_min_df = pd.DataFrame(
    year_cat_min_data,
    columns=["Year", "Magnitude Category", "Minimum Magnitude"]
)

chart_df = year_cat_min_df.pivot(
    index="Year",
    columns="Magnitude Category",
    values="Minimum Magnitude"
)

st.line_chart(chart_df)
st.subheader("Month-wise Maximum Magnitude by Magnitude Category")

cursor.execute("""
    SELECT month,
           magnitude_category,
           ROUND(MAX(mag), 2) AS maximum_magnitude
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND magnitude_category IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY month, magnitude_category
    ORDER BY month, magnitude_category
""")

month_cat_max_data = cursor.fetchall()

month_cat_max_df = pd.DataFrame(
    month_cat_max_data,
    columns=["Month", "Magnitude Category", "Maximum Magnitude"]
)

chart_df = month_cat_max_df.pivot(
    index="Month",
    columns="Magnitude Category",
    values="Maximum Magnitude"
)

st.line_chart(chart_df)
st.subheader("Month-wise Minimum Magnitude by Magnitude Category")

cursor.execute("""
    SELECT month,
           magnitude_category,
           ROUND(MIN(mag), 2) AS minimum_magnitude
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND magnitude_category IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY month, magnitude_category
    ORDER BY month, magnitude_category
""")

month_cat_min_data = cursor.fetchall()

month_cat_min_df = pd.DataFrame(
    month_cat_min_data,
    columns=["Month", "Magnitude Category", "Minimum Magnitude"]
)

chart_df = month_cat_min_df.pivot(
    index="Month",
    columns="Magnitude Category",
    values="Minimum Magnitude"
)

st.line_chart(chart_df)
st.subheader("Year-wise Earthquake Count by Magnitude Category")

cursor.execute("""
    SELECT year,
           magnitude_category,
           COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND magnitude_category IS NOT NULL
    GROUP BY year, magnitude_category
    ORDER BY year, magnitude_category
""")

year_cat_count_data = cursor.fetchall()

year_cat_count_df = pd.DataFrame(
    year_cat_count_data,
    columns=["Year", "Magnitude Category", "Earthquake Count"]
)

chart_df = year_cat_count_df.pivot(
    index="Year",
    columns="Magnitude Category",
    values="Earthquake Count"
)

st.line_chart(chart_df)
st.subheader("Month-wise Earthquake Count by Magnitude Category")

cursor.execute("""
    SELECT month,
           magnitude_category,
           COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND magnitude_category IS NOT NULL
    GROUP BY month, magnitude_category
    ORDER BY month, magnitude_category
""")

month_cat_count_data = cursor.fetchall()

month_cat_count_df = pd.DataFrame(
    month_cat_count_data,
    columns=["Month", "Magnitude Category", "Earthquake Count"]
)

chart_df = month_cat_count_df.pivot(
    index="Month",
    columns="Magnitude Category",
    values="Earthquake Count"
)

st.line_chart(chart_df)
st.subheader("Hour-wise Earthquake Count by Magnitude Category")

cursor.execute("""
    SELECT hour,
           magnitude_category,
           COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND magnitude_category IS NOT NULL
    GROUP BY hour, magnitude_category
    ORDER BY hour, magnitude_category
""")

hour_cat_count_data = cursor.fetchall()

hour_cat_count_df = pd.DataFrame(
    hour_cat_count_data,
    columns=["Hour", "Magnitude Category", "Earthquake Count"]
)

chart_df = hour_cat_count_df.pivot(
    index="Hour",
    columns="Magnitude Category",
    values="Earthquake Count"
)

st.line_chart(chart_df)
st.subheader("Hour-wise Average Magnitude by Magnitude Category")

cursor.execute("""
    SELECT hour,
           magnitude_category,
           AVG(mag) AS avg_magnitude
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND magnitude_category IS NOT NULL
    GROUP BY hour, magnitude_category
    ORDER BY hour, magnitude_category
""")

hour_avg_mag_cat_data = cursor.fetchall()

hour_avg_mag_cat_df = pd.DataFrame(
    hour_avg_mag_cat_data,
    columns=["Hour", "Magnitude Category", "Average Magnitude"]
)

chart_df = hour_avg_mag_cat_df.pivot(
    index="Hour",
    columns="Magnitude Category",
    values="Average Magnitude")

st.line_chart(chart_df)
st.subheader("Hour-wise Maximum Magnitude by Magnitude Category")

cursor.execute("""
    SELECT hour,
           magnitude_category,
           MAX(mag) AS max_magnitude
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND magnitude_category IS NOT NULL
    GROUP BY hour, magnitude_category
    ORDER BY hour, magnitude_category""")

hour_max_mag_cat_data = cursor.fetchall()

hour_max_mag_cat_df = pd.DataFrame(
    hour_max_mag_cat_data,
    columns=["Hour", "Magnitude Category", "Maximum Magnitude"]
)

chart_df = hour_max_mag_cat_df.pivot(
    index="Hour",
    columns="Magnitude Category",
    values="Maximum Magnitude")
st.line_chart(chart_df)

st.subheader("Hour-wise Minimum Magnitude by Magnitude Category")

cursor.execute("""
    SELECT hour,
           magnitude_category,
           MIN(mag) AS min_magnitude
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND magnitude_category IS NOT NULL
    GROUP BY hour, magnitude_category
    ORDER BY hour, magnitude_category
""")

hour_min_mag_cat_data = cursor.fetchall()

hour_min_mag_cat_df = pd.DataFrame(
    hour_min_mag_cat_data,
    columns=["Hour", "Magnitude Category", "Minimum Magnitude"]
)

chart_df = hour_min_mag_cat_df.pivot(
    index="Hour",
    columns="Magnitude Category",
    values="Minimum Magnitude"
)

st.line_chart(chart_df)

st.subheader("Month-wise Average Magnitude by Magnitude Category")

cursor.execute("""
    SELECT month,
           magnitude_category,
           AVG(mag) AS avg_magnitude
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND magnitude_category IS NOT NULL
    GROUP BY month, magnitude_category
    ORDER BY month, magnitude_category
""")

month_avg_mag_cat_data = cursor.fetchall()

month_avg_mag_cat_df = pd.DataFrame(
    month_avg_mag_cat_data,
    columns=["Month", "Magnitude Category", "Average Magnitude"]
)

chart_df = month_avg_mag_cat_df.pivot(
    index="Month",
    columns="Magnitude Category",
    values="Average Magnitude"
)

st.line_chart(chart_df)
st.subheader("Month-wise Minimum Magnitude by Magnitude Category")

cursor.execute("""
    SELECT month,
           magnitude_category,
           MIN(mag) AS min_magnitude
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND magnitude_category IS NOT NULL
    GROUP BY month, magnitude_category
    ORDER BY month, magnitude_category
""")

month_min_mag_cat_data = cursor.fetchall()

month_min_mag_cat_df = pd.DataFrame(
    month_min_mag_cat_data,
    columns=["Month", "Magnitude Category", "Minimum Magnitude"]
)

chart_df = month_min_mag_cat_df.pivot(
    index="Month",
    columns="Magnitude Category",
    values="Minimum Magnitude"
)

st.line_chart(chart_df)
st.subheader("Year-wise Average Magnitude by Magnitude Category")

cursor.execute("""
    SELECT year,
           magnitude_category,
           AVG(mag) AS avg_magnitude
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND magnitude_category IS NOT NULL
    GROUP BY year, magnitude_category
    ORDER BY year, magnitude_category
""")

year_avg_mag_cat_data = cursor.fetchall()

year_avg_mag_cat_df = pd.DataFrame(
    year_avg_mag_cat_data,
    columns=["Year", "Magnitude Category", "Average Magnitude"]
)

chart_df = year_avg_mag_cat_df.pivot(
    index="Year",
    columns="Magnitude Category",
    values="Average Magnitude"
)

st.line_chart(chart_df)
st.subheader("Year-wise Average Depth by Magnitude Category")

cursor.execute("""
    SELECT year,
           magnitude_category,
           AVG(depth) AS avg_depth
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND magnitude_category IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY year, magnitude_category
    ORDER BY year, magnitude_category
""")

year_avg_depth_cat_data = cursor.fetchall()

year_avg_depth_cat_df = pd.DataFrame(
    year_avg_depth_cat_data,
    columns=["Year", "Magnitude Category", "Average Depth"]
)

chart_df = year_avg_depth_cat_df.pivot(
    index="Year",
    columns="Magnitude Category",
    values="Average Depth"
)

st.line_chart(chart_df)
st.subheader("Month-wise Average Depth by Magnitude Category")

cursor.execute("""
    SELECT month,
           magnitude_category,
           AVG(depth) AS avg_depth
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND magnitude_category IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY month, magnitude_category
    ORDER BY month, magnitude_category
""")

month_avg_depth_cat_data = cursor.fetchall()

month_avg_depth_cat_df = pd.DataFrame(
    month_avg_depth_cat_data,
    columns=["Month", "Magnitude Category", "Average Depth"]
)

chart_df = month_avg_depth_cat_df.pivot(
    index="Month",
    columns="Magnitude Category",
    values="Average Depth"
)

st.line_chart(chart_df)
st.subheader("Hour-wise Average Depth")

cursor.execute("""
    SELECT hour,
           AVG(depth) AS avg_depth
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY hour
    ORDER BY hour
""")

hour_avg_depth_data = cursor.fetchall()

hour_avg_depth_df = pd.DataFrame(
    hour_avg_depth_data,
    columns=["Hour", "Average Depth"]
)

chart_df = hour_avg_depth_df.set_index("Hour")

st.line_chart(chart_df)
st.subheader("Hour-wise Maximum Depth")

cursor.execute("""
    SELECT hour,
           MAX(depth) AS max_depth
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY hour
    ORDER BY hour
""")

hour_max_depth_data = cursor.fetchall()

hour_max_depth_df = pd.DataFrame(
    hour_max_depth_data,
    columns=["Hour", "Maximum Depth"]
)

chart_df = hour_max_depth_df.set_index("Hour")

st.line_chart(chart_df)
st.subheader("Hour-wise Minimum Depth")

cursor.execute("""
    SELECT hour,
           MIN(depth) AS min_depth
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY hour
    ORDER BY hour
""")

hour_min_depth_data = cursor.fetchall()

hour_min_depth_df = pd.DataFrame(
    hour_min_depth_data,
    columns=["Hour", "Minimum Depth"]
)

chart_df = hour_min_depth_df.set_index("Hour")

st.line_chart(chart_df)
st.subheader("Year-wise Maximum Depth by Magnitude Category")

cursor.execute("""
    SELECT year,
           magnitude_category,
           MAX(depth) AS max_depth
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND magnitude_category IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY year, magnitude_category
    ORDER BY year, magnitude_category
""")

year_max_depth_cat_data = cursor.fetchall()

year_max_depth_cat_df = pd.DataFrame(
    year_max_depth_cat_data,
    columns=["Year", "Magnitude Category", "Maximum Depth"]
)

chart_df = year_max_depth_cat_df.pivot(
    index="Year",
    columns="Magnitude Category",
    values="Maximum Depth"
)

st.line_chart(chart_df)
st.subheader("Year-wise Minimum Depth by Magnitude Category")

cursor.execute("""
    SELECT year,
           magnitude_category,
           MIN(depth) AS min_depth
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND magnitude_category IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY year, magnitude_category
    ORDER BY year, magnitude_category
""")

year_min_depth_cat_data = cursor.fetchall()

year_min_depth_cat_df = pd.DataFrame(
    year_min_depth_cat_data,
    columns=["Year", "Magnitude Category", "Minimum Depth"]
)

chart_df = year_min_depth_cat_df.pivot(
    index="Year",
    columns="Magnitude Category",
    values="Minimum Depth"
)

st.line_chart(chart_df)
st.subheader("Month-wise Maximum Depth by Magnitude Category")

cursor.execute("""
    SELECT month,
           magnitude_category,
           MAX(depth) AS max_depth
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND magnitude_category IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY month, magnitude_category
    ORDER BY month, magnitude_category
""")

month_max_depth_cat_data = cursor.fetchall()

month_max_depth_cat_df = pd.DataFrame(
    month_max_depth_cat_data,
    columns=["Month", "Magnitude Category", "Maximum Depth"]
)

chart_df = month_max_depth_cat_df.pivot(
    index="Month",
    columns="Magnitude Category",
    values="Maximum Depth"
)

st.line_chart(chart_df)
st.subheader("Month-wise Minimum Depth by Magnitude Category")

cursor.execute("""
    SELECT month,
           magnitude_category,
           MIN(depth) AS min_depth
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND magnitude_category IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY month, magnitude_category
    ORDER BY month, magnitude_category
""")

month_min_depth_cat_data = cursor.fetchall()

month_min_depth_cat_df = pd.DataFrame(
    month_min_depth_cat_data,
    columns=["Month", "Magnitude Category", "Minimum Depth"]
)

chart_df = month_min_depth_cat_df.pivot(
    index="Month",
    columns="Magnitude Category",
    values="Minimum Depth"
)

st.line_chart(chart_df)
st.subheader("Year-wise Earthquake Count by Depth Category")

cursor.execute("""
    SELECT year,
           CASE
               WHEN depth < 50 THEN 'Below 50 km'
               WHEN depth < 100 THEN '50 to below 100 km'
               WHEN depth < 200 THEN '100 to below 200 km'
               ELSE '200 km and above'
           END AS depth_category,
           COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY year, depth_category
    ORDER BY year, depth_category
""")

year_count_depth_cat_data = cursor.fetchall()

year_count_depth_cat_df = pd.DataFrame(
    year_count_depth_cat_data,
    columns=["Year", "Depth Category", "Earthquake Count"]
)

chart_df = year_count_depth_cat_df.pivot(
    index="Year",
    columns="Depth Category",
    values="Earthquake Count"
)

st.line_chart(chart_df)
st.subheader("Month-wise Earthquake Count by Depth Category")

cursor.execute("""
    SELECT month,
           CASE
               WHEN depth < 50 THEN 'Below 50 km'
               WHEN depth < 100 THEN '50 to below 100 km'
               WHEN depth < 200 THEN '100 to below 200 km'
               ELSE '200 km and above'
           END AS depth_category,
           COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY month, depth_category
    ORDER BY month, depth_category
""")

month_count_depth_cat_data = cursor.fetchall()

month_count_depth_cat_df = pd.DataFrame(
    month_count_depth_cat_data,
    columns=["Month", "Depth Category", "Earthquake Count"]
)

chart_df = month_count_depth_cat_df.pivot(
    index="Month",
    columns="Depth Category",
    values="Earthquake Count"
)

st.line_chart(chart_df)
st.subheader("Hour-wise Earthquake Count by Depth Category")

cursor.execute("""
    SELECT hour,
           CASE
               WHEN depth < 50 THEN 'Below 50 km'
               WHEN depth < 100 THEN '50 to below 100 km'
               WHEN depth < 200 THEN '100 to below 200 km'
               ELSE '200 km and above'
           END AS depth_category,
           COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY hour, depth_category
    ORDER BY hour, depth_category
""")

hour_count_depth_cat_data = cursor.fetchall()

hour_count_depth_cat_df = pd.DataFrame(
    hour_count_depth_cat_data,
    columns=["Hour", "Depth Category", "Earthquake Count"]
)

chart_df = hour_count_depth_cat_df.pivot(
    index="Hour",
    columns="Depth Category",
    values="Earthquake Count"
)

st.line_chart(chart_df)
st.subheader("Earthquake Count by Depth Category and Magnitude Category")

cursor.execute("""
    SELECT
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        magnitude_category,
        COUNT(*) AS earthquake_count
    FROM earthquake_data
    WHERE depth IS NOT NULL
      AND magnitude_category IS NOT NULL
    GROUP BY depth_category, magnitude_category
    ORDER BY depth_category, magnitude_category
""")

depth_mag_count_data = cursor.fetchall()

depth_mag_count_df = pd.DataFrame(
    depth_mag_count_data,
    columns=["Depth Category", "Magnitude Category", "Earthquake Count"]
)

chart_df = depth_mag_count_df.pivot(
    index="Depth Category",
    columns="Magnitude Category",
    values="Earthquake Count"
)

st.bar_chart(chart_df)
st.subheader("Year-wise Average Depth by Depth Category")

cursor.execute("""
    SELECT
        year,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        AVG(depth) AS average_depth
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY year, depth_category
    ORDER BY year, depth_category
""")

year_avg_depth_cat_data = cursor.fetchall()

year_avg_depth_cat_df = pd.DataFrame(
    year_avg_depth_cat_data,
    columns=["Year", "Depth Category", "Average Depth"]
)

chart_df = year_avg_depth_cat_df.pivot(
    index="Year",
    columns="Depth Category",
    values="Average Depth"
)

st.line_chart(chart_df)
st.subheader("Month-wise Average Depth by Depth Category")

cursor.execute("""
    SELECT
        month,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        AVG(depth) AS average_depth
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY month, depth_category
    ORDER BY month, depth_category
""")

month_avg_depth_cat_data = cursor.fetchall()

month_avg_depth_cat_df = pd.DataFrame(
    month_avg_depth_cat_data,
    columns=["Month", "Depth Category", "Average Depth"]
)

chart_df = month_avg_depth_cat_df.pivot(
    index="Month",
    columns="Depth Category",
    values="Average Depth"
)

st.line_chart(chart_df)
st.subheader("Hour-wise Average Depth by Depth Category")

cursor.execute("""
    SELECT
        hour,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        AVG(depth) AS average_depth
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND depth IS NOT NULL
    GROUP BY hour, depth_category
    ORDER BY hour, depth_category
""")

hour_avg_depth_cat_data = cursor.fetchall()

hour_avg_depth_cat_df = pd.DataFrame(
    hour_avg_depth_cat_data,
    columns=["Hour", "Depth Category", "Average Depth"]
)

chart_df = hour_avg_depth_cat_df.pivot(
    index="Hour",
    columns="Depth Category",
    values="Average Depth"
)

st.line_chart(chart_df)
st.subheader("Year-wise Average Magnitude by Depth Category")

cursor.execute("""
    SELECT
        year,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        AVG(mag) AS average_magnitude
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY year, depth_category
    ORDER BY year, depth_category
""")

year_avg_mag_depth_data = cursor.fetchall()

year_avg_mag_depth_df = pd.DataFrame(
    year_avg_mag_depth_data,
    columns=["Year", "Depth Category", "Average Magnitude"]
)

chart_df = year_avg_mag_depth_df.pivot(
    index="Year",
    columns="Depth Category",
    values="Average Magnitude"
)

st.line_chart(chart_df)
st.subheader("Month-wise Average Magnitude by Depth Category")

cursor.execute("""
    SELECT
        month,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        AVG(mag) AS average_magnitude
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY month, depth_category
    ORDER BY month, depth_category
""")

month_avg_mag_depth_data = cursor.fetchall()

month_avg_mag_depth_df = pd.DataFrame(
    month_avg_mag_depth_data,
    columns=["Month", "Depth Category", "Average Magnitude"]
)

chart_df = month_avg_mag_depth_df.pivot(
    index="Month",
    columns="Depth Category",
    values="Average Magnitude"
)

st.line_chart(chart_df)
st.subheader("Hour-wise Average Magnitude by Depth Category")

cursor.execute("""
    SELECT
        hour,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        AVG(mag) AS average_magnitude
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY hour, depth_category
    ORDER BY hour, depth_category
""")

hour_avg_mag_depth_data = cursor.fetchall()

hour_avg_mag_depth_df = pd.DataFrame(
    hour_avg_mag_depth_data,
    columns=["Hour", "Depth Category", "Average Magnitude"]
)

chart_df = hour_avg_mag_depth_df.pivot(
    index="Hour",
    columns="Depth Category",
    values="Average Magnitude"
)

st.line_chart(chart_df)
st.subheader("Year-wise Maximum Magnitude by Depth Category")

cursor.execute("""
    SELECT
        year,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        MAX(mag) AS maximum_magnitude
    FROM earthquake_data
    WHERE year IS NOT NULL
      AND depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY year, depth_category
    ORDER BY year, depth_category
""")

year_max_mag_depth_data = cursor.fetchall()

year_max_mag_depth_df = pd.DataFrame(
    year_max_mag_depth_data,
    columns=["Year", "Depth Category", "Maximum Magnitude"]
)

chart_df = year_max_mag_depth_df.pivot(
    index="Year",
    columns="Depth Category",
    values="Maximum Magnitude"
)

st.line_chart(chart_df)
st.subheader("Month-wise Maximum Magnitude by Depth Category")

cursor.execute("""
    SELECT
        month,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        MAX(mag) AS maximum_magnitude
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY month, depth_category
    ORDER BY month, depth_category
""")

month_max_mag_depth_data = cursor.fetchall()

month_max_mag_depth_df = pd.DataFrame(
    month_max_mag_depth_data,
    columns=["Month", "Depth Category", "Maximum Magnitude"]
)

chart_df = month_max_mag_depth_df.pivot(
    index="Month",
    columns="Depth Category",
    values="Maximum Magnitude"
)

st.line_chart(chart_df)
st.subheader("Hour-wise Maximum Magnitude by Depth Category")

cursor.execute("""
    SELECT
        hour,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        MAX(mag) AS maximum_magnitude
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY hour, depth_category
    ORDER BY hour, depth_category
""")

hour_max_mag_depth_data = cursor.fetchall()

hour_max_mag_depth_df = pd.DataFrame(
    hour_max_mag_depth_data,
    columns=["Hour", "Depth Category", "Maximum Magnitude"]
)

chart_df = hour_max_mag_depth_df.pivot(
    index="Hour",
    columns="Depth Category",
    values="Maximum Magnitude"
)

st.line_chart(chart_df)
st.subheader("Month-wise Minimum Magnitude by Depth Category")

cursor.execute("""
    SELECT
        month,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        MIN(mag) AS minimum_magnitude
    FROM earthquake_data
    WHERE month IS NOT NULL
      AND depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY month, depth_category
    ORDER BY month, depth_category
""")

month_min_mag_depth_data = cursor.fetchall()

month_min_mag_depth_df = pd.DataFrame(
    month_min_mag_depth_data,
    columns=["Month", "Depth Category", "Minimum Magnitude"]
)

chart_df = month_min_mag_depth_df.pivot(
    index="Month",
    columns="Depth Category",
    values="Minimum Magnitude"
)

st.line_chart(chart_df)
st.subheader("Hour-wise Minimum Magnitude by Depth Category")

cursor.execute("""
    SELECT
        hour,
        CASE
            WHEN depth < 50 THEN 'Below 50 km'
            WHEN depth < 100 THEN '50 to below 100 km'
            WHEN depth < 200 THEN '100 to below 200 km'
            ELSE '200 km and above'
        END AS depth_category,
        MIN(mag) AS minimum_magnitude
    FROM earthquake_data
    WHERE hour IS NOT NULL
      AND depth IS NOT NULL
      AND mag IS NOT NULL
    GROUP BY hour, depth_category
    ORDER BY hour, depth_category
""")

hour_min_mag_depth_data = cursor.fetchall()

hour_min_mag_depth_df = pd.DataFrame(
    hour_min_mag_depth_data,
    columns=["Hour", "Depth Category", "Minimum Magnitude"]
)

chart_df = hour_min_mag_depth_df.pivot(
    index="Hour",
    columns="Depth Category",
    values="Minimum Magnitude"
)

st.line_chart(chart_df)