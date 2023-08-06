import os
import re
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from typing import List

from pyshex.shex_evaluator import evaluate_cli
from pyshex.user_agent import UserAgent
from tests import datadir, SKIP_EXTERNAL_URLS, SKIP_EXTERNAL_URLS_MSG
from tests.test_cli.clitests import CLITestCase, ArgParseExitException
from tests.utils.web_server_utils import DRUGBANK_SPARQL_URL, is_up, is_down_reason

update_test_files: bool = False


class ShexEvaluatorTestCase(CLITestCase):
    testdir = "evaluate"
    testprog = 'shexeval'
    IN_TOX = False

    def prog_ep(self, argv: List[str]) -> bool:
        return bool(evaluate_cli(argv, prog=self.testprog))

    @unittest.skipIf(os.environ.get('IN_TOX', False), "Skipping test_help because of TOX formatting parameters")
    def test_help(self):
        testfile_path = os.path.join(self.testdir_path, 'help')
        with open(testfile_path) as tf:
            help_text = tf.read().format(UserAgent=UserAgent)
        outf = StringIO()
        with redirect_stdout(outf):
            try:
                self.prog_ep(['--help'])
            except ArgParseExitException:
                pass
        self.maxDiff = None
        self.assertEqual(help_text.strip(), re.sub('optional arguments:', 'options:',
                                           (re.sub(';\\n\s*', '; ', outf.getvalue().strip()))))

    def test_obs(self):
        shex = os.path.join(self.test_input_dir, 'obs.shex')
        rdf = os.path.join(self.test_input_dir, 'obs.ttl')
        self.do_test([rdf, shex, '-fn', 'http://ex.org/Obs1'], 'obs1', update_test_file=update_test_files)
        self.assertFalse(update_test_files, "Updating test files")

    def test_biolink(self):
        shex = os.path.join(datadir,'schemas', 'meta.shex')
        rdf = os.path.join(datadir, 'validation', 'biolink-model.ttl')
        self.do_test([rdf, shex, '-fn', 'https://biolink.github.io/biolink-model/ontology/biolink.ttl',
                      '-s', 'http://bioentity.io/vocab/SchemaDefinition', '-cf'], 'biolinkpass',
                     update_test_file=update_test_files)
        self.do_test([rdf, shex, '-fn', 'https://biolink.github.io/biolink-model/ontology/biolink.ttl',
                      '-s', 'http://bioentity.io/vocab/SchemaDefinition'], 'biolinkfail',
                     update_test_file=update_test_files, failexpected=True)
        self.assertFalse(update_test_files, "Updating test files")

    def test_start_type(self):
        """ Test four subjects, two having one RDF type, one having two and one having none """
        shex = os.path.join(datadir, 'schemas', 'biolink-modelnc.shex')
        rdf = os.path.join(datadir, 'validation', 'type-samples.ttl')
        self.do_test([rdf, shex, '-A', '-ut', '-cf'], 'type-samples', update_test_file=update_test_files,
                     failexpected=True)
        self.assertFalse(update_test_files, "Updating test files")

    def test_start_predicate(self):
        """ Test four subjects, two having one RDF type, one having two and one having none """
        shex = os.path.join(datadir, 'schemas', 'biolink-modelnc.shex')
        rdf = os.path.join(datadir, 'validation', 'type-samples.ttl')
        self.do_test([rdf, shex, '-A', '-sp', 'http://w3id.org/biolink/vocab/type', '-cf'], 'pred-samples',
                     update_test_file=update_test_files,
                     failexpected=True)
        self.assertFalse(update_test_files, "Updating test files")

    @unittest.skipIf(not is_up(DRUGBANK_SPARQL_URL), is_down_reason(DRUGBANK_SPARQL_URL))
    def test_sparql_query(self):
        """ Test a sample DrugBank sparql query """
        shex = os.path.join(datadir, 't1.shex')
        sparql = os.path.join(datadir, 't1.sparql')
        self.do_test([DRUGBANK_SPARQL_URL, shex, '-sq', sparql], 't1', update_test_file=update_test_files)


if __name__ == '__main__':
    unittest.main()
