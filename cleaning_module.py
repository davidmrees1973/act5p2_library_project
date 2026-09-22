# Exercise 3 - Cleaning data using Python
# David Rees 22/08/2026  (with a little help from ChatGPT)


# Using the example library system data, clean the bad data to make it easier to present
# Examples of bad data include:
# •	Empty cells.
# •	Data in the wrong format.
# •	Wrong data.
# •	Duplicates.

# Look through the data and use the Python knowledge you learnt in Module 3, as well 
# as the best practices and documentation you have learnt about in this module, to clean the data. 
# •	Use your knowledge to clear out the empty cells from the example data. 
# •	Fix any data that is in the wrong format. 
# •	Fix any incorrectly inputted data. Use functions to find out the anomalies in the data. 
# •	Clear up any duplicates in the data. 


# ---------- Load the data --------------------
import pandas as pd

books = pd.read_csv("data/library.csv")
customers = pd.read_csv("data/library_customers.csv")

print("Original library data shape:")
print(books.shape)

print("\nOriginal customer data shape:")
print(customers.shape)


# ------------ See what is missing -------------


print("\nMissing library.csv (books)")
print(books.isna().sum())

print("\nMissing in library_customers.csv (customers)")
print(customers.isna().sum())


# ---------Clear out the empty cells from the example data-------

books_clean = books.dropna(how="all").copy()  # note, how="all" only removes when all the columns are empty
customers_clean = customers.dropna(how="all").copy()

print("\nLibrary shape after removing empty rows:")
print(books_clean.shape)

print("\nCustomer shape after removing empty rows:")
print(customers_clean.shape)


# ----- see partially incomplete records still in the "clean" version of data-------------

incomplete_books = books_clean[books_clean.isna().any(axis=1)]
print("\nPartially incomplete library records:")
print(incomplete_books)



# ------------------------------------------------------------
# 5. CLEAN AND VALIDATE DATE FIELDS
# ------------------------------------------------------------

# Remove unwanted quotation marks and spaces from Book checkout.
# The source data contains checkout dates surrounded by quote
# characters which are not required as part of the date value.

books_clean["Book checkout"] = (
    books_clean["Book checkout"]
    .astype("string")
    .str.replace('"', '', regex=False)
    .str.strip()
)

# Convert both date columns to genuine Pandas datetime values.
#
# errors="coerce" converts an invalid date to NaT (Not a Time)
# instead of causing the program to fail. This makes invalid dates
# easy to identify.
#
# format="%d/%m/%Y" specifies the expected UK date format.

books_clean["Book checkout"] = pd.to_datetime(
    books_clean["Book checkout"],
    format="%d/%m/%Y",
    errors="coerce"
)

books_clean["Book Returned"] = pd.to_datetime(
    books_clean["Book Returned"],
    format="%d/%m/%Y",
    errors="coerce"
)

# Display records containing dates that could not be converted.
# For example, a date containing an impossible day of the month
# will have been converted to NaT.

invalid_checkout_dates = books_clean[
    books_clean["Book checkout"].isna()
]

print("\nRecords containing invalid checkout dates:")
print(invalid_checkout_dates)


# ------------------------------------------------------------
# 6. FIND LOGICALLY INCORRECT DATES
# ------------------------------------------------------------

# A date can be technically valid but still be incorrect.
# For example, a book should not normally be returned before
# its checkout date.
#
# This check finds records where the return date occurs before
# the checkout date.

return_before_checkout = books_clean[
    books_clean["Book Returned"] < books_clean["Book checkout"]
]

print("\nRecords where return date is before checkout date:")
print(return_before_checkout)


# ------------------------------------------------------------
# 7. LOOK FOR UNEXPECTED CHECKOUT YEARS
# ------------------------------------------------------------

# Checking the range of years can identify values which are valid
# dates syntactically but appear inconsistent with the rest of the data.
#
# Most transactions in this example are from 2023. A very different
# year should therefore be investigated rather than automatically
# changed, because we cannot safely assume what the correct year is.

unexpected_years = books_clean[
    books_clean["Book checkout"].notna()
    & (books_clean["Book checkout"].dt.year != 2023)
]

print("\nCheckout dates with an unexpected year:")
print(unexpected_years)


# ------------------------------------------------------------
# 8. CHECK FOR DUPLICATE TRANSACTIONS
# ------------------------------------------------------------

# First check for completely duplicated rows.
print("\nNumber of completely duplicated library rows:")
print(books_clean.duplicated().sum())

# A duplicate transaction may have been assigned a different Id,
# so checking the complete row is not sufficient.
#
# We therefore check the business data while excluding the unique
# Id column. This identifies transactions where the book, dates,
# borrowing period and customer are all duplicated.

transaction_columns = [
    "Books",
    "Book checkout",
    "Book Returned",
    "Days allowed to borrow",
    "Customer ID"
]

duplicate_transactions = books_clean[
    books_clean.duplicated(
        subset=transaction_columns,
        keep=False
    )
]

print("\nPossible duplicate transactions:")
print(duplicate_transactions)

# Remove duplicate transactions while retaining the first occurrence.
books_clean = books_clean.drop_duplicates(
    subset=transaction_columns,
    keep="first"
)


# ------------------------------------------------------------
# 9. VALIDATE CUSTOMER IDs
# ------------------------------------------------------------

# A Customer ID recorded against a library transaction should exist
# in the customer master data.
#
# isin() compares the Customer IDs in the transaction data with
# those in the customer file. Records which do not have a matching
# customer are reported for investigation.

invalid_customer_ids = books_clean[
    books_clean["Customer ID"].notna()
    & ~books_clean["Customer ID"].isin(customers_clean["Customer ID"])
]

print("\nLibrary records containing an unknown Customer ID:")
print(invalid_customer_ids)


# ------------------------------------------------------------
# 10. FINAL DATA QUALITY CHECK
# ------------------------------------------------------------

print("\nMissing values remaining after cleaning:")
print(books_clean.isna().sum())

print("\nFinal library data shape:")
print(books_clean.shape)

print("\nCleaned library data:")
print(books_clean)


# ------------------------------------------------------------
# 11. SAVE THE CLEANED DATA
# ------------------------------------------------------------

# Save the cleaned DataFrames as new files.
# The original source files are not overwritten so that the raw
# source data is retained and the cleaning process is reproducible.

books_clean.to_csv("data/library_cleaned.csv", index=False)
customers_clean.to_csv("data/library_customers_cleaned.csv", index=False)

print("\nCleaning complete.")
print("Cleaned files have been saved in the data folder.")