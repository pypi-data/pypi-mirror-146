# -*- coding: utf-8 -*-
# copyright 2014-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

from unittest import TestCase, main

import sys
import os
from subprocess import Popen, PIPE
from io import BytesIO

from cubicweb_subprocess.utils import communicate


class TestCommunicate(TestCase):
    def test_stdout_stderr(self):
        pycode = r'''import sys
sys.stdout.write('\N{RIGHTWARDS ARROW}' * 666)
sys.stdout.flush()
sys.stderr.write('\N{LEFTWARDS ARROW}' * 200)
sys.stderr.flush()
'''
        outputs = {'stdout': BytesIO(),
                   'stderr': BytesIO()}
        cmdline = [sys.executable, '-c', pycode]
        proc = Popen(cmdline, stdout=PIPE, stderr=PIPE)
        for name, content in communicate(proc, chunk_size=500):
            outputs[name].write(content)

        self.assertEqual('→' * 666, outputs['stdout'].getvalue().decode('utf-8'))
        self.assertEqual('←' * 200, outputs['stderr'].getvalue().decode('utf-8'))

    def test_tiny_lines(self):
        pycode = r'''import sys
print('toto')
sys.stdout.flush()
print('tata')
sys.stdout.flush()
'''
        outputs = {'stdout': [],
                   'stderr': []}
        cmdline = [sys.executable, '-c', pycode]
        proc = Popen(cmdline, stdout=PIPE, stderr=PIPE)
        for name, content in communicate(proc, chunk_size=500):
            outputs[name].append(content)

        self.assertEqual(2, len(outputs['stdout']))
        self.assertEqual(0, len(outputs['stderr']))
        self.assertEqual(
            [
                ('toto' + os.linesep).encode('utf-8'),
                ('tata' + os.linesep).encode('utf-8')
            ],
            outputs['stdout']
        )


if __name__ == '__main__':
    main()
