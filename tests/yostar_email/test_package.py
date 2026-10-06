import subprocess
import sys
import textwrap

from majsoulrpa import yostar_email
from majsoulrpa.yostar_email import email, errors, provider


def test_public_exports_preserve_defining_objects() -> None:
    expected = {
        "InvalidYostarVerificationEmailError": (
            errors.InvalidYostarVerificationEmailError
        ),
        "VerificationCodeProvider": provider.VerificationCodeProvider,
        "YostarVerificationEmailError": errors.YostarVerificationEmailError,
        "extract_verification_code": email.extract_verification_code,
    }

    assert set(yostar_email.__all__) == expected.keys()
    for name, value in expected.items():
        assert getattr(yostar_email, name) is value


def test_import_without_aws_dependencies_does_not_load_s3() -> None:
    script = textwrap.dedent("""
        import importlib.abc
        import sys

        class RejectAwsImports(importlib.abc.MetaPathFinder):
            def find_spec(self, fullname, path=None, target=None):
                root = fullname.split(".", 1)[0]
                if root in {"boto3", "botocore", "types_boto3_s3"}:
                    raise AssertionError(f"Unexpected AWS import: {fullname}")

        sys.meta_path.insert(0, RejectAwsImports())

        import majsoulrpa.yostar_email as package

        for name in package.__all__:
            assert getattr(package, name) is not None
        assert "majsoulrpa.yostar_email.s3" not in sys.modules
        assert not any(
            name.split(".", 1)[0] in
            {"boto3", "botocore", "types_boto3_s3"}
            for name in sys.modules
        )
    """)

    result = subprocess.run(  # noqa: S603
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
