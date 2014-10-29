import collections
import mock
import os
import unittest

# FIXME: this is not super elegant
os.environ["ANSIBLE_IN_HAPPY_UNITTEST_LAND"] = "1"
from packaging.apt import (
    expand_pkgspec_from_fnmatches,
)


class AptExpandPkgspecTestCase(unittest.TestCase):

    def setUp(self):
        FakePackage = collections.namedtuple("Package", ("name",))
        self.fake_cache = [ FakePackage("apt"),
                            FakePackage("apt-utils"),
        ]

    def test_trivil(self):
        foo = ["apt"]
        self.assertEqual(
            expand_pkgspec_from_fnmatches(None, foo, self.fake_cache), foo)

    def test_bug_28(self):
        foo = ["apt=1.0*"]
        self.assertEqual(
            expand_pkgspec_from_fnmatches(None, foo, self.fake_cache), foo)

    def test_pkgname_wildcard_version_wildcard_fails(self):
        foo = ["apt*=1.0*"]
        m_mock = mock.Mock()
        expand_pkgspec_from_fnmatches(m_mock, foo, self.fake_cache)
        self.assertTrue(m_mock.fail_json.called)

    def test_pkgname_expands(self):
        foo = ["apt*"]
        m_mock = mock.Mock()
        self.assertEqual(
            expand_pkgspec_from_fnmatches(m_mock, foo, self.fake_cache),
            ["apt", "apt-utils"])
