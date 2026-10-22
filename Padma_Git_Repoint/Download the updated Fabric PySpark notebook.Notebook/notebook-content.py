# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "81c0ffa3-e128-45a9-b6f2-c63e4ccb9f98",
# META       "default_lakehouse_name": "lh_1",
# META       "default_lakehouse_workspace_id": "a3cd8064-25ec-4464-81e8-4c62e4c01cbd",
# META       "known_lakehouses": [
# META         {
# META           "id": "81c0ffa3-e128-45a9-b6f2-c63e4ccb9f98"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Fabric Lakehouse: DimProduct and FactSales dummy data
# 
# Creates or replaces Delta tables matching the supplied physical TMDL columns:
# 
# - **DimProduct**: 100 products with all supplied product columns, including `ClassID` and `ClassName`
# - **FactSales**: 500 sales rows with valid `ProductKey` references
# 
# Attach the target Lakehouse and set it as the notebook's **default Lakehouse**, then run all cells.
# 
# > Measures, hierarchies, hidden flags, format strings, lineage tags, and summarization settings are semantic-model metadata. This notebook creates the physical Lakehouse columns; apply those model properties in the semantic model.


# CELL ********************

from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, LongType, StringType, DoubleType,
    TimestampType, DecimalType
)
from decimal import Decimal
from datetime import datetime, timedelta
import random

random.seed(42)

DIM_PRODUCT_ROWS = 100
FACT_SALES_ROWS = 500
DIM_PRODUCT_TABLE = "DimProduct"
FACT_SALES_TABLE = "FactSales"

# For schema-enabled Lakehouses, use for example:
# DIM_PRODUCT_TABLE = "dbo.DimProduct"
# FACT_SALES_TABLE = "dbo.FactSales"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 1. Build the complete DimProduct table

# CELL ********************

dim_product_schema = StructType([
    StructField("ProductKey", LongType(), False),
    StructField("ProductLabel", StringType(), False),
    StructField("ProductName", StringType(), False),
    StructField("ProductDescription", StringType(), True),
    StructField("ProductSubcategoryKey", LongType(), False),
    StructField("Manufacturer", StringType(), False),
    StructField("BrandName", StringType(), False),
    StructField("ClassID", StringType(), False),
    StructField("ClassName", StringType(), False),
    StructField("StyleID", StringType(), False),
    StructField("StyleName", StringType(), False),
    StructField("ColorID", StringType(), False),
    StructField("ColorName", StringType(), False),
    StructField("Size", StringType(), False),
    StructField("SizeRange", StringType(), False),
    StructField("SizeUnitMeasureID", StringType(), False),
    StructField("Weight", DoubleType(), False),
    StructField("WeightUnitMeasureID", StringType(), False),
    StructField("UnitOfMeasureID", StringType(), False),
    StructField("UnitOfMeasureName", StringType(), False),
    StructField("StockTypeID", StringType(), False),
    StructField("StockTypeName", StringType(), False),
    StructField("UnitCost", DecimalType(18, 4), False),
    StructField("UnitPrice", DecimalType(18, 4), False),
    StructField("AvailableForSaleDate", TimestampType(), False),
    StructField("StopSaleDate", TimestampType(), True),
    StructField("Status", StringType(), False),
    StructField("ImageURL", StringType(), True),
    StructField("ProductURL", StringType(), True),
    StructField("ETLLoadID", LongType(), False),
    StructField("LoadDate", TimestampType(), False),
    StructField("UpdateDate", TimestampType(), False),
    StructField("ProductSubcategoryName", StringType(), False),
    StructField("ProductCategoryKey", LongType(), False),
    StructField("ProductCategoryName", StringType(), False)
])

# category key, category name, subcategory key, subcategory, class id, class name,
# base product, unit of measure, size range, stock type
product_templates = [
    (1, "Computers", 101, "Laptops", "CL01", "Computers", "Laptop", "EA", "Standard", "FG", "Finished Good"),
    (1, "Computers", 102, "Desktops", "CL01", "Computers", "Desktop", "EA", "Standard", "FG", "Finished Good"),
    (1, "Computers", 103, "Monitors", "CL01", "Computers", "Monitor", "EA", "Screen Size", "FG", "Finished Good"),
    (2, "Electronics", 201, "Mobile Phones", "CL02", "Electronics", "Smartphone", "EA", "Screen Size", "FG", "Finished Good"),
    (2, "Electronics", 202, "Tablets", "CL02", "Electronics", "Tablet", "EA", "Screen Size", "FG", "Finished Good"),
    (2, "Electronics", 203, "Audio", "CL02", "Electronics", "Speaker", "EA", "Standard", "FG", "Finished Good"),
    (3, "Accessories", 301, "Input Devices", "CL03", "Accessories", "Keyboard", "EA", "Standard", "FG", "Finished Good"),
    (3, "Accessories", 302, "Pointing Devices", "CL03", "Accessories", "Mouse", "EA", "Standard", "FG", "Finished Good"),
    (3, "Accessories", 303, "Audio Accessories", "CL03", "Accessories", "Headset", "EA", "Standard", "FG", "Finished Good"),
    (4, "Office Equipment", 401, "Printers", "CL04", "Office Equipment", "Printer", "EA", "Standard", "FG", "Finished Good")
]

