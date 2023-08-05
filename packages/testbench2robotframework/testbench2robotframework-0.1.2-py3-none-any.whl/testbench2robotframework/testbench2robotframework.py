from .json_reader import JsonReader
from .testbench2rf import create_test_suites
from .log import logger, setup_logger
from .testsuite_write import write_test_suites
from .utils import get_json_report_directory


def testbench2robotframework(json_report, config):
    json_report_directory = get_json_report_directory(json_report)
    reader = JsonReader(json_report_directory, config)
    setup_logger(reader.config)
    logger.debug(f"Config file '{config}' loaded.")
    test_suites = create_test_suites(
        reader.get_test_case_set_catalog(), reader.test_theme_tree, reader.config
    )
    write_test_suites(test_suites, reader.config)
