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

print("----------------------------------------------------------------------------------------------")
print("---------------------------Exercise 3 - Cleaning data using Python----------------------------")
print("----------------------------------------------------------------------------------------------")

#-----------------------------------------------------------------
# ---------- Load the data --------------------
import pandas as pd

books = pd.read_csv("data/library.csv")
customers = pd.read_csv("data/library_customers.csv")

print("Original library data shape:")
print(books.shape)

print("\nOriginal customer data shape:")
print(customers.shape)


#--------------------------------------------------------
#--------------- Functions -------------------------

# def display_section(title, data):
#     """Display a title followed by the supplied data."""
#     print(f"\n--- {title} ---") # could potentially add some fancy formatting here
#     print(data)

# DR 23/09/2029 New version of the function so it checks for missing data
def display_section(title, data):
    """Display a title followed by the supplied data."""

    if not title:
        raise ValueError("A section title must be provided")

    if data is None:
        raise ValueError("Section data must be provided")

    print(f"\n--- {title} ---")
    print(data)



def clean_date_column(dataframe, column_name):
    """
    Clean and convert a date column to Pandas datetime format.

    Invalid dates are converted to NaT so that they can be
    identified and investigated rather than causing an error.
    """
    dataframe[column_name] = (
        dataframe[column_name]
        .astype("string")
        .str.replace('"', '', regex=False)
        .str.strip()
    )

    dataframe[column_name] = pd.to_datetime(
        dataframe[column_name],
        format="%d/%m/%Y",
        errors="coerce"
    )

    return dataframe


def clean_titles(df):
    """Strip leading and trailing spaces from book titles."""
    out = df.copy()
    out["Books"] = out["Books"].str.strip()
    return out



def find_overdue_books(df, allowed_days=14):
    """
    Return books that were borrowed for longer than the
    permitted borrowing period.

    The default borrowing period is 14 days.
    """
    out = df.copy()

    # Calculate the number of days between checkout and return.
    out["Days borrowed"] = (
        out["Book Returned"] - out["Book checkout"]
    ).dt.days

    # Return only books borrowed for more than the allowed period.
    return out[out["Days borrowed"] >= allowed_days]  #DR 23/09/2029 changed from > to >=


#-----------------------------------------------------------------
# ------------ See what is missing -------------

display_section(
    "Missing library.csv (books)",
    books.isna().sum()
)

display_section(
    "Missing in library_customers.csv (customers)",
    customers.isna().sum()
)




#-----------------------------------------------------------------
# ---------Clear out the empty cells from the example data-------

books_clean = books.dropna(how="all").copy()  # note, how="all" only removes when all the columns are empty
customers_clean = customers.dropna(how="all").copy()

# Remove leading and trailing whitespace from book titles
books_clean = clean_titles(books_clean)


display_section(
    "Library shape after removing empty rows",
    books_clean.shape
)


display_section(
    "Customer shape after removing empty rows",
    customers_clean.shape
)




# -- see partially incomplete records still in the "clean" data-------------

incomplete_books = books_clean[books_clean.isna().any(axis=1)]

display_section(
    "Partially incomplete library records",
    incomplete_books
)



# ------------------------------------------------------------
#-------- Fix any data that is in the wrong format------------------

# for the date fields, first remove the quotation marks
# books_clean["Book checkout"] = (
#     books_clean["Book checkout"]
#     .astype("string")
#     .str.replace('"', '', regex=False)
#     .str.strip()
# )

# # -- convert to d/M/Y format
# # errors="coerce" converts invalid dates to NaT (Not a Time)
# books_clean["Book checkout"] = pd.to_datetime(
#     books_clean["Book checkout"],
#     format="%d/%m/%Y",
#     errors="coerce"
# )



# books_clean["Book Returned"] = pd.to_datetime(
#     books_clean["Book Returned"],
#     format="%d/%m/%Y",
#     errors="coerce"
# )


# The above now used a function
books_clean = clean_date_column(books_clean, "Book checkout")
books_clean = clean_date_column(books_clean, "Book Returned")

# Apply the library's 14-day borrowing rule.
overdue_books = find_overdue_books(books_clean)


# ''display overdue books
display_section(
    "Books borrowed for more than 14 days (may incude duplicates)",
    overdue_books
)


# --display rows with invalid dates
invalid_checkout_dates = books_clean[
    books_clean["Book checkout"].isna()
]


display_section(
    "Records containing invalid Book checkout date",
    invalid_checkout_dates
)



#--display rows where return date is before checkout date

return_before_checkout = books_clean[
    books_clean["Book Returned"] < books_clean["Book checkout"]
]

display_section(
    "Return date is before checkout date",
    return_before_checkout
)




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



display_section(
    "Checkout dates in the future or a long time ago",
    unexpected_dates
)


#-----------------------------------------------------------------
# -------------Clear up duplicates in the data----------------

display_section(
    "Number of completely duplicated library rows",
    books_clean.duplicated().sum()
)

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



display_section(
    "Possible duplicates:",
    duplicate_transactions
)



# -- remove duplicates
books_clean = books_clean.drop_duplicates(
    subset=transaction_columns,
    keep="first"
)


# Apply the library's 14-day borrowing rule.
overdue_books = find_overdue_books(books_clean)


# ''display overdue books
display_section(
    "Books borrowed for more than 14 days (after duplicates removed)",
    overdue_books
)




#--Check Customer ID's in library books exists in the customers table

invalid_customer_ids = books_clean[
    books_clean["Customer ID"].notna()
    & ~books_clean["Customer ID"].isin(customers_clean["Customer ID"])
]


display_section(
    "Library book records containing an unknown Customer:",
    invalid_customer_ids
)



# ------------------------------------------------------------
# --- Summarise clean shape of the data

display_section(
    "Missing values remaining after cleaning:",
    books_clean.shape
)

display_section(
    "Final library data shape:",
    invalid_customer_ids
)

display_section(
    "Cleaned library data:",
    books_clean
)


# ------------------------------------------------------------
#------------ Save the cleaned data -----------

books_clean.to_csv("data/library_cleaned.csv", index=False)
customers_clean.to_csv("data/library_customers_cleaned.csv", index=False)

print("\nCleaning complete.")
print("\nCleaned files have been saved in the data folder.")






#--- How to Upload to git---------------
# cls
# git status
# git add .
# git commit -m "Excercise 3 additional data checks"
# git push
# view details at https://github.com/davidmrees1973/act5p2_library_project