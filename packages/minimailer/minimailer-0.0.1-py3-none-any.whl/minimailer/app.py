#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Send emails with templating support using a CSV file as the data source
#
# Copyright (C) 2022 Silvio Rhatto <rhatto@torproject.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Dependencies
import argparse
import subprocess

from .csv import MinimailerCSV

def cmdline():
    """Process from CLI"""

    epilog = """Examples:

      minimailer message.tmpl data.csv --sendmail-command 'msmtp -a default'
      minimailer message.tmpl data.csv --recipient-field-address 'contact'
    """

    description = 'Send emails according to a CSV input with fields and templating support'
    parser      = argparse.ArgumentParser(
                    description=description,
                    epilog=epilog,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                  )

    parser.add_argument('template_file',       nargs=1,   help='Message template filename')
    parser.add_argument('csv_file',            nargs=1,   help='CSV filename. It\'s required that the first line in the CSV contain the field names.')
    #parser.add_argument('mstmp_account_name', nargs='?', help='MSTMP account name')

    # Defaults
    sendmail_command_default        = '/usr/bin/msmtp -a default'
    recipiend_field_address_default = 'email'
    delimiter_default               = ','
    quotechar_default               = '"'

    parser.add_argument(
            '--sendmail-command',
            help='Sendmail command invocation. Defaults to ' + sendmail_command_default
            )

    parser.add_argument(
            '--recipient-field-address',
            help='Email address field in the CSV file. Defaults to ' + recipiend_field_address_default
            )

    parser.add_argument(
            '--delimiter',
            help='CSV field delimiter. Defaults to' + delimiter_default,
            )

    parser.add_argument(
            '--quotechar',
            help='CSV quotechar. Defaults to' + quotechar_default,
            )

    # Set defaults
    #parser.set_defaults(msmtp_account_name='default')
    parser.set_defaults(sendmail_command=sendmail_command_default)
    parser.set_defaults(recipiend_field_address=recipiend_field_address_default)
    parser.set_defaults(delimiter=delimiter_default)
    parser.set_defaults(quotechar=quotechar_default)

    args = parser.parse_args()

    return args

def run_from_cmdline():
    args = cmdline()

    # Dispatch
    try:
        mailer = MinimailerCSV(args)

        mailer.send()

    except (FileNotFoundError, KeyboardInterrupt, subprocess.SubprocessError) as e:
        print(e)
        exit(1)
