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

# loc value vs iloc index
# books.loc('id')
output = books.loc[books.isnull().any(axis=1)].to_string() #shows rows with any NULL fields
print(output)
# when we don't let default fail/decide silently -> you decide the rows fate yourself
# the difference being in the early coerce examples, we handed control to the func, it promoted what it could
# the rest was removed

dropped_na = books.dropna(how="all") # little less harsh than any, e.g. row that is missing a single field
dropped_na.shape # gives me the updated dimension
dropped_na.isna().sum() # count for present na values, has it worked?
books.isna().sum() # compare with the above for missing value removeal
# books["loan amount..."].mean()

#filled_value = data.fillna("value") #inplace errors, see value hended back to the col with a new type
filled_value = books.fillna("value")
## this went to dtype float to int
filled_value.isnull().sum().sum() #0
#filled_value["customers"].tolist()[-1]
filled_value["Books"].tolist() # list of remaing books with value updates
#filled_value["Customer ID"].mean() # shows mean books

# #books.duplicated = true false true etc.
dropped_na.duplicated().sum #agg of the true returns
#deduped_dropped_na = dropped_na.drop_duplicates(subset="Days allowed to borrow") # com
