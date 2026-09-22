print('David Rees - Testing')
import pandas as pd
 
books = pd.read_csv("data/library.csv") # stored CSV in a dataframe
print (books)
books.shape # show number of rows and columns = [114 rows x 6 columns]

customers = pd.read_csv("data/library_customers.csv") # stores CSV in a dataframe
#print (customers)
#customers.shape #

books.shape  # print dimensions of my data frame
books.isnull().all().sum()  # count empty values in "books"
real = books.dropna(how="all")

print(real.shape)
print(real)

books['Id'] #print to the id column in the dataframe
three_books=books['Id'].head(3).tolist() # using key value pair mapping to identify 3 books from top

print(three_books)

print(books.dtypes)  # identify the type of datatype the df is
# pandas will use when given NaN errors, text, etc)
# pd.to_datetime(arg, error=coerce) # coerce is a error hunting tool, which strips the standard process of
# "raise error" aware from nan, etc values, so we can perform agg (sum, max, etc) functions on a series/df
silence_the_errors = pd.to_datetime(books['Book checkout'], errors="coerce", dayfirst=True)
print(silence_the_errors.dtype)
print(silence_the_errors.notna)
print(silence_the_errors.isnull().sum())
print(silence_the_errors.isna().sum())