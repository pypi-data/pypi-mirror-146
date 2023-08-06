# Minimailer

Minimailer is a small script to send automated emails.

It's feeded from a template file and from a CSV data file, sending one email
per CSV row after applying substitutions according to template rules that matches
the data columns.

## Dependencies

Minimailer has minimal dependencies:

* [Python 3](https://python.org).
* A sendmail-compatible program (defaults to [msmtp](https://marlam.de/msmtp/)).

It was successfully tested in [Debian](https://debian.org) but should run in
other systems without problems.

## Installation

Minimailer can live anywhere in your `$PATH` or run directly from the repository.

You can also install Minimailer from [PyPI](https://pypi.org) using

    pip install minimailer

## Basic usage

Minimailer only needs two parameters, the template and the data filenames:

    minimailer message.tmpl data.csv

## CSV file format

* Minimailer uses the first row in the CSV file as field names.
* All other rows are considered as data.
* There are no constraints about which or how many fields can be used.
* The only requirement is that one of those fields should be used as the email address source.
* By default, the field named `email` is used for email addresses, and can be
  overriden by the `--recipient-field-address` option.

## Template file format

Minimailer relies in Python 3's [str.format()
syntax](https://docs.python.org/3/library/string.html#formatstrings), meaning that any text
file can be used as long as:

1. Template variables are enclosed in curly braces like `{this}`.
2. It implements a valid email message, i.e, it's compatible if the format specified by
   [RFC 2822](https://datatracker.ietf.org/doc/html/rfc2822).

## Advanced usage

Minimailer also comes with optional parameters allowing things such as handling
email addresses in a custom `contact` field as indicated above:

    minimailer message.tmpl data.csv --recipient-field-address 'contact'

Or using a custom `sendmail` invocation (in this case, `msmtp` with the account
name `my-account`):

    minimailer message.tmpl data.csv --sendmail-command 'msmtp -a my-account'

Check `minimailer --help` for details and more invocation options.

## Examples

Check the following files for examples in how to structure your template file
and data source:

* [Data source example](examples/data.csv).
* [Email template example](examples/message.tmpl).
