#!/usr/bin/env python3

'''
bcal (Byte CALculator) test script

Author: Arun Prakash Jana
Email : engineerarun@gmail.com
Home  : https://github.com/jarun/bcal

NOTES:

1. Use the `-l` (light mode) option to print and
   verify against minimal output in decimal bytes

2. Before raising a PR,
   a. add relevant test cases
   b. run `make test`
'''

import pytest
import subprocess

test = [
    ('./bcal', '-m', '10', 'mb'),                                      # 1
    ('./bcal', '-m', '10', 'TiB'),                                     # 2
    ('./bcal', '-m', '.1', '   KIb    '),                              # 3
    ('./bcal', '-m', '.1', 'KB  '),                                    # 4
    ('./bcal', '-m', '10', 'lb'),                                      # 5
    ('./bcal', '-m', "0x4         kb   *  2     +   5        mib"),    # 6
    ('./bcal', '-m', "5*5*5*5     mIB"),                               # 7
    ('./bcal', '-m', "5mb*5*5*5"),                                     # 8
    ('./bcal', '-m', "5 tb / 12"),                                     # 9
    ('./bcal', '-m', "2kb+3mb/4*5+5*56mb"),                            # 10
    ('./bcal', '-m', "( 5 * 3) * (4 * 7 b)"),                          # 11
    ('./bcal', '-m', "( 5 * 3 + 8) * (4 * 7 b)"),                      # 12
    ('./bcal', '-m', "( 5 * (3 + 8 )) * (4 * 7 b )"),                  # 13
    ('./bcal', '-m', "( 5 ) * 2 mib"),                                 # 14
    ('./bcal', '-m', "3   mb -  2    mib"),                            # 15
    ('./bcal', '-m', "2mb-3mib"),                                      # 16
    ('./bcal', '-m', "2 mib * -2"),                                    # 17
    ('./bcal', '-m', "2mib*-2"),                                       # 18
    ('./bcal', '-m', "2giB*2/2"),                                      # 19
    ('./bcal', '-m', "1miB / 4 kib"),                                  # 20
    ('./bcal', '-m', "(2giB*2)/2kib"),                                 # 21
    ('./bcal', '-m', "1b / 0"),                                        # 22
    ('./bcal', '-m', "2qB*2"),                                         # 23
    ('./bcal', '-m', "((2giB)*2/2)"),                                  # 24
    ('./bcal', '-m', "((2giB)*(2/2)"),                                 # 25
    ('./bcal', '-m', "((2giB)*1)/(2/2))"),                             # 26
    ('./bcal', '-m', "((2giB)*1)/(2/2)"),                              # 27
    ('./bcal', '-m', "(((2giB)*)2/2)"),                                # 28
    ('./bcal', '-m', "(2giB)*2*"),                                     # 29
    ('./bcal', '-m', '0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111', 'b'),  # 30
    ('./bcal', '-m', '0xffffffffffffffffffffffffffffffff', 'b'),       # 31
    ('./bcal', '-m', '340282366920938463463374607431768211455', 'b'),  # 32
    ('./bcal', '-m', '0xffffffffffffffff', 'b'),                       # 33
    ('./bcal', '-m', "2b / 3"),                                        # 34
    ('./bcal', '-m', "2 kIb/((3 ) )"),                                 # 35
    ('./bcal', '-m', "2 gIb/ - 3"),                                    # 36
    ('./bcal', '-m', "(2) kIb/((3))"),                                 # 37
    ('./bcal', '-m', "(2) 4 kIb/((3))"),                               # 38
    ('./bcal', '-m', "(2) 4 kIb/((3))(2)"),                            # 39
    ('./bcal', '-m', "2 / 3 tib   "),                                  # 40
    ('./bcal', '-m', " 1000 "),                                        # 41
    ('./bcal', '-m', " 0x1234mib  "),                                  # 42
    ('./bcal', '-m', "        "),                                      # 43
    ('./bcal', '-m', "0x18mb"),                                        # 44
    ('./bcal', '-m', "0x18mb", "kb"),                                  # 45
    ('./bcal', '-m', "0x18mb82"),                                      # 46
    ('./bcal', '-m', "0x18mbc4"),                                      # 47
    ('./bcal', '-m', "0x18mb 82"),                                     # 48
    ('./bcal', '-m', "0x18mb", "82"),                                  # 49

    ('./bcal', "-c", "0b"),                                            # 50
    ('./bcal', "-c", "0x"),                                            # 51
    ('./bcal', "-c", "0"),                                             # 52
    ('./bcal', "-c", "0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"),   # 53
    ('./bcal', "-c", "0xffffffffffffffffffffffffffffffff"),            # 54
    ('./bcal', "-c", "340282366920938463463374607431768211455"),       # 55
    ('./bcal', "-c", "0b1111111111111111111111111111111111111111111111111111111111111111"),                                                                   # 56
    ('./bcal', "-c", "0b111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"),  # 57
    ('./bcal', '-m', "1kib/ 4kb"),                                     # 58
    ('./bcal', '-m', "0kib /4kb"),                                     # 59
    ('./bcal', '-m', "{10+2"),                                         # 60
    ('./bcal', '-m', "10 + 2]"),                                       # 61
]

