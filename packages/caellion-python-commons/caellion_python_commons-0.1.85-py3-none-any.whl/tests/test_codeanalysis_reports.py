# test framework
import unittest
import pytest

# package
from caellion.pycommons.codeanalysis.reports import ReportBuilder as rpt  # noqa


# test cases
class TestCodeAnalysisReportsReportBuilder:

    maxDiff = None

    # exceptions
    def test_cannot_init_twice(self):
        with pytest.raises(ValueError):
            RB = rpt()
            RB.__init__()

    # empty report
    def test_build_empty_report(self):
        RB = rpt()
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [], "size": 0}'
        )

    # basic report
    def test_build_basic_report(self):
        RB = rpt()
        RB.addIssue("some/file/path.py", "LOW", "test")
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test"}], "size": 1}'
        )

    # basic report
    def test_build_basic_report_invalid_path_fails(self):
        with pytest.raises(Exception):
            RB = rpt()
            RB.addIssue("/some/file/path/", "LOW", "test")
            report = RB.generateReport()  # noqa: F841

    # basic report
    def test_build_basic_report_none_path_fails(self):
        with pytest.raises(Exception):
            RB = rpt()
            RB.addIssue(None, "LOW", "test")
            report = RB.generateReport()  # noqa: F841

    # basic report
    def test_build_basic_report_empty_path_fails(self):
        with pytest.raises(Exception):
            RB = rpt()
            RB.addIssue("", "LOW", "test")
            report = RB.generateReport()  # noqa: F841

    # basic report
    def test_build_basic_report_unknown_severity_fails(self):
        with pytest.raises(Exception):
            RB = rpt()
            RB.addIssue("a.txt", "severityunk", "test")
            report = RB.generateReport()  # noqa: F841

    # basic report
    def test_build_basic_report_none_message_fails(self):
        with pytest.raises(Exception):
            RB = rpt()
            RB.addIssue("a.txt", "LOW", None)
            report = RB.generateReport()  # noqa: F841

    # basic report
    def test_build_basic_report_none_empty_message_fails(self):
        with pytest.raises(Exception):
            RB = rpt()
            RB.addIssue("a.txt", "LOW", "")
            report = RB.generateReport()  # noqa: F841

    # basic report
    def test_build_full_report_lineStart(self):
        RB = rpt()
        RB.addIssue("some/file/path.py", "LOW", "test", lineStart=1)
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1}], "size": 1}'
        )

    # basic report
    def test_build_full_report_lineStartEnd(self):
        RB = rpt()
        RB.addIssue("some/file/path.py", "LOW", "test", lineStart=1, lineEnd=2)
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1, "lineEnd": 2}], "size": 1}'
        )

    # basic report
    def test_build_full_report_lineStartEnd_fails_noStart(self):
        RB = rpt()
        RB.addIssue("some/file/path.py", "LOW", "test", lineEnd=2)
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test"}], "size": 1}'
        )

    # basic report
    def test_build_full_report_lineStartEndcolStart(self):
        RB = rpt()
        RB.addIssue(
            "some/file/path.py", "LOW", "test", lineStart=1, lineEnd=2, columnStart=3
        )
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1, "lineEnd": 2, "columnStart": 3}], "size": 1}'
        )

    # basic report
    def test_build_full_report_lineStartEndcolStartEnd(self):
        RB = rpt()
        RB.addIssue(
            "some/file/path.py",
            "LOW",
            "test",
            lineStart=1,
            lineEnd=2,
            columnStart=3,
            columnEnd=4,
        )
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1, "lineEnd": 2, "columnStart": 3, "columnEnd": 4}], "size": 1}'
        )

    # basic report
    def test_build_full_report_lineStartEndcolStartEnd_fails_noStart(self):
        RB = rpt()
        RB.addIssue(
            "some/file/path.py", "LOW", "test", lineStart=1, lineEnd=2, columnEnd=4
        )
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1, "lineEnd": 2}], "size": 1}'
        )

    # basic report
    def test_build_full_report_lineStartEndcolStartEndCatg(self):
        RB = rpt()
        RB.addIssue(
            "some/file/path.py",
            "LOW",
            "test",
            lineStart=1,
            lineEnd=2,
            columnStart=3,
            columnEnd=4,
            category="category",
        )
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1, "lineEnd": 2, "columnStart": 3, "columnEnd": 4, "category": "category"}], "size": 1}'
        )

    # basic report
    def test_build_full_report_lineStartEndcolStartEndCatgType(self):
        RB = rpt()
        RB.addIssue(
            "some/file/path.py",
            "LOW",
            "test",
            lineStart=1,
            lineEnd=2,
            columnStart=3,
            columnEnd=4,
            category="category",
            type="type",
        )
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1, "lineEnd": 2, "columnStart": 3, "columnEnd": 4, "category": "category", "type": "type"}], "size": 1}'
        )

    # basic report
    def test_build_full_report_lineStartEndcolStartEndCatgTypeDescr(self):
        RB = rpt()
        RB.addIssue(
            "some/file/path.py",
            "LOW",
            "test",
            lineStart=1,
            lineEnd=2,
            columnStart=3,
            columnEnd=4,
            category="category",
            type="type",
            description="description",
        )
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1, "lineEnd": 2, "columnStart": 3, "columnEnd": 4, "category": "category", "type": "type", "description": "description"}], "size": 1}'
        )

    # basic report
    def test_build_full_report_lineStartEndcolStartEndCatgTypeDescrPack(self):
        RB = rpt()
        RB.addIssue(
            "some/file/path.py",
            "LOW",
            "test",
            lineStart=1,
            lineEnd=2,
            columnStart=3,
            columnEnd=4,
            category="category",
            type="type",
            description="description",
            packageName="package",
        )
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1, "lineEnd": 2, "columnStart": 3, "columnEnd": 4, "category": "category", "type": "type", "description": "description", "packageName": "package"}], "size": 1}'
        )

    # basic report
    def test_build_full_report_lineStartEndcolStartEndCatgTypeDescrPackMod(self):
        RB = rpt()
        RB.addIssue(
            "some/file/path.py",
            "LOW",
            "test",
            lineStart=1,
            lineEnd=2,
            columnStart=3,
            columnEnd=4,
            category="category",
            type="type",
            description="description",
            packageName="package",
            moduleName="module",
        )
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1, "lineEnd": 2, "columnStart": 3, "columnEnd": 4, "category": "category", "type": "type", "description": "description", "packageName": "package", "moduleName": "module"}], "size": 1}'
        )

    # basic report
    def test_build_full_report(self):
        RB = rpt()
        RB.addIssue(
            "some/file/path.py",
            "LOW",
            "test",
            lineStart=1,
            lineEnd=2,
            columnStart=3,
            columnEnd=4,
            category="category",
            type="type",
            description="description",
            packageName="package",
            moduleName="module",
            additionalProperties="adds",
        )
        report = RB.generateReport()
        assert (
            report
            == '{"_class": "io.jenkins.plugins.analysis.core.restapi.ReportApi", "issues": [{"fileName": "some/file/path.py", "directory": "some/file/", "severity": "LOW", "message": "test", "lineStart": 1, "lineEnd": 2, "columnStart": 3, "columnEnd": 4, "category": "category", "type": "type", "description": "description", "packageName": "package", "moduleName": "module", "additionalProperties": "adds"}], "size": 1}'
        )


if __name__ == "__main__":
    unittest.main()
