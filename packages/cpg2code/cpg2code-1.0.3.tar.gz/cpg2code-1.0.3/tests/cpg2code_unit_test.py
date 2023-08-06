import logging
import unittest
import networkx as nx
from pjscan import AnalysisFramework
from pjscan.graph_traversal import ControlGraphForwardTraversal
from pjscan.const import *
from cpg2code.cpg2code_factory import Cpg2CodeFactory


class Cpg2CodeUnitTest(unittest.TestCase):
    def test_code_extract(self):
        """
        :return:
        """
        NEO4J_DEFAULT_CONFIG = {
            "NEO4J_HOST": "shaobaobaoer_ubuntu20",
            "NEO4J_USERNAME": "neo4j",
            "NEO4J_PASSWORD": "123",
            "NEO4J_PORT": "7474",
            "NEO4J_PROTOCOL": "http",
            "NEO4J_DATABASE": "neo4j",
        }
        # instance of wordpress
        # /home/lth/EnhancedPHPJoernMaster/large_scale_test/WordPress-5.7.1/wp-load.php
        analysis_framework = AnalysisFramework.from_dict(NEO4J_DEFAULT_CONFIG)
        traversal_entity = ControlGraphForwardTraversal(analysis_framework)
        # large_scale_test/MISP-2.4.142/app/webroot/index.php
        file = analysis_framework.fig_step.get_file_name_node('user_list_backend.php')
        origin = analysis_framework.basic_step.match_first(
            "AST", **{NODE_FILEID: file[NODE_FILEID], NODE_LINENO: 212}
        )
        origin = analysis_framework.ast_step.get_root_node(origin)
        print(f"{analysis_framework.fig_step.get_belong_file(origin)} :: L{origin[NODE_LINENO]}")
        traversal_entity.origin = [origin]
        traversal_entity.run()
        rec = traversal_entity.get_record()  # type:nx.DiGraph
        rec_list = [k for k, p in rec.nodes.items()]
        result = Cpg2CodeFactory.extract_code(analysis_framework, sorted(rec_list))
        print(result)


if __name__ == '__main__':
    unittest.main()
