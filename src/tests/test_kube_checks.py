import os

from nose.tools import raises
from unittest import TestCase

from compose_flow.kube.checks import BaseChecker, ManifestChecker

from tests.utils import get_content

class TestCheckerNoPrefix(BaseChecker):
    pass


class TestCheckerSingleCheck(BaseChecker):
    check_prefix = '_test_check_'

    def _test_check_noop(self, rendered: str) -> None:
        pass


class TestCheckerAlwaysError(BaseChecker):
    check_prefix = '_test_check_'

    def _test_check_always_return(self, rendered: str) -> str:
        return 'Fail!'


class TestBaseChecker(TestCase):
    @raises(AttributeError)
    def test_no_checks(self):
        """Ensure checker without a check_prefix errors out"""
        checker = TestCheckerNoPrefix()
        checker.check('')

    def test_noop_check(self):
        """Ensure checker with a single dummy checker runs"""
        checker = TestCheckerSingleCheck()
        errors = checker.check('')

        assert len(errors) == 0

    def test_always_error_check(self):
        """Ensure checker with check that returns an error actually returns a list of errors"""
        checker = TestCheckerAlwaysError()
        errors = checker.check('')

        assert len(errors) > 0
        assert 'Fail!' in errors

    def test_invalid_zalando_ingress(self):
        """Ensure ManifestChecker returns an error for invalid Zalando ingress manifest"""
        content = get_content('manifests/invalid-zalando-ingress.yaml')

        checker = ManifestChecker()
        errors = checker.check(content)

        assert len(errors) > 0

    def test_internal_zalando_ingress(self):
        """Ensure ManifestChecker does not return an error for internal Zalando ingress manifest"""
        content = get_content('manifests/internal-zalando-ingress.yaml')

        checker = ManifestChecker()
        errors = checker.check(content)

        assert not errors

    def test_external_zalando_ingress(self):
        """
        Ensure ManifestChecker does not return an error for an explicitly
        internet-facing Zalando ingress manifest
        """
        content = get_content('manifests/external-zalando-ingress.yaml')

        checker = ManifestChecker()
        errors = checker.check(content)

        assert not errors

    def test_nginx_ingress(self):
        """
        Ensure ManifestChecker does not return an error for an NGINX ingress
        """
        content = get_content('manifests/nginx-ingress.yaml')

        checker = ManifestChecker()
        errors = checker.check(content)

        assert not errors

    def test_multidoc_invalid_ingress(self):
        """
        Ensure ManifestChecker returns an error for a multi-document manifest including a single invalid Ingress
        """
        content = get_content('manifests/invalid-ingress-multidoc.yaml')

        checker = ManifestChecker()
        errors = checker.check(content)

        assert len(errors) > 0
