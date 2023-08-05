import argparse
import os
import re
import sys
from pathlib import PurePath
from typing import Dict, Tuple, Optional
from zipfile import ZipFile

from testbench2robotframework.model import (
    TestStructureTreeNode,
    TestStructureTree,
    TestStructureTreeNodeType,
)

CONVERTER_DESCRIPTION = """iTB2Robot converts TestBench JSON report to Robot Framework Code
                        and Robot Result Model to JSON full report."""
JSON_PATH_ARGUMENT_HELP = "Path to a ZIP file or directory containing TestBenchs JSON report files."
CONFIG_ARGUMENT_HELP = """Path to a config json file to generate robot files
                        based on the given configuration.
                        If no path is given testbench2robot will search for a file
                        named \"config.json\" in the current working directory."""


arg_parser = argparse.ArgumentParser(description=CONVERTER_DESCRIPTION)
arg_parser.add_argument(
    "-c",
    "--config",
    help=CONFIG_ARGUMENT_HELP,
    type=str,
    required=False,
    default=os.path.join(os.path.abspath(os.curdir), "config.json"),
)
arg_parser.add_argument(
    '--version',
    '--info',
    action='store_true',
    help='Writes the TestBench2RobotFramework, Robot Framework and Python version to console.',
)
arg_parser.add_argument(
    "jsonReport",
    nargs='?',
    type=str,
    help=JSON_PATH_ARGUMENT_HELP,
)


class PathResolver:
    def __init__(
        self,
        test_theme_tree: TestStructureTree,
        tcs_filter_uids: Tuple[str, ...],
        log_suite_numbers: bool,
    ):
        self.tcs_catalog: Dict[str, TestStructureTreeNode] = {}
        self.tt_catalog: Dict[str, TestStructureTreeNode] = {}
        self.tree_dict: Dict[str, TestStructureTreeNode] = {}
        self._max_numbers_dict: Dict[str, int] = {}
        self._log_suite_numbers = log_suite_numbers
        self._tcs_filter_uids = tcs_filter_uids
        self._analyze_tree(test_theme_tree)
        self.tcs_paths = self._get_paths(self.tcs_catalog)
        self.tt_paths = self._get_paths(self.tt_catalog)

    def _analyze_tree(self, test_theme_tree: TestStructureTree):
        self.tree_dict[test_theme_tree.root.baseInformation.key] = test_theme_tree.root
        for tse in test_theme_tree.nodes:
            self._add_tcs_catalog_based_on_filter_uids(tse)
            self.tree_dict[tse.baseInformation.key] = tse
            self._max_numbers_dict[tse.baseInformation.parentKey] = max(
                int(get_tse_index(tse)),
                self._max_numbers_dict.get(tse.baseInformation.parentKey, 0),
            )

    def _add_tcs_catalog_based_on_filter_uids(self, tse):
        if (
            tse.elementType == TestStructureTreeNodeType.TestCaseSet
            and tse.baseInformation.uniqueID in self._tcs_filter_uids
        ):
            self.tcs_catalog[tse.baseInformation.uniqueID] = tse

    def _get_paths(self, tse_catalog: Dict[str, TestStructureTreeNode]) -> Dict[str, PurePath]:
        return {uid: self._resolve_tse_path(tse) for uid, tse in tse_catalog.items()}

    def _resolve_tse_path(self, tse: TestStructureTreeNode) -> PurePath:
        self._add_tt_to_tt_catalog_if_not_exist(tse)
        if tse.elementType == TestStructureTreeNodeType.Root:
            return PurePath()
        tse_name = replace_invalid_characters(tse.baseInformation.name)
        if tse.baseInformation.parentKey not in self.tree_dict:
            return PurePath(f"{self._file_prefix(tse)}{tse_name}")
        parent_path = self._resolve_tse_path(self.tree_dict[tse.baseInformation.parentKey])
        return parent_path / f"{self._file_prefix(tse)}{tse_name}"

    def _add_tt_to_tt_catalog_if_not_exist(self, tse):
        if (
            tse.elementType == TestStructureTreeNodeType.TestTheme
            and tse.baseInformation.uniqueID not in self.tt_catalog
        ):
            self.tt_catalog[tse.baseInformation.uniqueID] = tse

    def _file_prefix(self, tse) -> str:
        prefix_separator = '_' * self._log_suite_numbers
        return f"{self._get_padded_index(tse)}_{prefix_separator}"

    def _get_padded_index(self, tse) -> str:
        index = get_tse_index(tse)
        max_length = len(str(self._max_numbers_dict[tse.baseInformation.parentKey]))
        return index.zfill(max_length)


def get_json_report_directory(json_report_path: Optional[str]) -> str:
    if json_report_path is None:
        return ""
    if not os.path.exists(json_report_path):
        sys.exit("Error opening " + json_report_path + ". Path does not exist.")
    if os.path.isdir(json_report_path):
        return os.path.abspath(json_report_path)
    if os.path.splitext(json_report_path)[1].lower() == ".zip":
        with ZipFile(json_report_path, 'r') as zip_ref:
            zip_ref.extractall("json_report")
        return os.path.abspath("json_report")
    sys.exit("Error opening " + json_report_path + ". File is not a ZIP file.")


def replace_invalid_characters(name: str) -> str:
    return re.sub(r'[<>:"/\\|?* ]', "_", name)


def get_tse_index(tse: TestStructureTreeNode) -> str:
    return tse.baseInformation.numbering.rsplit(".", 1)[-1]
