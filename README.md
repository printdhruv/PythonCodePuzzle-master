# Build a Web API

##

Staples needs a new report. We have access to session data from a 3rd party
vendor, which is formatted as a pipe-delimited file. Staples also has internal
data stored in a CSV file.  The web application should compare the data in the
two files, and build a report which shows the discrepancies.

## Requirements

* You need to create a web service with a single route, which generates a report
  as described in the [expected api response](resources/expected-api-responses.json).

* Our top priority is to allow a developer to demonstrate that he or she is skilled in
  his or her craft. If you believe that you can demonstrate this best by
  completing the puzzle in a different language, then use that language.

* For a Python solution, a virtualenv folder will be created by the `bin/pyenv` 
  helper script. You can also use the `bin/pyrun` and `bin/pytest` helper scripts
  to run your server and test cases.

## API routes:

* /analytics/report - route which returns the report data. It takes a parameter `order_by`, which can be any of these 3 values
  * `session-type-desc`         - sort by `session-type` in descending order
  * `order-id-asc`              - sort by `order-id` in ascending order
  * `unit-price-dollars-asc`    - sort by `unit-price-dollars` in ascending order<br />

[This](resources/expected-api-responses.json) file has the above 3 use cases.

## Caveats:

* DO NOT use a specialized CSV-parsing library to parse either of the
  character-delimited files. There are many libraries available to parse
  character delimited files. Do not use them. It is perfectly fine to use a
  libary that parses text into numbers, or one which handles regular
  expressions. However, we would like to see you write the code that parses the
  actual file. Don't worry about the edge cases of parsing the CSV/PSV
  files. Just do enough to parse the 2 files. For any of the non-parsing parts
  of the application you are free to use any libraries you want (from Clojars or
  Maven Central, etc).

* It is fine to use a json processing library if you are interested in
  reading the `expected-api-reponse.json` file for any reason.

* Notice that the order of the columns in the Staples data file and the Merchant
  data file are different, and the prices in the Staples data file are in cents,
  while the prices in the Merchant file are in dollars.

## Inputs

  * Files located in the resources folder
    * [Merchant Data File](resources/external_data.psv) is the data from 3rd party vendor.
    * [Staples Data File](resources/staples_data.csv) is the data stored in Staples's database

## Outputs

Look at this file - [expected api response](expected-api-responses.json)

## Questions and clarifications:

If you have questions about the code puzzle, email stephon@stapleslabs.com for
clarifications.

## Solution Submission

Fork the project, and send an email to careers@stapleslabs.com once you're done.

There are no points given for speed, so please take as much time as you desire,
so that you can submit your best work.

Have fun! :)
