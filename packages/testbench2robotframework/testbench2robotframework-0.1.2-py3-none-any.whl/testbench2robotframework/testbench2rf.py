from __future__ import annotations
from dataclasses import dataclass
from pathlib import PurePath, Path
from typing import Dict, List, Set, Optional
import os
import re

from robot.parsing.lexer.tokens import Token
from robot.parsing.model.blocks import SettingSection, TestCase, TestCaseSection, File
from robot.parsing.model.statements import (
    EmptyLine,
    KeywordCall,
    LibraryImport,
    ResourceImport,
    VariablesImport,
    Metadata,
    SectionHeader,
    TestCaseName,
    Comment,
    Statement,
    ForceTags,
    Tags,
)

from .config import Configuration
from .json_reader import TestCaseSet
from .log import logger
from .model import (
    InteractionDetails,
    TestCaseDetails,
    TestStructureTree,
    InteractionType,
    ParameterUseType,
    TestStructureTreeNode,
    UserDefinedField,
    UdfType,
)
from .utils import PathResolver


SEPERATOR = "    "


@dataclass
class InteractionCall:
    name: str


@dataclass
class AtomicInteractionCall(InteractionCall):
    cbv_parameters: Dict[str, str]
    cbr_parameters: Dict[str, str]
    indent: int
    import_prefix: str


@dataclass
class CompoundInteractionCall(InteractionCall):
    cbv_parameters: Dict[str, str]
    cbr_parameters: Dict[str, str]
    indent: int


