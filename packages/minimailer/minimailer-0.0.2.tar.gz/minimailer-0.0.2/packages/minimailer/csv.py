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
import csv
import os, subprocess

class MinimailerCSV:
    """Send emails according to a CSV input with fields and templating support"""

    def __init__(self, args):
        self.args = args
        self.data = []

        if os.path.exists(args.template_file[0]):
            with open(args.template_file[0], 'r') as template_file:
                self.template = template_file.read()
        else:
            raise FileNotFoundError('No such file ' + template_file)

        if os.path.exists(args.csv_file[0]):
            with open(args.csv_file[0], newline='') as csv_file:
                self.csv = csv.DictReader(csv_file,
                        delimiter=args.delimiter,
                        quotechar=args.quotechar,
                        )

                for row in self.csv:
                    self.data.append(row)

        else:
            raise FileNotFoundError('No such file ' + csv_file)

    def send(self):
        for item in self.data:
            print('Sending message to {}...'.format(item[self.args.recipient_field_address]))

            message = self.template.format(**item)

            with subprocess.Popen('{sendmail} {recipient}'.format(
                message=message,
                sendmail=self.args.sendmail_command,
                recipient=item[self.args.recipient_field_address],
                ), text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) as proc:

                proc.stdin.write(message)
                proc.stdin.close()

