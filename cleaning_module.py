# Exercise 3 - Cleaning data using Python
# David Rees 22/08/2026  (with some help from ChatGPT)


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

#-----------------------------------------------------------------
# ---------- Load the data --------------------
import pandas as pd

books = pd.read_csv("data/library.csv")
customers = pd.read_csv("data/library_customers.csv")

print("Original library data shape:")
print(books.shape)

print("\nOriginal customer data shape:")
print(customers.shape)


#-----------------------------------------------------------------
# ------------ See what is missing -------------


print("\nMissing library.csv (books)")
print(books.isna().sum())

print("\nMissing in library_customers.csv (customers)")
print(customers.isna().sum())


#-----------------------------------------------------------------
# ---------Clear out the empty cells from the example data-------

books_clean = books.dropna(how="all").copy()  # note, how="all" only removes when all the columns are empty
customers_clean = customers.dropna(how="all").copy()

print("\nLibrary shape after removing empty rows:")
print(books_clean.shape)

print("\nCustomer shape after removing empty rows:")
print(customers_clean.shape)


# -- see partially incomplete records still in the "clean" data-------------

incomplete_books = books_clean[books_clean.isna().any(axis=1)]
print("\nPartially incomplete library records:")
print(incomplete_books)



# ------------------------------------------------------------
#-------- Fix any data that is in the wrong format------------------

# for the date fields, first remove the quotation marks
books_clean["Book checkout"] = (
    books_clean["Book checkout"]
    .astype("string")
    .str.replace('"', '', regex=False)
    .str.strip()
)

# -- convert to d/M/Y format
# errors="coerce" converts invalid dates to NaT (Not a Time)
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


# --display rows with invalid dates
invalid_checkout_dates = books_clean[
    books_clean["Book checkout"].isna()
]
print("\nRecords containing invalid Book checkout date")
print(invalid_checkout_dates)


#--display rows where return date is before checkout date

return_before_checkout = books_clean[
    books_clean["Book Returned"] < books_clean["Book checkout"]
]

print("\nReturn date is before checkout date:")
print(return_before_checkout)


#--Checkout date over 10 years ago or in the future

today = pd.Timestamp.today().normalize()
long_time_ago = today - pd.DateOffset(years=10)

unexpected_dates = books_clean[
    books_clean["Book checkout"].notna()
    & (
        (books_clean["Book checkout"] > today)
        | (books_clean["Book checkout"] < long_time_ago)
    )
]

print("\nCheckout dates in the future or a long time ago")
print(unexpected_dates)



#-----------------------------------------------------------------
# -------------Clear up duplicates in the data----------------
print("\nNumber of completely duplicated library rows:")
print(books_clean.duplicated().sum())

# -- check duplicated (except ID)
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

print("\nPossible duplicates:")
print(duplicate_transactions)

# -- remove duplicates
books_clean = books_clean.drop_duplicates(
    subset=transaction_columns,
    keep="first"
)



#--Check Custoemr ID's in library books exists in the customers table

invalid_customer_ids = books_clean[
    books_clean["Customer ID"].notna()
    & ~books_clean["Customer ID"].isin(customers_clean["Customer ID"])
]

print("\nLibrary book records containing an unknown Customer")
print(invalid_customer_ids)


# ------------------------------------------------------------
# --- Summarise clean shape of the data

print("\nMissing values remaining after cleaning:")
print(books_clean.isna().sum())

print("\nFinal library data shape:")
print(books_clean.shape)

print("\nCleaned library data:")
print(books_clean)


# ------------------------------------------------------------
#------------ Save the cleaned data -----------

books_clean.to_csv("data/library_cleaned.csv", index=False)
customers_clean.to_csv("data/library_customers_cleaned.csv", index=False)

print("\nCleaning complete.")
print("Cleaned files have been saved in the data folder.")



#--- How to Upload to git---------------
# cls
# git status
# git add .
# git commit -m "Excercise 3 additional data checks"
# git push
# view details at https://github.com/davidmrees1973/act5p2_library_project