class RfTestCase:
    def __init__(self, test_case_details: TestCaseDetails, config: Configuration) -> None:
        self.uid: str = test_case_details.uniqueID
        self.interaction_calls: List[InteractionCall] = []
        self.used_imports: Dict[str, Set[str]] = {}
        self.config = config
        for interaction in test_case_details.interactions:
            self._get_interaction_calls(interaction)
        self.rf_tags = [
            keyword.name for keyword in test_case_details.spec.keywords
        ] + self._get_udf_tags(test_case_details.spec.udfs)

        # TODO description

    @staticmethod
    def _get_udf_tags(user_defined_fields: List[UserDefinedField]) -> List[str]:
        udfs = []
        for udf in user_defined_fields:
            if udf.valueType == UdfType.Enumeration:
                udfs.append(f"{udf.name}:{udf.value}")
            elif udf.valueType == UdfType.String and udf.value:
                udfs.append(f"{udf.name}:{udf.value}")
            elif udf.valueType == UdfType.Boolean and udf.value == "true":
                udfs.append(udf.name)
        return udfs

    def _get_interaction_calls(self, interaction: InteractionDetails, indent: int = 0) -> None:
        indent += 1
        if interaction.interactionType != InteractionType.Textuell:
            cbv_params = self._get_params_by_use_type(interaction, ParameterUseType.CallByValue)
            cbr_params = self._get_params_by_use_type(
                interaction,
                ParameterUseType.CallByReference,
                ParameterUseType.CallByReferenceMandatory,
            )
            if interaction.interactionType == InteractionType.Compound:
                self._append_compound_ia_and_analyze_childs(
                    cbr_params, cbv_params, indent, interaction
                )
            elif interaction.interactionType == InteractionType.Atomic:
                self._append_atomic_ia(cbr_params, cbv_params, indent, interaction)

    def _append_atomic_ia(
        self,
        cbr_params: Dict[str, str],
        cbv_params: Dict[str, str],
        indent: int,
        interaction: InteractionDetails,
    ):
        ia_path_parts = interaction.path.split(".")
        if len(ia_path_parts) == 1:
            root_subdivion = "UNKNOWN"
            import_prefix = ia_path_parts[0]
        else:
            root_subdivion, import_prefix = ia_path_parts[:2]
        if root_subdivion not in self.used_imports:
            self.used_imports[root_subdivion] = {import_prefix}
        else:
            self.used_imports[root_subdivion].add(import_prefix)
        self.interaction_calls.append(
            AtomicInteractionCall(
                name=interaction.name,
                cbv_parameters=cbv_params,
                cbr_parameters=cbr_params,
                indent=indent,
                import_prefix=import_prefix,
            )
        )

    def _append_compound_ia_and_analyze_childs(
        self,
        cbr_params: Dict[str, str],
        cbv_params: Dict[str, str],
        indent: int,
        interaction_detail: InteractionDetails,
    ):
        self.interaction_calls.append(
            CompoundInteractionCall(
                interaction_detail.name,
                cbv_parameters=cbv_params,
                cbr_parameters=cbr_params,
                indent=indent,
            )
        )
        for interaction in interaction_detail.interactions:
            self._get_interaction_calls(interaction, indent)

    def _create_rf_keywords(
        self, interaction_calls: List[InteractionCall]
    ) -> List[List[Statement]]:
        keyword_lists: List[List[Statement]] = [[]]
        tc_index = 0
        for interaction_call in interaction_calls:
            if isinstance(interaction_call, AtomicInteractionCall):
                if self.is_splitting_ia(interaction_call, keyword_lists, tc_index):
                    tc_index += 1
                    keyword_lists.append([])
                keyword_lists[tc_index].append(self._create_rf_keyword(interaction_call))
            elif (
                isinstance(interaction_call, CompoundInteractionCall)
                and self.config.logCompoundInteractions
            ):
                keyword_lists[tc_index].append(self._create_rf_compound_keyword(interaction_call))
        return keyword_lists

    def is_splitting_ia(self, interaction_call, keyword_lists, tc_index):
        return (
            re.match(
                self.config.testCaseSplitPathRegEx,
                f"{interaction_call.import_prefix}.{interaction_call.name}",
            )
            and keyword_lists[tc_index]
        )

    def to_robot_ast_test_cases(self) -> List[TestCase]:
        rf_keyword_lists = self._create_rf_keywords(self.interaction_calls)
        rf_test_cases: List[TestCase] = []
        multiple_tests = len(rf_keyword_lists) > 1
        for index, rf_keywords in enumerate(rf_keyword_lists):
            suffix = f' : Phase {index + 1}/{len(rf_keyword_lists)}' if multiple_tests else ''
            tc_name = f"{self.uid}{suffix}"  # TODO later UID or Comments
            rf_test_case = TestCase(header=TestCaseName.from_params(tc_name))
            rf_test_case.body.append(Tags.from_params(self.rf_tags))
            rf_test_case.body.extend(rf_keywords)
            rf_test_case.body.extend([EmptyLine.from_params()])
            rf_test_cases.append(rf_test_case)
        return rf_test_cases

    def _create_cbv_parameters(self, interaction: AtomicInteractionCall) -> List[str]:
        parameters = []
        for name, value in interaction.cbv_parameters.items():
            if name.endswith('='):
                parameters.append(f"{name}{value}")
            else:
                parameters.append(value)
        return parameters

    def _create_rf_keyword(self, interaction: AtomicInteractionCall) -> KeywordCall:
        import_prefix = self.config.fullyQualified * f"{interaction.import_prefix}."
        interaction_indent = (
            SEPERATOR * interaction.indent if self.config.logCompoundInteractions else SEPERATOR
        )
        cbv_parameters = self._create_cbv_parameters(interaction)
        return KeywordCall.from_params(
            assign=tuple(interaction.cbr_parameters.values()),
            name=f"{import_prefix}{interaction.name}",
            args=tuple(
                cbv_parameters
            ),  
            indent=interaction_indent,
        )

    def _create_rf_compound_keyword(self, interaction: CompoundInteractionCall) -> Comment:
        interaction_indent = " " * (interaction.indent * 4)
        return Comment.from_params(
            comment=self._generate_compound_interaction_comment(interaction),
            indent=interaction_indent,
        )  # TODO  prio later key=value als named erlauben config?

    @staticmethod
    def _generate_compound_interaction_comment(interaction: CompoundInteractionCall) -> str:
        cbr_params = SEPERATOR.join(
            [
                f"{param_name}={param_value}"
                for param_name, param_value in interaction.cbr_parameters.items()
            ]
        )
        cbv_params = SEPERATOR.join(
            [
                f"{param_name}={param_value}"
                for param_name, param_value in interaction.cbv_parameters.items()
            ]
        )
        if cbr_params:
            return f"#{SEPERATOR.join([cbr_params, interaction.name, cbv_params])}"
        return f"#{SEPERATOR.join([interaction.name, cbv_params])}"

    @staticmethod
    def _get_params_by_use_type(
        interaction: InteractionDetails, *param_use_types: ParameterUseType
    ) -> Dict[str, str]:
        return {
            parameter.name: parameter.value
            for parameter in interaction.parameters
            if parameter.parameterUseType in param_use_types
        }


