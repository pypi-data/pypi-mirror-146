from typing import List, Set, Union
from pjscan import AnalysisFramework
from cpg2code.symbolic_tracking import SymbolicTracking
import py2neo


class Cpg2CodeFactory(object):
    @staticmethod
    def extract_code(analysis_framework: AnalysisFramework, feeder: Union[List, int, py2neo.Node]):
        """
        This an simple API for extract code from CPG

        :param analysis_framework:
        :param feeder:
        :return:
        """
        if isinstance(feeder,List) and feeder.__len__() == 0:
            raise IndexError("feeder must contain at least one node")
        st = SymbolicTracking(analysis_framework)
        if isinstance(feeder, List) and isinstance(feeder[0], int):
            res = ""
            for node_id in feeder:
                _res = st.extract_code(analysis_framework.get_node_itself(node_id))
                if _res != "":
                    res += _res + "\n"
            return res
        elif isinstance(feeder, List) and isinstance(feeder[0], py2neo.Node):
            res = ""
            for node_id in feeder:
                _res = st.extract_code(analysis_framework.get_node_itself(node_id))
                if _res != "":
                    res += _res + "\n"
            return res
        elif isinstance(feeder, py2neo.Node):
            return st.extract_code(feeder)
        elif isinstance(feeder, int):
            return st.extract_code(analysis_framework.get_node_itself(feeder))


    @staticmethod
    def tracking_code(analysis_framework: SymbolicTracking, feeder: Union[List, int]):
        """
        This is an simple API for tracking code from CPG

        However, not implement yet.

        :param analysis_framework:
        :param feeder:
        :return:
        """
        st = SymbolicTracking(analysis_framework)
