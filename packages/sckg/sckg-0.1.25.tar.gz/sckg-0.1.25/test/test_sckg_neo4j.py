"""Tests for `sckg_neo4j` package."""
import unittest

from sckg.sckg_neo4j import SoftwareKGSearcher


class TestSckgNeo4j(unittest.TestCase):
    def test_get_node_num(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_node_num())

    def test_get_relation_num(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_relation_num())

    def test_get_node_info_by_id(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_node_info_by_id(6926))

    def test_get_concept_by_id(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_concept_by_id(6926))

    def test_get_id_by_concept(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_id_by_concept('nodejs'))

    def test_get_node_by_concept(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_node_by_concept('react.js'))
        print(sckg_neo4j.get_node_by_concept('reactjs'))

    def test_is_exist_concept(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.is_exist_concept('is'))

    def test_is_exist_concept_by_id(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.is_exist_concept_by_id(9890000))

    def test_get_concept_score(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_concept_score('cnn'))

    def test_get_concept_pagerankscore(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_concept_pagerankscore('cnn'))

    def test_get_get_concept_labels(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_concept_labels('open'))

    def test_is_action(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.is_action('use'))

    def test_is_concept(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.is_concept('an'))

    def test_is_characteristic(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.is_characteristic('open'))

    def test_get_out_relation_by_concept(self):
        sckg_neo4j = SoftwareKGSearcher()
        re=sckg_neo4j.get_out_relation_by_concept('programming language')
        for i in re:
            print(i)

    def test_get_out_relation_info_by_concept(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_out_relation_info_by_concept('react.js'))

    def test_get_in_relation_info_by_concept(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_in_relation_info_by_concept('node.js'))

    def test_get_in_relation_by_concept(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_in_relation_by_concept('node.js'))

    def test_find_all_concept_from_sentence(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.find_all_concept_from_sentence("Node.js is an event-based, non-blocking, asynchronous I/O runtime that uses Google's V8 JavaScript engine and libuv library"))


    def test_find_longest_concept_from_sentence(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.find_longest_concept_from_sentence("Node.js is an event-based, non-blocking, asynchronous I/O runtime that uses Google's V8 JavaScript engine and libuv library"))

    def test_find_longest_valid_concept_from_sentence(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.find_longest_valid_concept_from_sentence('Is it possible to use private field conventions for Fluent NHibernate Automapping?'))

    def test_get_get_random_node(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_random_node())

    def test_get_random_lastest_node(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_random_lastest_node())

    def test_get_hot_concepts(self):
        sckg_neo4j = SoftwareKGSearcher()
        print(sckg_neo4j.get_hot_concepts())

    def test_cul_in_related_node(self):
        sckg_neo4j = SoftwareKGSearcher()
        nodes = sckg_neo4j.cul_in_related_node('jquery')
        for node in nodes:
            print(node)

    def test_get_upper_concept(self):
        sckg_neo4j = SoftwareKGSearcher()
        nodes = sckg_neo4j.get_upper_concept('jquery')
        for node in nodes:
            print(node)

    def  test_get_common_upper_concept(self):
        sckg_neo4j = SoftwareKGSearcher()
        nodes = sckg_neo4j.get_common_upper_concept('java','javascript')
        for node in nodes:
            print(node)