def create_test_suites(
    test_case_set_catalog: Dict[str, TestCaseSet],
    test_theme_tree: TestStructureTree,
    config: Configuration,
) -> Dict[str, File]:
    path_resolver = PathResolver(
        test_theme_tree, tuple(test_case_set_catalog.keys()), config.logSuiteNumbering
    )
    tcs_paths = path_resolver.tcs_paths
    test_suites = {}
    for uid, test_case_set in test_case_set_catalog.items():
        test_suites[uid] = RobotSuiteFileBuilder(
            test_case_set, tcs_paths[uid], config
        ).create_test_suite_file()
    tt_paths = path_resolver.tt_paths
    for uid, test_theme in path_resolver.tt_catalog.items():
        test_suites[uid] = RobotInitFileBuilder(
            test_theme, tt_paths[uid], config
        ).create_init_file()
    return test_suites


class RobotInitFileBuilder:
    def __init__(
        self, test_theme: TestStructureTreeNode, tt_path: PurePath, config: Configuration
    ) -> None:
        self.test_theme = test_theme
        self.tt_path = tt_path
        self.config = config

    def create_init_file(self) -> File:
        sections = [self._create_setting_section()]
        return File(sections, source=os.path.join(str(self.tt_path), "__init__"))

    def _create_setting_section(self) -> SettingSection:
        setting_section_meta_data = self._get_setting_section_metadata()
        setting_section = SettingSection(header=SectionHeader.from_params(Token.SETTING_HEADER))
        setting_section.body.extend(
            [
                Metadata.from_params(metadata_name, metadata_value)
                for metadata_name, metadata_value in setting_section_meta_data.items()
            ]
        )
        return setting_section

    def _get_setting_section_metadata(self) -> Dict[str, str]:
        meta_data = {
            "uniqueID": self.test_theme.baseInformation.uniqueID,
            "numbering": self.test_theme.baseInformation.numbering,
        }
        if self.test_theme.specification:
            meta_data["specification status"] = self.test_theme.specification.status
        return meta_data