res = [
    b'10000000 B\n',                                 # 1
    b'10995116277760 B\n',                           # 2
    b'102 B\n',                                      # 3
    b'100 B\n',                                      # 4
    b'ERROR: unknown unit\n',                        # 5
    b'5250880 B\n',                                  # 6
    b'655360000 B\n',                                # 7
    b'625000000 B\n',                                # 8
    b'WARNING: result truncated\n416666666666 B\n',  # 9
    b'283752000 B\n',                                # 10
    b'420 B\n',                                      # 11
    b'644 B\n',                                      # 12
    b'1540 B\n',                                     # 13
    b'10485760 B\n',                                 # 14
    b'902848 B\n',                                   # 15
    b'ERROR: negative result\n',                     # 16
    b'ERROR: negative token\n',                      # 17
    b'ERROR: negative token\n',                      # 18
    b'2147483648 B\n',                               # 19
    b'256\n',                                        # 20
    b'2097152\n',                                    # 21
    b'ERROR: division by 0\n',                       # 22
    b'ERROR: unknown unit\n',                        # 23
    b'2147483648 B\n',                               # 24
    b'ERROR: unbalanced expression\n',               # 25
    b'ERROR: unbalanced expression\n',               # 26
    b'2147483648 B\n',                               # 27
    b'ERROR: invalid token\n',                       # 28
    b'ERROR: invalid token\n',                       # 29
    b'340282366920938463463374607431768211455 B\n',  # 30
    b'340282366920938463463374607431768211455 B\n',  # 31
    b'340282366920938463463374607431768211455 B\n',  # 32
    b'18446744073709551615 B\n',                     # 33
    b'WARNING: result truncated\n0 B\n',             # 34
    b'WARNING: result truncated\n682 B\n',           # 35
    b'ERROR: negative token\n',                      # 36
    b'ERROR: invalid expression\n',                  # 37
    b'WARNING: result truncated\nERROR: invalid expression\n',  # 38
    b'WARNING: result truncated\nERROR: invalid expression\n',  # 39
    b'ERROR: unit mismatch in /\n',                  # 40
    b'1000 B\n',                                     # 41
    b'4886364160 B\n',                               # 42
    b'ERROR: invalid value\n',                       # 43
    b'24000000 B\n',                                 # 44
    b'ERROR: malformed input\n',                     # 45
    b'ERROR: malformed input\n',                     # 46
    b'ERROR: malformed input\n',                     # 47
    b'ERROR: malformed input\n',                     # 48
    b'ERROR: unknown unit\n',                        # 49

    b'ERROR: invalid input\n',                       # 50
    b'ERROR: invalid input\n',                       # 51
    b'\x1b[1mBASE CONVERSION\x1b[0m\n (b) 0b0\n (d) 0\n (h) 0x0\n\n',  # 52
    b'\x1b[1mBASE CONVERSION\x1b[0m\n (b) 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111\n (d) 340282366920938463463374607431768211455\n (h) 0xffffffffffffffffffffffffffffffff\n\n',  # 53
    b'\x1b[1mBASE CONVERSION\x1b[0m\n (b) 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111\n (d) 340282366920938463463374607431768211455\n (h) 0xffffffffffffffffffffffffffffffff\n\n',  # 54
    b'\x1b[1mBASE CONVERSION\x1b[0m\n (b) 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111\n (d) 340282366920938463463374607431768211455\n (h) 0xffffffffffffffffffffffffffffffff\n\n',  # 55
    b'\x1b[1mBASE CONVERSION\x1b[0m\n (b) 0b1111111111111111111111111111111111111111111111111111111111111111\n (d) 18446744073709551615\n (h) 0xffffffffffffffff\n\n',  # 56
    b'ERROR: invalid input\n',                       # 57
    b'WARNING: result truncated\n0\n',               # 58
    b'0\n',                                          # 59
    b'ERROR: first brackets only\n',                 # 60
    b'ERROR: first brackets only\n',                 # 61
]


@pytest.mark.parametrize('item, res', zip(test, res))
def test_output(item, res):
    try:
        out = subprocess.check_output(item, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        # print(e.output)
        assert e.output == res
    else:
        assert out == res