manufacturers = ["Contoso Manufacturing", "Fabrikam Industries", "Northwind Devices", "Adventure Works", "Proseware Labs"]
brands = ["Contoso", "Fabrikam", "Northwind", "Adventure Works", "Proseware"]
styles = [("ST01", "Standard"), ("ST02", "Professional"), ("ST03", "Premium"), ("ST04", "Compact")]
colors = [("BK", "Black"), ("WH", "White"), ("SL", "Silver"), ("BL", "Blue"), ("RD", "Red"), ("GY", "Gray")]
sizes = ["Small", "Medium", "Large", "13 inch", "15 inch", "17 inch"]

product_rows=[]
now=datetime.now()

for product_key in range(1, DIM_PRODUCT_ROWS + 1):
    (category_key, category_name, subcategory_key, subcategory_name,
     class_id, class_name, product_type, uom_id, size_range,
     stock_type_id, stock_type_name) = product_templates[(product_key - 1) % len(product_templates)]

    manufacturer = manufacturers[(product_key - 1) % len(manufacturers)]
    brand = brands[(product_key - 1) % len(brands)]
    style_id, style_name = styles[(product_key - 1) % len(styles)]
    color_id, color_name = colors[(product_key - 1) % len(colors)]
    size = sizes[(product_key - 1) % len(sizes)]
    unit_cost = Decimal(str(round(random.uniform(10, 900), 4)))
    margin = Decimal(str(round(random.uniform(0.15, 0.45), 4)))
    unit_price = (unit_cost * (Decimal("1") + margin)).quantize(Decimal("0.0001"))
    available_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))
    discontinued = random.random() < 0.08
    stop_date = available_date + timedelta(days=random.randint(180, 720)) if discontinued else None
    status = "Discontinued" if discontinued else "Active"
    product_name = f"{brand} {product_type} {product_key:03d}"

    product_rows.append((
        product_key,
        f"PRD-{product_key:05d}",
        product_name,
        f"{style_name} {color_name.lower()} {product_type.lower()} manufactured by {manufacturer}",
        subcategory_key,
        manufacturer,
        brand,
        class_id,
        class_name,
        style_id,
        style_name,
        color_id,
        color_name,
        size,
        size_range,
        "IN" if "inch" in size.lower() else "EA",
        round(random.uniform(0.10, 8.00), 3),
        "KG",
        uom_id,
        "Each",
        stock_type_id,
        stock_type_name,
        unit_cost,
        unit_price,
        available_date,
        stop_date,
        status,
        f"https://example.com/images/product-{product_key}.jpg",
        f"https://example.com/products/{product_key}",
        1,
        now,
        now,
        subcategory_name,
        category_key,
        category_name
    ))

dim_product_df = spark.createDataFrame(product_rows, schema=dim_product_schema)
print(f"Generated DimProduct rows: {dim_product_df.count()}")
display(dim_product_df.limit(10))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create or replace DimProduct
(
    dim_product_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(DIM_PRODUCT_TABLE)
)