class RobotSuiteFileBuilder:
    def __init__(
        self, test_case_set: TestCaseSet, tcs_path: PurePath, config: Configuration
    ) -> None:
        self.test_case_set = test_case_set
        self.tcs_path = tcs_path
        self.config = config
        self._rf_test_cases: List[RfTestCase] = [
            RfTestCase(test_case_details=test_case, config=config)
            for test_case in self.test_case_set.test_cases.values()
        ]

    def create_test_suite_file(self) -> File:
        sections = [self._create_setting_section(), self._create_test_case_section()]
        return File(sections, source=str(self.tcs_path))

    def _create_test_case_section(self) -> TestCaseSection:
        test_case_section = TestCaseSection(header=SectionHeader.from_params(Token.TESTCASE_HEADER))
        robot_ast_test_cases = []
        for test_case in self._rf_test_cases:
            robot_ast_test_cases.extend(test_case.to_robot_ast_test_cases())
        test_case_section.body.extend(robot_ast_test_cases)
        test_case_section.body.extend([EmptyLine.from_params(), EmptyLine.from_params()])
        return test_case_section

    def _get_used_subdivisions(self) -> Dict[str, Set[str]]:
        import_dict: Dict[str, Set[str]] = {}
        for test_case in self._rf_test_cases:
            for root, import_name in test_case.used_imports.items():
                if root not in import_dict:
                    import_dict[root] = {*import_name}
                else:
                    import_dict[root].update(import_name)
        return import_dict

    def _create_rf_variable_imports(self) -> List[VariablesImport]:
        return [
            VariablesImport.from_params(name=variable_file)
            for variable_file in self.config.forcedImport.variables
        ]

    def _create_rf_resource_imports(self, import_dict: Dict[str, Set[str]]) -> List[ResourceImport]:
        resource_imports: Set[str] = set()
        for resource_root in self.config.rfResourceRoots:
            resource_imports.update(import_dict.pop(resource_root, []))
        resource_imports.update(self.config.forcedImport.resources)
        resource_files = {
            self._create_resource_import(resource_import)
            for resource_import in sorted(resource_imports)
        }  # TODO Fix Paths to correct models
        return [ResourceImport.from_params(res) for res in sorted(resource_files)]

    def _create_resource_import(self, resource_import: str) -> str:
        if not self.config.resourceDirectory:
            return f"{resource_import}.resource"
        resource_dir = self._get_resource_directory()
        resource_mapping = self.config.subdivisionsMapping.resources.get(resource_import)
        if resource_mapping:
            return f"{'../' * (len(self.tcs_path.parts))}{resource_dir}/{resource_mapping}"
        return f"{'../' * (len(self.tcs_path.parts))}{resource_dir}/{resource_import}.resource"

    def _get_resource_directory(self) -> str:
        root_path = Path(os.curdir).absolute()
        return os.path.relpath(
            re.sub(
                r"^{root}",
                str(root_path).replace('\\', '\\\\'),
                self.config.resourceDirectory,
                flags=re.IGNORECASE,
            ),
            root_path,
        ).replace('\\', '/')

    def _create_rf_library_imports(self, import_dict: Dict[str, Set[str]]) -> List[LibraryImport]:
        lib_imports = set()
        for lib_root in self.config.rfLibraryRoots:
            lib_imports.update(import_dict.pop(lib_root, set()))
        lib_imports.update(self.config.forcedImport.libraries)
        libraries = {
            self.config.subdivisionsMapping.libraries.get(lib_import, lib_import)
            for lib_import in lib_imports
        }
        return [LibraryImport.from_params(lib) for lib in sorted(libraries)]

    def _create_rf_force_tags(self) -> Optional[ForceTags]:
        tb_keyword_names = [keyword.name for keyword in self.test_case_set.details.spec.keywords]
        udfs = []
        for udf in self.test_case_set.details.spec.udfs:
            if udf.valueType == UdfType.Enumeration:
                udfs.append(f"{udf.name}:{udf.value}")
            elif udf.valueType == UdfType.String and udf.value:
                udfs.append(f"{udf.name}:{udf.value}")
            elif udf.valueType == UdfType.Boolean and udf.value == "true":
                udfs.append(udf.name)
        force_tags = tb_keyword_names + udfs
        if force_tags:
            return ForceTags.from_params(force_tags)
        return None

    def _create_rf_unknown_imports(self, import_dict: Dict[str, Set[str]]) -> List[Comment]:
        unknown_imports = set()
        for root, subdivision_names in import_dict.items():
            unknown_imports.update(subdivision_names)
            logger.debug(
                f"{self.test_case_set.details.uniqueID} has imports {list(subdivision_names)} "
                f"from unknown root subdivision '{root}'!"
            )
        if unknown_imports:
            logger.warning(
                f"{self.test_case_set.details.uniqueID} has unknown imports. "
                f"See Log for more details."
            )
        return [
            Comment.from_params(comment=f"# UNKNOWN    {unknown}", indent="")
            for unknown in unknown_imports
        ]

    def _create_setting_section(self) -> SettingSection:
        subdivisions = self._get_used_subdivisions()

        setting_section_meta_data = self._get_setting_section_metadata()
        setting_section = SettingSection(header=SectionHeader.from_params(Token.SETTING_HEADER))
        setting_section.body.extend(self._create_rf_variable_imports())
        setting_section.body.extend(self._create_rf_library_imports(subdivisions))
        setting_section.body.extend(self._create_rf_resource_imports(subdivisions))
        setting_section.body.extend(self._create_rf_unknown_imports(subdivisions))
        setting_section.body.extend(
            [
                Metadata.from_params(metadata_name, metadata_value)
                for metadata_name, metadata_value in setting_section_meta_data.items()
            ]
        )
        setting_section.body.append(self._create_rf_force_tags())
        setting_section.body.extend([EmptyLine.from_params(), EmptyLine.from_params()])
        return setting_section

    def _get_setting_section_metadata(self) -> Dict[str, str]:
        return {
            "uniqueID": self.test_case_set.details.uniqueID,
            "name": self.test_case_set.details.name,
            "numbering": self.test_case_set.details.numbering,
        }
