# Exercise 7 - Presenting the cleaned library data
# David Rees - 24/09/2026

import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Load CLEANED data produced by cleaning_module.py
# ------------------------------------------------------------

books = pd.read_csv("data/library_cleaned.csv")
customers = pd.read_csv("data/library_customers_cleaned.csv")

# Convert dates back to datetime after reading from CSV
books["Book checkout"] = pd.to_datetime(books["Book checkout"])
books["Book Returned"] = pd.to_datetime(books["Book Returned"])


# Calculate loan duration
books["Days borrowed"] = (
    books["Book Returned"] - books["Book checkout"]
).dt.days


# Only use valid loan durations for duration analysis.
# Negative durations indicate invalid date data and are excluded.
valid_loans = books[books["Days borrowed"] >= 0].copy()


print("\n" + "=" * 80)
print("LIBRARY DATA ANALYSIS")
print("=" * 80)


# ------------------------------------------------------------
# 1. How many books has each customer checked out?
# ------------------------------------------------------------

customer_counts = (
    books.groupby("Customer ID")
    .size()
    .reset_index(name="Books checked out")
)

# Add customer names
customer_counts = customer_counts.merge(
    customers,
    on="Customer ID",
    how="left"
)

# Some Customer IDs do not have a matching name in the customer file.
# Give these a readable label for the presentation.
customer_counts["Customer Name"] = customer_counts["Customer Name"].fillna(
    customer_counts["Customer ID"].apply(
        lambda x: f"Unknown Customer ID {int(x)}"
    )
)


print("\n1. BOOKS CHECKED OUT BY CUSTOMER")
print("-" * 80)
print(customer_counts.to_string(index=False))


# Bar chart
plt.figure(figsize=(12, 6))
plt.bar(
    customer_counts["Customer Name"],
    customer_counts["Books checked out"]
)
plt.title("Books Checked Out by Customer")
plt.xlabel("Customer")
plt.ylabel("Number of Books")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 2. Loans which exceeded the two-week threshold
# ------------------------------------------------------------

#overdue = books[books["Days borrowed"] >= 14].copy()
overdue = valid_loans[valid_loans["Days borrowed"] >= 14].copy()

overdue = overdue.merge(
    customers,
    on="Customer ID",
    how="left"
)

overdue["Customer Name"] = overdue["Customer Name"].fillna(
    overdue["Customer ID"].apply(
        lambda x: f"Unknown Customer ID {int(x)}"
    )
)

print("\n2. LOANS OF 14 DAYS OR MORE")
print("-" * 80)

print(
    overdue[
        ["Customer Name", "Books", "Book checkout",
         "Book Returned", "Days borrowed"]
    ].to_string(index=False)
)

# Bar chart showing loans of 14 days or more
plt.figure(figsize=(10, 5))

plt.bar(
    overdue["Books"],
    overdue["Days borrowed"]
)

plt.axhline(
    y=14,
    linestyle="--",
    label="14-day threshold"
)

plt.title("Books Exceeding the 14-Day Loan Threshold")
plt.xlabel("Book")
plt.ylabel("Days Borrowed")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()




# ------------------------------------------------------------
# 3. Longest checked-out book
# ------------------------------------------------------------

#longest = books.loc[books["Days borrowed"].idxmax()]

longest = valid_loans.loc[valid_loans["Days borrowed"].idxmax()]


print("\n3. LONGEST BOOK LOAN")
print("-" * 80)
print(f"Book:          {longest['Books']}")
print(f"Days borrowed: {int(longest['Days borrowed'])}")


# ------------------------------------------------------------
# 4. Shortest checked-out book
# ------------------------------------------------------------

#shortest = books.loc[books["Days borrowed"].idxmin()]

shortest = valid_loans.loc[valid_loans["Days borrowed"].idxmin()]

print("\n4. SHORTEST BOOK LOAN")
print("-" * 80)
print(f"Book:          {shortest['Books']}")
print(f"Days borrowed: {int(shortest['Days borrowed'])}")


# ------------------------------------------------------------
# 5 & 6. Checkout records by month
# ------------------------------------------------------------

books["Checkout Month"] = books["Book checkout"].dt.month_name()

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_counts = (
    books["Checkout Month"]
    .value_counts()
    .reindex(month_order, fill_value=0)
)

# Only show months represented in the data
monthly_counts_display = monthly_counts[monthly_counts > 0]

print("\n5. MONTH WITH MOST CHECKOUT RECORDS")
print("-" * 80)
print(
    f"{monthly_counts_display.idxmax()}: "
    f"{monthly_counts_display.max()} checkouts"
)

print("\n6. MONTH WITH LEAST CHECKOUT RECORDS")
print("-" * 80)
print(
    f"{monthly_counts_display.idxmin()}: "
    f"{monthly_counts_display.min()} checkouts"
)


# Monthly bar chart
plt.figure(figsize=(10, 5))
plt.bar(
    monthly_counts_display.index,
    monthly_counts_display.values
)
plt.title("Library Checkouts by Month")
plt.xlabel("Month")
plt.ylabel("Number of Checkouts")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 7. List of books on display
# ------------------------------------------------------------

print("\n7. BOOKS ON DISPLAY")
print("-" * 80)

print(books["Books"].dropna().drop_duplicates().to_string(index=False))


print("\n" + "=" * 80)
print("END OF LIBRARY DATA ANALYSIS")
print("=" * 80)


#Findings......

# Most books checked out: John Smith — 5
# Loans ≥14 days: Little Women 29 days, Dark Tales 17, Dracula 30, Frankenstein 19
# Longest valid loan: Dracula — 30 days
# Most active month: April — 9 checkouts
# Least active month represented in the data: February — 1 checkout
# unmatched Customer IDs 4 and 10.