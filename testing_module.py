# Exercise 4 - Unit Testing
# David Rees
#
# Unit tests for functions created in Exercise 3.


# ------------------------------- IMPORTS -----------------------------
import pandas as pd

# Import the functions that we created in Exercise 3.
# This means we are testing the real function rather than
# creating another copy of it in this testing file.
from cleaning_module import clean_titles, clean_date_column
# -----------------------------------------------------------------------



def test_clean_titles_removes_trailing_spaces():
    """
    Test that clean_titles() removes leading and trailing
    whitespace from book titles.
    """

    # ARRANGE
    # Create a small test DataFrame containing deliberately
    # untidy book titles.
    test_data = pd.DataFrame({
        "Books": [
            "Dune ",
            " IT",
            " The Hobbit "
        ]
    })

    # ACT
    # Run the clean_titles function from Exercise 3.
    result = clean_titles(test_data)

    # ASSERT
    # Check that there are no book titles ending with a space.
    trailing_spaces = result["Books"].str.endswith(" ").sum()

    assert trailing_spaces == 0




def test_clean_date_column_converts_valid_date():
    """
    Test that clean_date_column() correctly converts
    a valid UK date into a Pandas datetime value.
    """

    # ARRANGE
    # Create test data containing a date in the same format
    # as the library source data.
    test_data = pd.DataFrame({
        "Book checkout": ['"20/02/2023"']
    })

    # ACT
    result = clean_date_column(test_data, "Book checkout")

    # ASSERT
    expected_date = pd.Timestamp("2023-02-20")

    assert result["Book checkout"].iloc[0] == expected_date



def test_clean_date_column_invalid_date():
    """
    Test that an impossible date is converted to NaT
    rather than causing the program to fail.
    """

    # ARRANGE
    # 32 May is deliberately invalid.
    test_data = pd.DataFrame({
        "Book checkout": ["32/05/2023"]
    })

    # ACT
    result = clean_date_column(test_data, "Book checkout")

    # ASSERT
    # pd.isna() should return True because the invalid
    # date should have been converted to NaT.
    assert pd.isna(result["Book checkout"].iloc[0])

    