print(f"{DIM_PRODUCT_TABLE} created/replaced with {spark.table(DIM_PRODUCT_TABLE).count()} rows.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Build FactSales using valid DimProduct keys

# CELL ********************

fact_sales_schema = StructType([
    StructField("SalesKey", LongType(), False),
    StructField("DateKey", TimestampType(), False),
    StructField("channelKey", LongType(), False),
    StructField("Store_Key", LongType(), False),
    StructField("ProductKey", LongType(), False),
    StructField("PromotionKey", LongType(), False),
    StructField("CurrencyKey", LongType(), False),
    StructField("UnitCost", DecimalType(18, 4), False),
    StructField("UnitPrice", DecimalType(18, 4), False),
    StructField("SalesQuantity", LongType(), False),
    StructField("ReturnQuantity", LongType(), False),
    StructField("ReturnAmount", DecimalType(18, 4), False),
    StructField("DiscountQuantity", LongType(), False),
    StructField("DiscountAmount", DecimalType(18, 4), False),
    StructField("TotalCost", DecimalType(18, 4), False),
    StructField("SalesAmount", DecimalType(18, 4), False),
    StructField("ETLLoadID", LongType(), False),
    StructField("LoadDate", TimestampType(), False),
    StructField("UpdateDate", TimestampType(), False)
])

product_lookup = {
    r["ProductKey"]: (r["UnitCost"], r["UnitPrice"])
    for r in dim_product_df.select("ProductKey", "UnitCost", "UnitPrice").collect()
}

fact_rows=[]
sales_start=datetime(2025, 1, 1)
for sales_key in range(1, FACT_SALES_ROWS + 1):
    product_key=random.randint(1, DIM_PRODUCT_ROWS)
    unit_cost, unit_price=product_lookup[product_key]
    qty=random.randint(1, 10)
    return_qty=random.randint(1, min(2, qty)) if random.random() < 0.10 else 0

    if random.random() < 0.35:
        discount_qty=random.randint(1, qty)
        discount_pct=Decimal(str(random.choice([0.05, 0.10, 0.15, 0.20])))
    else:
        discount_qty=0
        discount_pct=Decimal("0")

    return_amount=(unit_price * Decimal(return_qty)).quantize(Decimal("0.0001"))
    discount_amount=(unit_price * Decimal(discount_qty) * discount_pct).quantize(Decimal("0.0001"))
    total_cost=(unit_cost * Decimal(qty)).quantize(Decimal("0.0001"))
    sales_amount=(unit_price * Decimal(qty) - discount_amount - return_amount).quantize(Decimal("0.0001"))
    sale_time=sales_start + timedelta(days=random.randint(0,364), hours=random.randint(8,20), minutes=random.randint(0,59))
    load_time=datetime.now()

    fact_rows.append((sales_key, sale_time, random.randint(1,4), random.randint(1,20),
                      product_key, random.randint(0,10), 1, unit_cost, unit_price, qty,
                      return_qty, return_amount, discount_qty, discount_amount, total_cost,
                      sales_amount, 1, load_time, load_time))

fact_sales_df=spark.createDataFrame(fact_rows, schema=fact_sales_schema)
display(fact_sales_df.limit(10))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create or replace FactSales
(
    fact_sales_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(FACT_SALES_TABLE)
)
print(f"{FACT_SALES_TABLE} created/replaced with {spark.table(FACT_SALES_TABLE).count()} rows.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Validate columns, relationships, and calculated amounts

# CELL ********************

expected_product_columns = [
    "ProductKey", "ProductLabel", "ProductName", "ProductDescription",
    "ProductSubcategoryKey", "Manufacturer", "BrandName", "ClassID", "ClassName",
    "StyleID", "StyleName", "ColorID", "ColorName", "Size", "SizeRange",
    "SizeUnitMeasureID", "Weight", "WeightUnitMeasureID", "UnitOfMeasureID",
    "UnitOfMeasureName", "StockTypeID", "StockTypeName", "UnitCost", "UnitPrice",
    "AvailableForSaleDate", "StopSaleDate", "Status", "ImageURL", "ProductURL",
    "ETLLoadID", "LoadDate", "UpdateDate", "ProductSubcategoryName",
    "ProductCategoryKey", "ProductCategoryName"
]

actual_columns = spark.table(DIM_PRODUCT_TABLE).columns
missing_columns = sorted(set(expected_product_columns) - set(actual_columns))
extra_columns = sorted(set(actual_columns) - set(expected_product_columns))

print("Missing DimProduct columns:", missing_columns)
print("Unexpected DimProduct columns:", extra_columns)
assert not missing_columns, f"Missing columns: {missing_columns}"

invalid_product_keys = (
    spark.table(FACT_SALES_TABLE).alias("f")
    .join(spark.table(DIM_PRODUCT_TABLE).alias("d"), F.col("f.ProductKey") == F.col("d.ProductKey"), "left_anti")
    .count()
)
print("FactSales rows with invalid ProductKey:", invalid_product_keys)
assert invalid_product_keys == 0

amount_errors = (
    spark.table(FACT_SALES_TABLE)
    .filter(
        F.col("SalesAmount") != F.round(
            F.col("UnitPrice") * F.col("SalesQuantity") - F.col("DiscountAmount") - F.col("ReturnAmount"), 4
        )
    ).count()
)
print("Rows with invalid SalesAmount:", amount_errors)
assert amount_errors == 0


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Preview the product hierarchy and joined sales

# CELL ********************

# Physical columns supporting the semantic hierarchy:
# ClassName > BrandName > ProductCategoryName > ProductSubcategoryName > ProductName
product_hierarchy_preview = (
    spark.table(DIM_PRODUCT_TABLE)
    .select("ClassName", "BrandName", "ProductCategoryName", "ProductSubcategoryName", "ProductName")
    .orderBy("ClassName", "BrandName", "ProductCategoryName", "ProductSubcategoryName", "ProductName")
)
display(product_hierarchy_preview.limit(100))

joined_preview = (
    spark.table(FACT_SALES_TABLE).alias("f")
    .join(spark.table(DIM_PRODUCT_TABLE).alias("d"), "ProductKey", "inner")
    .select(
        "SalesKey", "DateKey", "ProductKey", "ProductName", "ClassName", "BrandName",
        "ProductCategoryName", "ProductSubcategoryName", "SalesQuantity", "UnitPrice",
        "DiscountAmount", "ReturnAmount", "SalesAmount"
    )
    .orderBy("SalesKey")
)
display(joined_preview.limit(100))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Semantic-model items to add separately
# 
# The Lakehouse now contains every physical `DimProduct` column from the supplied TMDL. In the semantic model, recreate:
# 
# - Measures: `Unit Cost` and `Unit Price`
# - Hierarchy: `ClassName` → `BrandName` → `ProductCategoryName` → `ProductSubcategoryName` → `ProductName`
# - Hidden-column settings, formatting, summarization, lineage tags, and date hierarchies

