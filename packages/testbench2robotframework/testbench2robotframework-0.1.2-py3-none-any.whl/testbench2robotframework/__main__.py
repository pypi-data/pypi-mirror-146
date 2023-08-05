# Copyright 2022-     imbus AG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import robot

from testbench2robotframework.utils import arg_parser
from testbench2robotframework.testbench2robotframework import testbench2robotframework
from testbench2robotframework import __version__


def run():
    args = arg_parser.parse_args()
    if args.version:
        print_version()
    testbench2robotframework(args.jsonReport, args.config)


def print_version():
    print(
        f'TestBench2RobotFramework {__version__} with '
        f'[Robot Framework {robot.version.get_full_version()}]'
    )
    sys.exit()


if __name__ == "__main__":
    run()
