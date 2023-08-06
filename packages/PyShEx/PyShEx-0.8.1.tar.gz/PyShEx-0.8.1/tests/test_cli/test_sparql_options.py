import os
import re
import unittest
from typing import List

from pyshex.shex_evaluator import evaluate_cli
from tests import datadir, SKIP_EXTERNAL_URLS, SKIP_EXTERNAL_URLS_MSG
from tests.test_cli.clitests import CLITestCase
from tests.utils.web_server_utils import FHIRCAT_GRAPHDB_URL, is_up, is_down_reason, DRUGBANK_SPARQL_URL, \
    DUMONTIER_GRAPHDB_URL


def elapsed_filter(txt: str) -> str:
    return re.sub(r'\(\d+(\.\d+)? ([a-zA-Z]*)\)', '(n.nn \\2)', txt)


@unittest.skipIf(SKIP_EXTERNAL_URLS, SKIP_EXTERNAL_URLS_MSG)
class SparqlQueryTestCase(CLITestCase):
    testdir = "evaluate"
    testprog = 'shexeval'
    schemadir = os.path.join(datadir, 'schemas')

    def prog_ep(self, argv: List[str]) -> bool:
        return bool(evaluate_cli(argv, prog=self.testprog))

    @unittest.skipIf(not is_up(DRUGBANK_SPARQL_URL), is_down_reason(DRUGBANK_SPARQL_URL))
    def test_sparql_query(self):
        """ Test a sample DrugBank sparql query """
        shex = os.path.join(datadir, 't1.shex')
        sparql = os.path.join(datadir, 't1.sparql')
        self.do_test([DRUGBANK_SPARQL_URL, shex, '-sq', sparql], 'dbsparql1')

    @unittest.skipIf(not is_up(DRUGBANK_SPARQL_URL), is_down_reason(DRUGBANK_SPARQL_URL))
    def test_print_queries(self):
        """ Test a sample DrugBank sparql query printing queries"""
        shex = os.path.join(datadir, 't1.shex')
        sparql = os.path.join(datadir, 't1.sparql')
        self.do_test([DRUGBANK_SPARQL_URL, shex, '-sq', sparql, '-ps'], 'dbsparql2', text_filter=elapsed_filter)

    @unittest.skipIf(not is_up(DRUGBANK_SPARQL_URL), is_down_reason(DRUGBANK_SPARQL_URL))
    def test_print_results(self):
        """ Test a sample DrugBank sparql query printing results"""
        shex = os.path.join(datadir, 't1.shex')
        sparql = os.path.join(datadir, 't1.sparql')
        self.do_test([DRUGBANK_SPARQL_URL, shex, '-sq', sparql, '-pr', "--stopafter", "1"], 'dbsparql3', text_filter=elapsed_filter)

    @unittest.skipIf(not is_up(DRUGBANK_SPARQL_URL), is_down_reason(DRUGBANK_SPARQL_URL))
    def test_named_graph(self):
        """ Test a sample DrugBank using any named graph """

        shex = os.path.join(datadir, 't1.shex')
        sparql = os.path.join(datadir, 't1.sparql')
        self.maxDiff = None
        self.do_test([DRUGBANK_SPARQL_URL, shex, '-sq', sparql, '-ps', '-gn', "", "-pr"], 'dbsparql4',
                     failexpected=True, text_filter=elapsed_filter)

        graphid = "<http://identifiers.org/drugbank:>"
        self.do_test([DRUGBANK_SPARQL_URL, shex, '-sq', sparql, '-ps', '-gn', graphid, "-pr"], 'dbsparql5',
                     failexpected=True, text_filter=elapsed_filter)

    @unittest.skipIf(not is_up(DUMONTIER_GRAPHDB_URL), is_down_reason(DUMONTIER_GRAPHDB_URL))
    def test_named_graph_types(self):
        """ Test a Drugbank query with named graph in the query """
        shex = os.path.join(datadir, 'schemas', 'biolink-modelnc.shex')
        self.maxDiff = None
        self.do_test([DUMONTIER_GRAPHDB_URL, shex, '-ss', '-gn', '', '-ps', '-pr', '-ut', '-sq',
                      'select ?item where{?item a <http://w3id.org/biolink/vocab/Protein>} LIMIT 20'],
                     'dbsparql6', failexpected=True, text_filter=elapsed_filter)

    @unittest.skipIf(not is_up(FHIRCAT_GRAPHDB_URL), is_down_reason(FHIRCAT_GRAPHDB_URL))
    def test_infer_setting(self):
        """ Test setting infer to False """

        shex = os.path.join(datadir, 'patient.shex')
        rdf = 'https://graph.fhircat.org/repositories/fhirontology?infer=false'
        self.maxDiff = None
        self.do_test([rdf, shex, '-fn', "http://hl7.org/fhir/Patient/pat4", '-ssg', '-pb', '-ps', '-pr'], 'dbsparql7',
                     text_filter=elapsed_filter)


if __name__ == '__main__':
    unittest.main()
