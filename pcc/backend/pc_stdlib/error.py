# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from sys import exit, stderr

def error(msg: str) -> None:
    print(msg, file=stderr)
    exit(1)