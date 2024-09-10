
# CMoAT (Cancer Multi-Omics Analysis Toolkit)

![GitHub License](https://img.shields.io/github/license/ZhangSamantha9/CMoAT)
![Pypi Version](https://img.shields.io/pypi/v/cmoat)
![Workflow Status](https://img.shields.io/github/workflow/status/ZhangSamantha9/CMoAT/upload-to-pypi.yml)

CMoAT (Cancer Multi-Omics Analysis Toolkit) is a Python-based toolkit designed for analyzing cancer genomics and proteomics data. The manual provides information on how to use and install the toolkit, as well as its features and functions.


## 1. Usage:
   - CLI (Command Line Interface): After installation, CMoAT can be used via command line in the terminal.
   - GUI (Graphical User Interface): Not implemented yet.

## 2. Installation:
   - CMoAT can be installed using pip with the command: `pip install cmoat`

## 3. Features:
   - Protein Correlation Scatter Plot: Creates scatter plots of two genes' expression with a fitted straight line, including correlation coefficient and p-value.
   - Dual Survival Analysis: Generates survival curves for high (0.75/0.75) and low (0.25/0.25) expression of both genes simultaneously.
   - Expression Boxplot (one gene): Produces a box plot comparing tumor and normal tissue protein expression for a single gene.
   - Single Gene Survival Analysis: Creates monogenic survival curves.
   - Normal Tissue Expression: Generates a bar chart showing the expression of one gene across multiple human normal tissues.
  