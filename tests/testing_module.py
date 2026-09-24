# Exercise 4 - Unit Testing
# David Rees (with help from ChatGPT)
#
# Unit tests for functions created in Exercise 3.


# ------------------------------- IMPORTS -----------------------------
import pandas as pd
import pytest # DR added 23/09/2026 as needed for test_display_section_missing_title()
# Import the functions that we created in Exercise 3.
# This means we are testing the real function rather than
# creating another copy of it in this testing file.
from src.cleaning_module import clean_titles, clean_date_column, find_overdue_books, display_section
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




def test_find_overdue_books_14_day_rule():
    """
    Test the library's 14-day borrowing rule.

    A book returned after 10 days should not be overdue.
    A book returned after 16 days should be overdue.
    """

    # ARRANGE
    # Create two example library transactions.
    # One is within the 14-day allowance and one exceeds it.
    test_data = pd.DataFrame({
        "Books": [
            "Book returned on time",
            "Book returned late"
        ],
        "Book checkout": [
            pd.Timestamp("2023-05-01"),
            pd.Timestamp("2023-05-01")
        ],
        "Book Returned": [
            pd.Timestamp("2023-05-11"),  # 10 days
            pd.Timestamp("2023-05-17")   # 16 days
        ]
    })

    # ACT
    # Apply the 14-day borrowing rule.
    result = find_overdue_books(test_data, allowed_days=14)

    # ASSERT
    # Only one book should be identified as overdue.
    assert len(result) == 1

    # Check that the correct book was identified.
    assert result.iloc[0]["Books"] == "Book returned late"

    # Check that the calculated borrowing period is 16 days.
    assert result.iloc[0]["Days borrowed"] == 16




def test_display_section_missing_title():
    """
    Test that display_section raises a ValueError
    when no title is supplied.
    """

    # ARRANGE
    title = ""
    data = "Some test data"

    # ACT / ASSERT
    with pytest.raises(ValueError):
        display_section(title, data)