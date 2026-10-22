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

# # Create DimProduct and FactSales dummy data in a Fabric Lakehouse
# 
# This notebook creates or replaces two Delta tables in the default Microsoft Fabric Lakehouse:
# 
# - `DimProduct`: 50 dummy products
# - `FactSales`: 500 dummy sales rows based on the provided TMDL
# 
# Attach the target Lakehouse to this notebook and set it as the **default Lakehouse** before running all cells.


# CELL ********************

from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, LongType, StringType,
    DateType, TimestampType, DecimalType
)
from decimal import Decimal
from datetime import date, datetime, timedelta
import random

random.seed(42)

DIM_PRODUCT_ROWS = 50
FACT_SALES_ROWS = 500

DIM_PRODUCT_TABLE = "DimProduct"
FACT_SALES_TABLE = "FactSales"

# For schema-enabled Lakehouses, use names such as:
# DIM_PRODUCT_TABLE = "dbo.DimProduct"
# FACT_SALES_TABLE = "dbo.FactSales"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 1. Create DimProduct

# CELL ********************

dim_product_schema = StructType([
    StructField("ProductKey", LongType(), False),
    StructField("ProductName", StringType(), False),
    StructField("ProductDescription", StringType(), True),
    StructField("BrandName", StringType(), False),
    StructField("CategoryName", StringType(), False),
    StructField("SubcategoryName", StringType(), False),
    StructField("ColorName", StringType(), True),
    StructField("Size", StringType(), True),
    StructField("UnitCost", DecimalType(18, 4), False),
    StructField("UnitPrice", DecimalType(18, 4), False),
    StructField("StartDate", DateType(), False),
    StructField("EndDate", DateType(), True),
    StructField("Status", StringType(), False),
    StructField("ETLLoadID", LongType(), False),
    StructField("LoadDate", TimestampType(), False),
    StructField("UpdateDate", TimestampType(), False)
])

product_templates = [
    ("Laptop", "Computers", "Laptops"),
    ("Desktop", "Computers", "Desktops"),
    ("Monitor", "Computers", "Monitors"),
    ("Keyboard", "Accessories", "Input Devices"),
    ("Mouse", "Accessories", "Input Devices"),
    ("Headset", "Accessories", "Audio"),
    ("Speaker", "Electronics", "Audio"),
    ("Smartphone", "Electronics", "Mobile Phones"),
    ("Tablet", "Electronics", "Tablets"),
    ("Printer", "Office Equipment", "Printers")
]

brands = ["Contoso", "Fabrikam", "Northwind", "Adventure Works", "Proseware"]
colors = ["Black", "White", "Silver", "Blue", "Red", "Gray"]
sizes = ["Small", "Medium", "Large", "Standard"]

product_rows = []
current_timestamp = datetime.now()

for product_key in range(1, DIM_PRODUCT_ROWS + 1):
    product_type, category, subcategory = product_templates[(product_key - 1) % len(product_templates)]
    brand = brands[(product_key - 1) % len(brands)]
    color = colors[(product_key - 1) % len(colors)]
    size = sizes[(product_key - 1) % len(sizes)]

    unit_cost = Decimal(str(round(random.uniform(10, 900), 4)))
    margin = Decimal(str(round(random.uniform(0.15, 0.45), 4)))
    unit_price = (unit_cost * (Decimal("1.0000") + margin)).quantize(Decimal("0.0001"))

    product_rows.append((
        product_key,
        f"{brand} {product_type} {product_key:03d}",
        f"Dummy {product_type.lower()} product generated for testing",
        brand,
        category,
        subcategory,
        color,
        size,
        unit_cost,
        unit_price,
        date(2024, 1, 1),
        None,
        "Active",
        1,
        current_timestamp,
        current_timestamp
    ))

dim_product_df = spark.createDataFrame(product_rows, schema=dim_product_schema)
display(dim_product_df.limit(10))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create or replace the DimProduct Delta table
(
    dim_product_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(DIM_PRODUCT_TABLE)
)

