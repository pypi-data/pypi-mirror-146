fdata

This tool is meant for the cleaning and creation of custom tables using FDA Adverse Event Reporting System (FAERS) data.

Download whichever quarterly files (ASCII format) you wish to analyze, and utilize these functions to expedite cleaning and organization for your project!


Installation

Run the following to install:

	pip install fdata

Note: if there are empty lists initialized before the definition, the final output of the function will be attached to these built-in lists. See example below.

Usage

	import fdata as fd

	drug_file = pd.read_csv(‘DRUG20Q1.txt’,  delimiter=‘$’)
	fd.sorter(drug_file) 

		…

		“Check ‘class_dfs’, ‘missing_dfs’, ‘new_files’, ‘positives’, and ‘inds’ for output”

    class_dfs = fd.class_dfs
    missing_dfs = fd.missing_dfs

    print(class_dfs)
    print(missing_dfs)


See function documentation for further details.