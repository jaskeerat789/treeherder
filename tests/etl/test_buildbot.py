from treeherder.etl import buildbot
import pytest
import datetime
import time
import json

from django.conf import settings
from treeherder.etl import buildbot

slow = pytest.mark.slow

buildernames = [
    ('Android 2.2 Armv6 mozilla-inbound build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'armv6',
                   'os': 'android',
                   'os_platform': 'android-2-2-armv6',
                   'vm': False}}),
    ('Android 2.2 Armv6 Tegra mozilla-inbound opt test crashtest',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Crashtest',
               'job_symbol': 'C'},
      'platform': {'arch': 'armv6',
                   'os': 'android',
                   'os_platform': 'android-2-2-armv6',
                   'vm': False}}),
    ('Android 2.2 Armv6 Tegra mozilla-inbound opt test jsreftest-1',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'JSReftest',
               'job_symbol': 'J1'},
      'platform': {'arch': 'armv6',
                   'os': 'android',
                   'os_platform': 'android-2-2-armv6',
                   'vm': False}}),
    ('Android 2.2 Armv6 Tegra mozilla-inbound opt test mochitest-1',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Mochitest',
               'group_symbol': 'M',
               'name': 'Mochitest',
               'job_symbol': '1'},
      'platform': {'arch': 'armv6',
                   'os': 'android',
                   'os_platform': 'android-2-2-armv6',
                   'vm': False}}),
    ('Ubuntu VM 12.04 x64 mozilla-central opt test mochitest-e10s-1',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Mochitest e10s',
               'group_symbol': 'M-e10s',
               'name': 'Mochitest e10s',
               'job_symbol': '1'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': True}}),
    ('Ubuntu VM 12.04 mozilla-central opt test jittest-2',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'JIT Tests',
               'job_symbol': 'Jit2'},
      'platform': {'arch': 'x86',
                   'os': 'linux',
                   'os_platform': 'linux32',
                   'vm': True}}),
    ('Rev4 MacOSX Snow Leopard 10.6 mozilla-central debug test mochitest-devtools-chrome-2',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'Mochitest',
               'group_symbol': 'M',
               'name': 'Mochitest DevTools Browser Chrome',
               'job_symbol': 'dt2'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-6',
                   'vm': False}}),
    ('Android 2.2 Tegra mozilla-inbound opt test mochitest-6',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Mochitest',
               'group_symbol': 'M',
               'name': 'Mochitest',
               'job_symbol': '6'},
      'platform': {'arch': 'x86',
                   'os': 'android',
                   'os_platform': 'android-2-2',
                   'vm': False}}),
    ('Android 2.2 Armv6 Tegra mozilla-inbound opt test plain-reftest-1',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Reftest',
               'job_symbol': 'R1'},
      'platform': {'arch': 'armv6',
                   'os': 'android',
                   'os_platform': 'android-2-2-armv6',
                   'vm': False}}),
    ('Android 2.2 Armv6 Tegra mozilla-inbound opt test robocop-1',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Mochitest',
               'group_symbol': 'M',
               'name': 'Robocop',
               'job_symbol': 'rc1'},
      'platform': {'arch': 'armv6',
                   'os': 'android',
                   'os_platform': 'android-2-2-armv6',
                   'vm': False}}),
    ('Android 2.2 Armv6 Tegra mozilla-inbound opt test xpcshell',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'XPCShell',
               'job_symbol': 'X'},
      'platform': {'arch': 'armv6',
                   'os': 'android',
                   'os_platform': 'android-2-2-armv6',
                   'vm': False}}),
    ('Android 2.2 Debug mozilla-inbound build',
    {'build_type': 'debug',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'android',
                   'os_platform': 'android-2-2',
                   'vm': False}}),
    ('Android 2.2 mozilla-inbound build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'android',
                   'os_platform': 'android-2-2',
                   'vm': False}}),
    ('Android 2.2 Tegra mozilla-inbound opt test crashtest',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Crashtest',
               'job_symbol': 'C'},
      'platform': {'arch': 'x86',
                   'os': 'android',
                   'os_platform': 'android-2-2',
                   'vm': False}}),
    ('Android 2.2 Tegra mozilla-inbound talos remote-tcanvasmark',
    {'build_type': 'opt',
      'job_type': 'talos',
      'name': {'group_name': 'Talos Performance',
               'group_symbol': 'T',
               'name': 'Talos canvasmark',
               'job_symbol': 'cm'},
      'platform': {'arch': 'x86',
                   'os': 'android',
                   'os_platform': 'android-2-2',
                   'vm': False}}),
    ('Android 4.0 Panda mozilla-inbound talos remote-tsvgx',
    {'build_type': 'opt',
      'job_type': 'talos',
      'name': {'group_name': 'Talos Performance',
               'group_symbol': 'T',
               'name': 'Talos svg',
               'job_symbol': 's'},
      'platform': {'arch': 'x86',
                   'os': 'android',
                   'os_platform': 'android-4-0',
                   'vm': False}}),
    ('Android 4.2 x86 mozilla-inbound build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'android',
                   'os_platform': 'android-4-2-x86',
                   'vm': False}}),
    ('b2g_emulator mozilla-inbound opt test reftest-1',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Reftest',
               'job_symbol': 'R1'},
      'platform': {'arch': 'x86',
                   'os': 'b2g',
                   'os_platform': 'b2g-emu-ics',
                   'vm': False}}),
    ('b2g_mozilla-inbound_emulator_dep',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'B2G Emulator Image Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'b2g',
                   'os_platform': 'b2g-emu-ics',
                   'vm': False}}),
    ('b2g_mozilla-inbound_emulator-debug_dep',
    {'build_type': 'debug',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'B2G Emulator Image Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'b2g',
                   'os_platform': 'b2g-emu-ics',
                   'vm': False}}),
    ('b2g_mozilla-inbound_emulator-jb_dep',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'B2G Emulator Image Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'b2g',
                   'os_platform': 'b2g-emu-jb',
                   'vm': False}}),
    ('b2g_mozilla-inbound_emulator-jb-debug_dep',
    {'build_type': 'debug',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'B2G Emulator Image Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'b2g',
                   'os_platform': 'b2g-emu-jb',
                   'vm': False}}),
    ('b2g_mozilla-inbound_linux32_gecko build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'linux',
                   'os_platform': 'b2g-linux32',
                   'vm': False}}),
    ('b2g_mozilla-inbound_linux64_gecko build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'b2g-linux64',
                   'vm': False}}),
    ('b2g_mozilla-inbound_macosx64_gecko build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'b2g-osx',
                   'vm': False}}),
    ('b2g_mozilla-inbound_unagi_dep',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'Unagi Device Image',
               'group_symbol': 'Unagi',
               'name': 'Unagi Device Image Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'b2g',
                   'os_platform': 'b2g-device-image',
                   'vm': False}}),
    ('b2g_mozilla-inbound_win32_gecko build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'win',
                   'os_platform': 'b2g-win32',
                   'vm': False}}),
    ('b2g_ubuntu64_vm mozilla-inbound opt test gaia-ui-test',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Gaia UI Test',
               'job_symbol': 'Gu'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'b2g-linux64',
                   'vm': True}}),
    ('b2g_ubuntu64_vm mozilla-inbound opt test gaia-unit',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Gaia Unit Test',
               'job_symbol': 'G'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'b2g-linux64',
                   'vm': True}}),
    ('b2g_ubuntu64_vm mozilla-inbound opt test mochitest-1',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Mochitest',
               'group_symbol': 'M',
               'name': 'Mochitest',
               'job_symbol': '1'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'b2g-linux64',
                   'vm': True}}),
    ('Linux mozilla-inbound build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'linux',
                   'os_platform': 'linux32',
                   'vm': False}}),
    ('Linux mozilla-inbound leak test build',
    {'build_type': 'debug',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'linux',
                   'os_platform': 'linux32',
                   'vm': False}}),
    ('Linux mozilla-inbound leak test spidermonkey_info-warnaserrdebug build',
    {'build_type': 'debug',
      'job_type': 'build',
      'name': {'group_name': 'SpiderMonkey',
               'group_symbol': 'SM',
               'name': 'SpiderMonkey Fail-On-Warnings Build',
               'job_symbol': 'e'},
      'platform': {'arch': 'x86',
                   'os': 'linux',
                   'os_platform': 'linux32',
                   'vm': False}}),
    ('Linux mozilla-inbound pgo-build',
    {'build_type': 'pgo',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'linux',
                   'os_platform': 'linux32',
                   'vm': False}}),
    ('Linux mozilla-inbound spidermonkey_info-warnaserr build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'SpiderMonkey',
               'group_symbol': 'SM',
               'name': 'SpiderMonkey Fail-On-Warnings Build',
               'job_symbol': 'e'},
      'platform': {'arch': 'x86',
                   'os': 'linux',
                   'os_platform': 'linux32',
                   'vm': False}}),
    ('Linux x86-64 mozilla-inbound asan build',
    {'build_type': 'asan',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'AddressSanitizer Opt Build',
               'job_symbol': 'Bo'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('Linux x86-64 mozilla-inbound build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('Linux x86-64 mozilla-inbound debug asan build',
    {'build_type': 'asan',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'AddressSanitizer Debug Build',
               'job_symbol': 'Bd'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('Linux x86-64 mozilla-inbound debug static analysis build',
    {'build_type': 'debug',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Static Checking Build',
               'job_symbol': 'S'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('Linux x86-64 mozilla-inbound leak test build',
    {'build_type': 'debug',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('Linux x86-64 mozilla-inbound leak test non-unified',
    {'build_type': 'debug',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Non-Unified Build',
               'job_symbol': 'Bn'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('Linux x86-64 mozilla-inbound non-unified',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Non-Unified Build',
               'job_symbol': 'Bn'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('Linux x86-64 mozilla-inbound leak test spidermonkey_tier_1-rootanalysis '
    'build',
    {'build_type': 'debug',
    'job_type': 'build',
    'name': {'group_name': 'SpiderMonkey',
              'group_symbol': 'SM',
              'name': 'SpiderMonkey Root Analysis Build',
              'job_symbol': 'r'},
    'platform': {'arch': 'x86_64',
                  'os': 'linux',
                  'os_platform': 'linux64',
                  'vm': False}}),
    ('Linux x86-64 mozilla-inbound pgo-build',
    {'build_type': 'pgo',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('Linux x86-64 mozilla-inbound spidermonkey_info-warnaserr build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'SpiderMonkey',
               'group_symbol': 'SM',
               'name': 'SpiderMonkey Fail-On-Warnings Build',
               'job_symbol': 'e'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('OS X 10.7 64-bit mozilla-inbound leak test build',
    {'build_type': 'debug',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-8',
                   'vm': False}}),
    ('OS X 10.7 mozilla-inbound build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-8',
                   'vm': False}}),
    ('Rev4 MacOSX Lion 10.7 mozilla-inbound debug test jetpack',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Jetpack SDK Test',
               'job_symbol': 'JP'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-8',
                   'vm': False}}),
    ('Rev4 MacOSX Lion 10.7 mozilla-inbound debug test marionette',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Marionette Framework Unit Tests',
               'job_symbol': 'Mn'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-8',
                   'vm': False}}),
    ('Rev4 MacOSX Lion 10.7 mozilla-inbound debug test reftest',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Reftest',
               'job_symbol': 'R'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-8',
                   'vm': False}}),
    ('Rev4 MacOSX Lion 10.7 mozilla-inbound talos dromaeojs',
    {'build_type': 'opt',
      'job_type': 'talos',
      'name': {'group_name': 'Talos Performance',
               'group_symbol': 'T',
               'name': 'Talos dromaeojs',
               'job_symbol': 'd'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-8',
                   'vm': False}}),
    ('Rev4 MacOSX Snow Leopard 10.6 mozilla-inbound debug test crashtest',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Crashtest',
               'job_symbol': 'C'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-6',
                   'vm': False}}),
    ('Rev5 MacOSX Mountain Lion 10.8 mozilla-inbound debug test crashtest',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Crashtest',
               'job_symbol': 'C'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-8',
                   'vm': False}}),
    ('Ubuntu ASAN VM 12.04 x64 mozilla-inbound opt test crashtest',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Crashtest',
               'job_symbol': 'C'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': True}}),
    ('Ubuntu VM 12.04 x64 mozilla-inbound debug test marionette',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Marionette Framework Unit Tests',
               'job_symbol': 'Mn'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': True}}),
    ('Ubuntu HW 12.04 mozilla-central pgo talos other_nol64',
    {'build_type': 'pgo',
      'job_type': 'talos',
      'name': {'group_name': 'Talos Performance',
               'group_symbol': 'T',
               'name': 'Talos other',
               'job_symbol': 'o'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('Ubuntu HW 12.04 mozilla-central pgo talos g1',
    {'build_type': 'pgo',
      'job_type': 'talos',
      'name': {'group_name': 'Talos Performance',
               'group_symbol': 'T',
               'name': 'Talos g1',
               'job_symbol': 'g1'},
      'platform': {'arch': 'x86',
                   'os': 'linux',
                   'os_platform': 'linux32',
                   'vm': False}}),
    ('Ubuntu HW 12.04 mozilla-inbound pgo talos chromez',
    {'build_type': 'pgo',
      'job_type': 'talos',
      'name': {'group_name': 'Talos Performance',
               'group_symbol': 'T',
               'name': 'Talos chrome',
               'job_symbol': 'c'},
      'platform': {'arch': 'x86',
                   'os': 'linux',
                   'os_platform': 'linux32',
                   'vm': False}}),
    ('Ubuntu HW 12.04 x64 mozilla-inbound pgo talos chromez',
    {'build_type': 'pgo',
      'job_type': 'talos',
      'name': {'group_name': 'Talos Performance',
               'group_symbol': 'T',
               'name': 'Talos chrome',
               'job_symbol': 'c'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('Ubuntu VM 12.04 mozilla-inbound debug test crashtest',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Crashtest',
               'job_symbol': 'C'},
      'platform': {'arch': 'x86',
                   'os': 'linux',
                   'os_platform': 'linux32',
                   'vm': True}}),
    ('Ubuntu VM 12.04 x64 mozilla-inbound debug test crashtest',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Crashtest',
               'job_symbol': 'C'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': True}}),
    ('Windows 7 32-bit mozilla-inbound debug test crashtest',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Crashtest',
               'job_symbol': 'C'},
      'platform': {'arch': 'x86',
                   'os': 'win',
                   'os_platform': 'windows7-32',
                   'vm': False}}),
    ('Windows XP 32-bit mozilla-inbound debug test crashtest',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Crashtest',
               'job_symbol': 'C'},
      'platform': {'arch': 'x86',
                   'os': 'win',
                   'os_platform': 'windowsxp',
                   'vm': False}}),
    ('WINNT 5.2 mozilla-inbound build',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'win',
                   'os_platform': 'windowsxp',
                   'vm': False}}),
    ('WINNT 6.2 mozilla-inbound debug test crashtest',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'Reftest',
               'group_symbol': 'R',
               'name': 'Crashtest',
               'job_symbol': 'C'},
      'platform': {'arch': 'x86',
                   'os': 'win',
                   'os_platform': 'windows8-32',
                   'vm': False}}),

    ('Linux x86-64 b2g-inbound valgrind',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Valgrind Build',
               'job_symbol': 'V'},
      'platform': {'arch': 'x86_64',
                   'os': 'linux',
                   'os_platform': 'linux64',
                   'vm': False}}),
    ('b2g_mozilla-b2g18_leo_eng_nightly',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'Leo Device Image',
               'group_symbol': 'Leo',
               'name': 'Leo Device Image Nightly (Engineering)',
               'job_symbol': 'Ne'},
      'platform': {'arch': 'x86',
                   'os': 'b2g',
                   'os_platform': 'b2g-device-image',
                   'vm': False}}),
    ('b2g_mozilla-b2g26_v1_2_hamachi_nightly',
    {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'Buri/Hamachi Device Image',
               'group_symbol': 'Buri/Hamachi',
               'name': 'Hamachi Device Image Nightly',
               'job_symbol': 'N'},
      'platform': {'arch': 'x86',
                   'os': 'b2g',
                   'os_platform': 'b2g-device-image',
                   'vm': False}}),
    ('jetpack-fx-team-snowleopard-debug',
    {'build_type': 'debug',
      'job_type': 'unittest',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Jetpack SDK Test',
               'job_symbol': 'JP'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-6',
                   'vm': False}}),
    ('jetpack-fx-team-snowleopard-opt',
    {'build_type': 'opt',
      'job_type': 'unittest',
      'name': {'group_name': 'unknown',
               'group_symbol': '?',
               'name': 'Jetpack SDK Test',
               'job_symbol': 'JP'},
      'platform': {'arch': 'x86_64',
                   'os': 'mac',
                   'os_platform': 'osx-10-6',
                   'vm': False}}),
    ('b2g_mozilla-inbound_wasabi_dep',
     {'build_type': 'opt',
      'job_type': 'build',
      'name': {'group_name': 'Wasabi Device Image',
               'group_symbol': 'Wasabi',
               'name': 'Wasabi Device Image Build',
               'job_symbol': 'B'},
      'platform': {'arch': 'x86',
                   'os': 'b2g',
                   'os_platform': 'b2g-device-image',
                   'vm': False}}),
]


@pytest.mark.parametrize(('buildername', 'exp_result'), buildernames)
def test_buildername_translation(buildername, exp_result):
    """
    test getting the right platform based on the buildername
    """

    assert buildbot.extract_platform_info(buildername) == exp_result["platform"]
    assert buildbot.extract_job_type(buildername, default="not found") == exp_result["job_type"]
    assert buildbot.extract_build_type(buildername) == exp_result["build_type"]
    assert buildbot.extract_name_info(buildername) == exp_result["name"]