print(f"{DIM_PRODUCT_TABLE} created with {spark.table(DIM_PRODUCT_TABLE).count()} rows.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Create FactSales

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

product_price_lookup = {
    row["ProductKey"]: {
        "UnitCost": row["UnitCost"],
        "UnitPrice": row["UnitPrice"]
    }
    for row in dim_product_df.select("ProductKey", "UnitCost", "UnitPrice").collect()
}

fact_sales_rows = []
start_sales_date = datetime(2025, 1, 1)
number_of_sales_days = 365

for sales_key in range(1, FACT_SALES_ROWS + 1):
    product_key = random.randint(1, DIM_PRODUCT_ROWS)
    unit_cost = product_price_lookup[product_key]["UnitCost"]
    unit_price = product_price_lookup[product_key]["UnitPrice"]
    sales_quantity = random.randint(1, 10)

    return_quantity = (
        random.randint(1, min(2, sales_quantity))
        if random.random() < 0.10 else 0
    )

    if random.random() < 0.35:
        discount_quantity = random.randint(1, sales_quantity)
        discount_percentage = Decimal(str(random.choice([0.05, 0.10, 0.15, 0.20])))
    else:
        discount_quantity = 0
        discount_percentage = Decimal("0.00")

    gross_sales_amount = unit_price * Decimal(sales_quantity)
    discount_amount = (
        unit_price * Decimal(discount_quantity) * discount_percentage
    ).quantize(Decimal("0.0001"))
    return_amount = (
        unit_price * Decimal(return_quantity)
    ).quantize(Decimal("0.0001"))
    total_cost = (
        unit_cost * Decimal(sales_quantity)
    ).quantize(Decimal("0.0001"))
    sales_amount = (
        gross_sales_amount - discount_amount - return_amount
    ).quantize(Decimal("0.0001"))

    sales_date = start_sales_date + timedelta(
        days=random.randint(0, number_of_sales_days - 1),
        hours=random.randint(8, 20),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    load_timestamp = datetime.now()

    fact_sales_rows.append((
        sales_key,
        sales_date,
        random.randint(1, 4),
        random.randint(1, 20),
        product_key,
        random.randint(0, 10),
        1,
        unit_cost,
        unit_price,
        sales_quantity,
        return_quantity,
        return_amount,
        discount_quantity,
        discount_amount,
        total_cost,
        sales_amount,
        1,
        load_timestamp,
        load_timestamp
    ))

fact_sales_df = spark.createDataFrame(fact_sales_rows, schema=fact_sales_schema)
display(fact_sales_df.limit(10))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create or replace the FactSales Delta table
(
    fact_sales_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(FACT_SALES_TABLE)
)

print(f"{FACT_SALES_TABLE} created with {spark.table(FACT_SALES_TABLE).count()} rows.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Validate the generated tables

# CELL ********************

print("DimProduct row count:", spark.table(DIM_PRODUCT_TABLE).count())
print("FactSales row count:", spark.table(FACT_SALES_TABLE).count())

print("\nFactSales schema:")
spark.table(FACT_SALES_TABLE).printSchema()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate ProductKey referential integrity
invalid_product_keys_df = (
    spark.table(FACT_SALES_TABLE).alias("sales")
        .join(
            spark.table(DIM_PRODUCT_TABLE).alias("product"),
            F.col("sales.ProductKey") == F.col("product.ProductKey"),
            "left_anti"
        )
)

invalid_product_key_count = invalid_product_keys_df.count()
print(f"Rows with invalid ProductKey: {invalid_product_key_count}")
assert invalid_product_key_count == 0, "FactSales contains invalid ProductKey values."


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate calculated amounts
validation_df = (
    spark.table(FACT_SALES_TABLE)
        .withColumn(
            "ExpectedSalesAmount",
            F.round(
                (F.col("UnitPrice") * F.col("SalesQuantity"))
                - F.col("DiscountAmount")
                - F.col("ReturnAmount"),
                4
            )
        )
        .withColumn(
            "ExpectedTotalCost",
            F.round(F.col("UnitCost") * F.col("SalesQuantity"), 4)
        )
        .withColumn("SalesAmountValid", F.col("SalesAmount") == F.col("ExpectedSalesAmount"))
        .withColumn("TotalCostValid", F.col("TotalCost") == F.col("ExpectedTotalCost"))
)

display(validation_df.select(
    "SalesKey", "ProductKey", "SalesQuantity", "UnitPrice",
    "DiscountAmount", "ReturnAmount", "SalesAmount",
    "ExpectedSalesAmount", "SalesAmountValid",
    "TotalCost", "ExpectedTotalCost", "TotalCostValid"
).limit(20))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Preview joined sales and product data

# CELL ********************

sales_preview_df = (
    spark.table(FACT_SALES_TABLE).alias("sales")
        .join(
            spark.table(DIM_PRODUCT_TABLE).alias("product"),
            F.col("sales.ProductKey") == F.col("product.ProductKey"),
            "inner"
        )
        .select(
            F.col("sales.SalesKey"),
            F.col("sales.DateKey"),
            F.col("sales.channelKey"),
            F.col("sales.Store_Key"),
            F.col("sales.ProductKey"),
            F.col("product.ProductName"),
            F.col("product.CategoryName"),
            F.col("product.BrandName"),
            F.col("sales.SalesQuantity"),
            F.col("sales.UnitCost"),
            F.col("sales.UnitPrice"),
            F.col("sales.DiscountAmount"),
            F.col("sales.ReturnAmount"),
            F.col("sales.TotalCost"),
            F.col("sales.SalesAmount")
        )
        .orderBy("SalesKey")
)

display(sales_preview_df.limit(100))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Notes
# 
# - TMDL `int64` columns are represented as Spark `LongType`.
# - TMDL `decimal` columns are represented as `DecimalType(18,4)`.
# - Semantic-model properties such as `isHidden`, `summarizeBy`, format strings, lineage tags, and annotations are not physical Lakehouse table properties.
# - Rerunning this notebook replaces both Delta tables because it uses overwrite mode with schema overwrite enabled.

