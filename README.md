# Library Data Quality Analysis Project

## Project Overview

This project was developed as part of the Data Engineering Product Development module.

The scenario is based on a library that currently performs data quality analysis manually. The aim of the project is to improve the efficiency and reliability of this process by using Python, automated testing, CI/CD and containerisation.

The solution takes source library and customer CSV data, identifies and corrects data quality issues, produces cleaned datasets and performs analysis ready for presentation.

The project also demonstrates software development and data engineering practices including source control with GitHub, unit testing with Pytest, automated CI/CD workflows using GitHub Actions, and application containerisation using Docker.


## Repository Structure

```text
act5p2_library_project/
│
├── .github/
│   └── workflows/
│       ├── main.yml
│       └── docker_ci.yml
│
├── data/
│   ├── library.csv
│   ├── library_customers.csv
│   ├── library_cleaned.csv
│   └── library_customers_cleaned.csv
│
├── docker/
│   └── Dockerfile
│
├── docs/
│   └── Project documentation and screenshots
│
├── pipeline/
│   └── Pipeline development files
│
├── src/
│   ├── cleaning_module.py
│   └── presentation_module.py
│
├── tests/
│   ├── fundamentals_testing.py
│   └── testing_module.py
│
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```


## Solution Architecture

The project follows a simple data engineering workflow:

```text
Source CSV Data
       |
       v
Python / Pandas
Data Cleaning
       |
       v
Cleaned CSV Data
       |
       +--------------------+
       |                    |
       v                    v
    Pytest             Data Analysis
 Unit Testing           Matplotlib
       |
       v
GitHub Actions CI
       |
       v
Docker Build
       |
       v
Docker Container
```

The source data is processed using Python and Pandas. Automated tests are used to validate the application, while GitHub Actions provides CI/CD automation.

Docker is then used to package the Python application and its dependencies into a portable container image.


## Technologies Used

- **Python 3.14** - application development
- **Pandas** - data manipulation and cleaning
- **NumPy** - supporting data processing
- **Pytest** - automated unit testing
- **Matplotlib** - data analysis visualisations
- **Git / GitHub** - source control and repository management
- **GitHub Actions** - CI/CD automation
- **Docker** - application containerisation
- **Visual Studio Code** - development environment


## Processing Workflow

The main processing workflow is:

1. Read the source library and customer CSV files.
2. Inspect the datasets for missing or invalid data.
3. Remove completely empty records.
4. Clean book titles.
5. Standardise and correct date fields.
6. Apply data quality corrections where appropriate.
7. Identify loans reaching or exceeding the permitted borrowing period.
8. Write cleaned datasets back to the `data` folder.
9. Run automated Pytest tests.
10. Analyse the cleaned data and produce presentation outputs.


## Data Quality Processing

The `cleaning_module.py` module performs a number of data quality checks and corrections.

These include:

- Removing leading and trailing spaces from book titles.
- Removing completely empty rows.
- Converting date columns into valid Python datetime values.
- Correcting inconsistent date formats.
- Handling invalid or missing dates.
- Identifying loans that meet or exceed the allowed borrowing period.
- Producing cleaned versions of the library and customer datasets.

The cleaned files are saved as:

```text
data/library_cleaned.csv
data/library_customers_cleaned.csv
```


## Overview of Python Scripts

### cleaning_module.py

The main application responsible for loading, cleaning, validating and exporting the library data.

Run from the project root using:

```bash
python src/cleaning_module.py
```


### presentation_module.py

Uses the cleaned datasets to perform analysis and produce presentation outputs.

The analysis includes:

- Number of books checked out by each customer.
- Loans of 14 days or more.
- Longest valid book loan.
- Shortest valid book loan.
- Month with the most checkout records.
- Month with the least checkout records.
- List of books within the cleaned dataset.
- Matplotlib visualisations of the results.

Run using:

```bash
python src/presentation_module.py
```


## Unit Testing

Pytest is used to test functions within the application.

The tests validate important cleaning functionality rather than testing a separate copy of the code.

Tests can be run from the project root using:

```bash
python -m pytest tests/testing_module.py -v
```

The use of `python -m pytest` ensures Pytest runs using the active Python environment and that the project root is available for module imports.


## GitHub CI/CD

Two GitHub Actions workflows are included in the project.

### Main CI Workflow

The main workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs project dependencies.
4. Runs the Pytest unit tests.
5. Confirms that the application passes the automated test stage.

The workflow runs automatically when changes are pushed to the `main` branch.


### Docker CI/CD Workflow

A second workflow extends the CI process to Docker.

The workflow:

1. Runs the Python unit tests.
2. Only continues to the Docker build if the tests pass.
3. Builds the Docker image.
4. Runs the application from the Docker image.
5. Saves the resulting Docker image as an artifact.

This prevents the Docker build stage from proceeding when the application fails its automated tests.


## Docker

The application has been containerised using Docker.

The Dockerfile:

- Uses a Python 3.14 slim base image.
- Creates an application working directory.
- Copies the project requirements.
- Installs the required Python packages.
- Copies the application files into the image.
- Runs `src/cleaning_module.py` when the container starts.

Build the Docker image from the project root:

```bash
docker build -f docker/Dockerfile -t projectapp:1.0 .
```

Run the image:

```bash
docker run --name c1 projectapp:1.0
```

A `.dockerignore` file is used to prevent unnecessary development files, caches and local environment files from being copied into the Docker build context.


## Data Analysis and Visualisation

The cleaned data is analysed using Pandas and visualised using Matplotlib.

The presentation analysis identified:

- **John Smith** had the highest number of checkouts, with **5 books**.
- **Dracula** had the longest valid loan period, at **30 days**.
- Loans meeting or exceeding the 14-day threshold were identified for further analysis.
- **April** contained the most checkout records, with **9**.
- **February** contained the fewest checkout records represented in the data, with **1**.
- Unmatched customer IDs were also identified, highlighting a referential data quality issue between the library and customer datasets.

Visualisations include:

- Books checked out by customer.
- Books exceeding the 14-day loan threshold.
- Library checkouts by month.


## Installing the Project

Create and activate a Python virtual environment, then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

The project dependencies include:

- pandas
- numpy
- pytest
- matplotlib


## Running the Complete Solution

Run the cleaning application:

```bash
python src/cleaning_module.py
```

Run the automated tests:

```bash
python -m pytest tests/testing_module.py -v
```

Run the analysis and visualisations:

```bash
python src/presentation_module.py
```

Alternatively, build and run the application using Docker:

```bash
docker build -f docker/Dockerfile -t projectapp:1.0 .
docker run --name c1 projectapp:1.0
```


## Conclusion

The project demonstrates an end-to-end data engineering development process.

A manual library data quality task has been converted into a repeatable Python application with data cleaning, automated unit testing, CI/CD, Docker containerisation and data visualisation.

Using GitHub Actions allows changes to be automatically tested, while Docker provides a consistent and portable environment in which to run the application. The cleaned data can then be analysed and presented using the separate presentation module.