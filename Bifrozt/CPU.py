"""
Copyright (c) 2015, Are Hansen - Honeypot Development

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list
of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or other
materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND AN
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


__author__ = 'are@bifrozt.com'
__date__ = '2015, Jan 22'
__version__ = '0.0.2'


import datetime
import sys
try:
    import psutil
except ImportError, err:
    print 'ImportError: {0}'.format(err)
    sys.exit(1)


class Proc(object):
    """Interacts with system processes. """

    def __init__(self):
        """Explanation:
        self.start: Execution start time
        self.rcode: Return code for those who dont have one
        self.rfail: String holding any exception/error messages. """
        self.start = datetime.datetime.now()
        self.rcode = 0
        self.rfail = ''


    def use(self, sti):
        """Samples the CPU usage percent over number of seconds defined by sti and returns
        a float. """
        return psutil.cpu_percent(interval=sti)


    def kill(self, pname):
        """Attempts to use SIGTEM to terminate any process(es) belonging to 'pname'. If
        SIGTERM is ignored it will escalate and use SIGKILL to kill the processes. Returns
        a list containing the return code, 0 on sucsess and 1 on failure, and the time it
        took to preform the task.

        Position    Type    Contents
        --------    ----    ----------
        0           int     Exit code from the command
        1           str     None on sucsess, error message on failure
        2           str     Execution time
        """
        for proc in psutil.process_iter():
            if pname in proc.name:
                try:
                    proc.terminate()
                except psutil.AccessDenied, err:
                    self.rcode = 1
                    self.rfail = 'AccessDenied{0}'.format(err)
                    break

            if pname in proc.name:
                proc.terminate()

        xtime = datetime.datetime.now() - self.start
        return [self.rcode, self.rfail, str(xtime)]

