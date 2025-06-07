I made this script to help me write user-defined data types by defining the children in a csv file.
The script:
* checks for duplicate names.
* writes the name in pascal case
* prefixes the name with the data type abbreviation (hungarian notation).
* sums the size of each object to get the size of the UDT.
* [todo] indicates the byte in which each object is located.

To use it:
1. Define the data-type in the definition.csv, follow the sample.
2. Execute the script, the result is written to udt.csv
