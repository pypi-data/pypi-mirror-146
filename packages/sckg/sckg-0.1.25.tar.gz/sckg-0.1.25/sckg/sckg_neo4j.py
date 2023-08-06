"""
-----------------------------------------
@Author: xhj
@Email: 20212010075@fudan.edu.cn
@Created: 2022/4/13
------------------------------------------
@Modify: 2022/4/13
------------------------------------------
@Description:
"""
import math
import string
from pathlib import Path
import random

from definitions import DATA_DIR
from sckg.constant_util import ConstantUtil
from neo4j import GraphDatabase


class SoftwareKGSearcher:
    def __init__(self):
        self.constant = ConstantUtil()
        self.re_weight = {}
        with open(Path(DATA_DIR) / 'new_relation_weigth_10', 'r', encoding='utf-8') as f:
            for line in f:
                data_line = line.split(':')
                self.re_weight[data_line[0]] = data_line[1]
        self.driver = GraphDatabase.driver("neo4j://47.116.194.87:9204", auth=("neo4j", "fdsefdse"))
        self.session = self.driver.session()
        self.concepts_list = self.get_all_concept()

    def __del__(self):
        self.session.close()
        self.driver.close()

    def execute(self, query):
        return self.session.read_transaction(lambda tx: list(tx.run(query)))

    def get_all_concept(self):
        query = f'MATCH (n:concept) RETURN n'
        records = self.execute(query)
        results = []
        for record in records:
            properties = {}
            for re in record['n']:
                if re == 'id':
                    continue
                properties[re] = record['n'][re]
            result = {
                "id": record['n']['id'],
                'pagerank': record['n']['pagerank_score'],
                "properties": properties,
                "labels": record['n'].labels
            }
            results.append(result)
        return results

    def get_node_num(self):
        query = f'MATCH (n) RETURN count(*) as c'
        records = self.execute(query)
        return records[0]['c']

    def get_relation_num(self):
        query = f'MATCH P=()-->() RETURN COUNT(*)  AS c'
        records = self.execute(query)
        return records[0]['c']

    def get_node_info_by_id(self, node_id):
        query = f'MATCH (entity:concept{{id:{node_id}}}) RETURN entity'
        records = self.execute(query)
        if not records:
            return []
        record = records[0]['entity']
        properties = {}
        for re in record:
            if re == 'id':
                continue
            properties[re] = record[re]
        result = {
            "id": record['id'],
            "properties": properties,
            "labels": record.labels
        }
        return result

    def get_concept_by_id(self, node_id):
        query = f'MATCH (entity:concept{{id:{node_id}}}) RETURN entity'
        records = self.execute(query)
        if not records:
            return []
        concept = records[0]['entity']['concept_name']
        return concept

    def get_node_by_concept(self, concept):
        query = f'MATCH (entity:concept{{concept_name:{repr(concept)}}}) RETURN entity'
        records = self.execute(query)
        if not records:
            return []
        record = records[0]['entity']
        properties = {}
        for re in record:
            if re == 'id':
                continue
            properties[re] = record[re]
        result = {
            "id": record['id'],
            "properties": properties,
            "labels": record.labels
        }
        return result

    def get_id_by_concept(self, concept):
        query = f'MATCH (entity:concept{{concept_name:{repr(concept)}}}) RETURN entity'
        records = self.execute(query)
        if not records:
            return []
        id = records[0]['entity']['id']
        return id

    def is_exist_concept(self, concept):
        query = f'MATCH (entity:concept{{concept_name:{repr(concept)}}}) RETURN entity'
        records = self.execute(query)
        if records:
            return True
        return False

    def new_is_exist_concept(self, word):
        for concept in self.concepts_list:
            if concept['properties']['concept_name'] == word:
                return True
        return False

    def is_exist_concept_by_id(self, concept_id):
        query = f'MATCH (entity:concept{{id:{concept_id}}}) RETURN entity'
        records = self.execute(query)
        if records:
            return True
        return False

    def get_concept_score(self, concept):
        query = f'MATCH (entity:concept{{concept_name:{repr(concept)}}}) RETURN entity'
        records = self.execute(query)
        if not records:
            return []
        if 'score' in records[0]['entity']:
            return records[0]['entity']['score']
        return ''

    def get_concept_pagerankscore(self, concept):
        query = f'MATCH (entity:concept{{concept_name:{repr(concept)}}}) RETURN entity'
        records = self.execute(query)
        if not records:
            return []
        return records[0]['entity']['pagerank_score']

    def get_concept_labels(self, concept):
        query = f'MATCH (entity:concept{{concept_name:{repr(concept)}}}) RETURN entity'
        records = self.execute(query)
        if not records:
            return []
        return list(records[0]['entity'].labels)

    def is_action(self, word):
        labels = self.get_concept_labels(word)
        if 'action' in labels:
            return True
        return False

    def is_characteristic(self, word):
        labels = self.get_concept_labels(word)
        if 'characteristic' in labels:
            return True
        return False

    def new_is_concept(self, word):
        for concept in self.concepts_list:
            if concept['properties']['concept_name'] == word:
                if 'action' in concept['labels'] or 'characteristic' in concept['labels']:
                    return False
                return True
        return False

    def is_concept(self, word):
        labels = self.get_concept_labels(word)
        if not labels:
            return False
        if 'characteristic' in labels or 'action' in labels:
            return False
        return True

    def get_out_relation_by_concept(self, concept):
        query = f'MATCH (head:entity{{concept_name:{repr(concept)}}})-[CLAIM]->(tail) RETURN head,CLAIM, tail'
        records = self.execute(query)
        # print(records)
        result = []
        # print(records[0]['head'])
        for re in records:
            result.append((re['head']['concept_name'], re['CLAIM'].type, re['tail']['concept_name']))
            # print(re['head']['id'])
            # print(re['CLAIM'].type)
            # print(re['tail']['concept_name'])
            # print('======')
        return result

    def get_out_relation_info_by_concept(self, concept):
        # 会返回结点的完整信息
        query = f'MATCH (head:entity{{concept_name:{repr(concept)}}})-[CLAIM]->(tail) RETURN head,CLAIM, tail'
        records = self.execute(query)
        result = []
        for re in records:
            tail = re['tail']
            properties = {}
            for property in tail:
                if re == 'id':
                    continue
                properties[property] = tail[property]
            tail_info = {
                "id": tail['id'],
                "properties": properties,
                "labels": tail.labels
            }
            result.append((re['head']['concept_name'], re['CLAIM'].type, tail_info))
        return result

    def get_in_relation_by_concept(self, concept):
        query = f'MATCH (head)-[CLAIM]->(tail:entity{{concept_name:{repr(concept)}}}) RETURN head,CLAIM, tail'
        records = self.execute(query)
        result = []
        for re in records:
            result.append((re['head']['concept_name'], re['CLAIM'].type, re['tail']['concept_name']))
        return result

    def get_in_relation_info_by_concept(self, concept):
        # 会返回结点的完整信息
        query = f'MATCH (head)-[CLAIM]->(tail:entity{{concept_name:{repr(concept)}}}) RETURN head,CLAIM, tail'
        records = self.execute(query)
        # print(records)
        result = []
        # properties = {}
        # head=records[0]['head']
        # for re in head:
        #     if re == 'id':
        #         continue
        #     properties[re] = head[re]
        # head_info = {
        #     "id":head['id'],
        #     "properties": properties,
        #     "labels": head.labels
        # }
        # print(records[0]['head'])
        for re in records:
            head = re['head']
            properties = {}
            for property in head:
                if re == 'id':
                    continue
                properties[property] = head[property]
            head_info = {
                "id": head['id'],
                "properties": properties,
                "labels": head.labels
            }
            result.append((head_info, re['CLAIM'].type, re['tail']['concept_name']))
        return result

    def find_all_concept_from_sentence(self, sentence):
        # 给一段文本，返回在KG里面出现的概念
        concepts = []
        sentence = sentence.lower()
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        words = sentence.strip("\n").lower().split()
        for i, word in enumerate(words):
            concept = word
            if i == len(words) - 1:
                break
            for j in range(i + 1, i + 5):
                if j < len(words):
                    concept = concept + " " + words[j]
                if self.new_is_exist_concept(concept):
                    concepts.append(concept)
        for word in words:
            if not self.new_is_concept(word):
                continue
            concepts.append(word)
        concepts = set(concepts)
        return concepts

    def is_exit_concept_in_sentence(self, concept, sentence):
        concepts = self.find_all_concept_from_sentence(sentence)
        if concept in concepts:
            return True
        return False

    def find_longest_valid_concept_from_sentence(self, sentence):
        # 给一段文本，返回在KG里面出现的有效最长概念
        concepts = []
        sentence = sentence.lower()
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        words = sentence.strip("\n").lower().split()
        index = 0
        while index < len(words):
            concept = words[index]
            longest_concept = concept
            for j in range(index + 1, index + 6):
                if j < len(words):
                    concept = concept + " " + words[j]
                    if self.new_is_concept(concept):
                        longest_concept = concept
                        index = j
                    else:
                        break
            if self.new_is_concept(longest_concept):
                concepts.append(longest_concept)
            index = index + 1
        return concepts

    def find_longest_concept_from_sentence(self, sentence):
        # 给一段文本，返回在KG里面出现的最长概念
        concepts = []
        sentence = sentence.lower()
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        words = sentence.strip("\n").lower().split()
        index = 0
        while index < len(words):
            concept = words[index]
            longest_concept = concept
            for j in range(index + 1, index + 6):
                if j < len(words):
                    concept = concept + " " + words[j]
                    if self.new_is_exist_concept(concept):
                        longest_concept = concept
                        index = j
                    else:
                        break
            # if self.is_exist_concept(longest_concept):
            if self.new_is_concept(longest_concept):
                concepts.append((longest_concept, 'valid'))
            else:
                concepts.append((longest_concept, 'invalid'))
            index = index + 1
        return concepts

    def get_random_node(self):
        count = []
        query = f'MATCH (n) RETURN n LIMIT 50'
        records = self.execute(query)
        random_records = random.sample(records, 5)
        for record in random_records:
            properties = {}
            for re in record['n']:
                if re == 'id':
                    continue
                properties[re] = record['n'][re]
            result = {
                "id": record['n']['id'],
                "properties": properties,
                "labels": record['n'].labels
            }
            count.append(result)
        return count

    def get_random_lastest_node(self):
        count = []
        max_num = self.get_node_num()
        num = 0
        i = 0
        while num <= 5:
            node = self.get_node_info_by_id(max_num - i)
            if node:
                count.append(node)
                num += 1
            i = i + 1
        return count

    def get_hot_concepts(self):
        # query = f'MATCH (n:concept) RETURN n'
        # records = self.execute(query)
        # results = []
        # for record in records:
        #     properties = {}
        #     for re in record['n']:
        #         if re == 'id':
        #             continue
        #         properties[re] = record['n'][re]
        #     result = {
        #         "id": record['n']['id'],
        #         'pagerank': record['n']['pagerank_score'],
        #         "properties": properties,
        #         "labels": record['n'].labels
        #     }
        #     results.append(result)
        result = sorted(self.concepts_list, key=lambda e: e['pagerank'], reverse=True)
        return result[:10]

    def return_hot_concepts(self):
        # 提前运行get_hot_concept保存结果
        hot_concepts = [{'id': 10824, 'pagerank': 0.012326411789583007,
                         'properties': {'sotag_count': '7011', 'Freebase ID': ['/m/0chln1'],
                                        'sotag_excerpt_post_id': '11816500', 'sotag_wiki_post_id': '11816499',
                                        'JSTOR topic ID': ['report-writing'],
                                        'sotag_shortdescription': 'A report contains summarized information from a data source, usually in an end-user-friendly format, such as PDF or Excel, although proprietary reporting tools (usually with built-in design tools) also exist.',
                                        'sotag_id': '6262', 'wikidata_id': 'Q10870555', 'GND ID': ['4005709-4'],
                                        'frequency': 2343, 'concept_name': 'report', 'score': 0.9847345251095273,
                                        'pagerank_score': 0.012326411789583007, 'P8408': ['WrittenReportOnSituation'],
                                        'other_definitions': [
                                            'A report is a purposeful presentation of data, typically for human review.',
                                            'A report contains summarized information from a data source, usually in an end-user-friendly format, such as PDF or Excel, although proprietary reporting tools (usually with built-in design tools) also exist.',
                                            'There is a multitude of software and services available to facilitate bug reporting, as well as numerous philosophies regarding how reports should be gathered, triaged, and resolved.',
                                            'Reports can be created entirely from code, using a purpose-built reporting tool, or using a hybrid approach, where the reporting tool generates code that can later be adapted.'],
                                        'alias': ['reports#1001', 'Report#842', 'Reports#333', 'REPORT#2'],
                                        'equivalent class': ['https://schema.org/Report'],
                                        'definition': 'A report is a human-readable representation of information from a data source, usually in summarized form (especially if the volume of raw data is large).',
                                        'wikidata_label_en': 'report', 'max_frequency': ['report#130'],
                                        'image': ['Brundtland en-077.png'],
                                        'exact match': ['https://citationstyles.org/ontology/type/report',
                                                        'http://purl.org/coar/resource_type/c_93fc'],
                                        'wikidata_slug': 'report', 'AAT ID': ['300027267'], 'EuroVoc ID': ['2891'],
                                        'sum_frequency': 4521, 'Gran Enciclopèdia Catalana ID': ['0188851'],
                                        'wikidata_descriptions_en': ['informational, formal, and detailed text'],
                                        'YSO ID': ['237'], 'P7749': ['13283'], 'wikidata_aliases_en': ['reports']},
                         'labels': frozenset({'entity', 'concept', 'wikidata'})},
                        {'id': 19660, 'pagerank': 0.008611316632723813,
                         'properties': {'PSH ID': ['12568'], 'sotag_count': '4788', 'Freebase ID': ['/m/030mbr'],
                                        'sotag_excerpt_post_id': '5146384', 'sotag_wiki_post_id': '5146383',
                                        'sotag_shortdescription': 'Visualization is any technique for creating images, diagrams, or animations to communicate a message.',
                                        'sotag_id': '1848', 'wikidata_id': 'Q451553', 'GND ID': ['4188417-6'],
                                        'Quora topic ID': ['Visualization'], 'P6366': ['36464697'],
                                        'subreddit': ['visualization'], 'frequency': 298,
                                        'concept_name': 'visualization', 'score': 0.9780249385552663,
                                        'pagerank_score': 0.008611316632723813, 'UNESCO Thesaurus ID': ['concept6822'],
                                        'Stack Exchange tag': ['https://stackoverflow.com/tags/visualization'],
                                        'Library of Congress authority ID': ['sh85143939'],
                                        'TED topic ID': ['visualizations'], 'other_definitions': [
                                 'Visualization is done using histograms, density plots and 3d volume rendering, allowing interactive exploration of big data.',
                                 'The visualization is intended to be used within an IPython notebook but can also be saved to a stand-alone HTML file for easy sharing.',
                                 'This visualization is fully introduced and explained in the CPU Flame Graphs page, and in Brendan Gregg presentation.'],
                                        'alias': ['visualizations#19', 'Visualization#85', 'Visualizations#4'],
                                        'definition': 'Visualization is any technique for creating images, diagrams, or animations to communicate a message.',
                                        'wikidata_label_en': 'visualization', 'max_frequency': ['visualization#13'],
                                        'image': ['Rettungszeichen Rettungsweg.svg', 'Bevpyr 2050.png',
                                                  'Saeulendiagramm-Beispiel.svg'], 'wikidata_slug': 'visualization',
                                        'AAT ID': ['300215284'], 'Zhihu topic ID': ['19635471'], 'sum_frequency': 406,
                                        'P6870': ['38189'], 'wikidata_descriptions_en': [
                                 'set of techniques for creating images, diagrams, or animations to communicate a message'],
                                        'YSO ID': ['7938'], 'Commons category': ['Visualization'],
                                        'STW Thesaurus for Economics ID': ['19806-3'], 'BabelNet ID': ['00080130n'],
                                        'wikidata_aliases_en': ['visualisation', 'Imaging'],
                                        'NDL Auth ID': ['01213306']},
                         'labels': frozenset({'entity', 'concept', 'wikidata'})},
                        {'id': 373, 'pagerank': 0.0077990290696506905,
                         'properties': {'sotag_count': '47252', 'Freebase ID': ['/m/01hyh_'], 'MeSH ID': ['D000069550'],
                                        'sotag_excerpt_post_id': '4676710', 'JSTOR topic ID': ['machine-learning'],
                                        'sotag_wiki_post_id': '4676709',
                                        'sotag_shortdescription': 'Implementation questions about machine learning algorithms. General questions about machine learning (concepts, theory, methodology, terminology, etc.) should be posted to their specific communities.',
                                        'sotag_id': '5990', 'wikidata_id': 'Q2539', 'GND ID': ['4193754-5'],
                                        'Quora topic ID': ['Machine-Learning'], 'P6366': ['119857082'],
                                        'subreddit': ['MachineLearning'], 'frequency': 80,
                                        'P5555': ['Machine learning workflow diagram.png'],
                                        'concept_name': 'machine learning',
                                        'MeSH Code': ['L01.224.050.375.530', 'G17.035.250.500'],
                                        'score': 0.9794591816847478, 'pagerank_score': 0.0077990290696506905,
                                        'P8408': ['MachineLearning'], 'P8529': ['4611'], 'Stack Exchange tag': [
                                 'https://datascience.stackexchange.com/tags/machine-learning',
                                 'https://ai.stackexchange.com/tags/machine-learning',
                                 'https://stats.stackexchange.com/tags/machine-learning',
                                 'https://stackoverflow.com/tags/machine-learning'],
                                        'Library of Congress authority ID': ['sh85079324'], 'other_definitions': [
                                 'Machine learning revolves around developing self-learning computer algorithms that function by virtue of discovering patterns in data and making intelligent decisions based on such patterns.',
                                 'Machine learning explores the construction and study of algorithms that can learn from and make predictions about data.'],
                                        'alias': ['Machine learning#23', 'Machine Learning#45'],
                                        'definition': 'Machine learning is a subfield of computer science that evolved from the study of pattern recognition and computational learning theory in artificial intelligence.',
                                        'wikidata_label_en': 'machine learning',
                                        'max_frequency': ['Machine learning#5'], 'BNCF Thesaurus ID': ['58790'],
                                        'image': ['Kernel Machine.svg'], 'wikidata_slug': 'machine-learning',
                                        'Zhihu topic ID': ['19559450'], 'Treccani ID': ['autoapprendimento'],
                                        'sum_frequency': 148, 'P9100': ['machinelearning', 'machine-learning'],
                                        'Encyclopædia Britannica Online ID': ['technology/machine-learning'],
                                        'Store norske leksikon ID': ['maskinlæring'], 'wikidata_descriptions_en': [
                                 'scientific study of algorithms and statistical models that computer systems use to perform tasks without explicit instructions'],
                                        'YSO ID': ['21846'], 'Commons category': ['Machine learning'],
                                        'BabelNet ID': ['01647033n'],
                                        'wikidata_aliases_en': ['ML', 'statistical learning'],
                                        'NDL Auth ID': ['001210569']},
                         'labels': frozenset({'entity', 'concept', 'wikidata'})},
                        {'id': 8810, 'pagerank': 0.007008995354408684,
                         'properties': {'Freebase ID': ['/m/01mf0'], 'NALT ID': ['28433'], 'P9272': ['19402'],
                                        'Universal Decimal Classification': ['004.42'],
                                        'Enciclopedia Italiana ID': ['software'], 'P6366': ['2777904410'],
                                        'subreddit': ['software'], 'Yahoo Answers category': ['396545664'],
                                        'frequency': 2700, 'TDKIV term ID': ['000000077'], 'MeSH Code': ['L01.224.900'],
                                        'score': 0.9814483441828803, 'pagerank_score': 0.007008995354408684,
                                        'UNESCO Thesaurus ID': ['concept6081'], 'Commons gallery': ['Software'],
                                        'ASC Leiden Thesaurus ID': ['294938281'],
                                        'Library of Congress authority ID': ['sh85029534'], 'other_definitions': [
                                 'Software as a service (SaaS), or "on-demand software," is a software delivery model in which software and its associated data are hosted centrally and are typically accessed by users using a thin client, normally using a web browser over the Internet.',
                                 'The software is available as open source software under modified versions of the Mozilla Public License or the original Eclipse Public License.',
                                 'Software offered includes iRidium studio, iRidium transfer, iRidium Server.',
                                 'Their software is used by customers, including companies, schools and libraries, to protect their networks from spyware, prevent students from viewing sexual or other inappropriate content, discourage employees from spending time browsing webpages instead of working, and similar purposes.'],
                                        'equivalent class': ['http://dbpedia.org/ontology/Software',
                                                             'http://purl.org/dc/dcmitype/Software'],
                                        'P7818': ['Logiciel'], 'wikidata_label_en': 'software', 'IAB code': ['602'],
                                        'max_frequency': ['software#457'],
                                        'exact match': ['http://purl.org/coar/resource_type/c_5ce6'],
                                        'image': ['Kmail.png'], 'wikidata_slug': 'software', 'AAT ID': ['300028566'],
                                        'Zhihu topic ID': ['19551718'], 'BNE ID': ['XX530960'], 'EuroVoc ID': ['1696'],
                                        'Gran Enciclopèdia Catalana ID': ['0143168'], 'P6573': ['Software'],
                                        'P8834': ['software'], 'P7502': ['Software-Y4G'],
                                        'Commons category': ['Software'], 'P7749': ['10402'], 'P8519': ['80398'],
                                        'P7827': ['Software'], 'P7829': ['Software'], 'BabelNet ID': ['00021497n'],
                                        'PSH ID': ['12463'], 'MeSH ID': ['D012984'], 'P6181': ['computer-software'],
                                        'Encyclopædia Universalis ID': ['logiciels'],
                                        'JSTOR topic ID': ['computer-software'], 'P7033': ['scot/4207'],
                                        'wikidata_id': 'Q7397', 'P10017': ['software'], 'P8885': ['소프트웨어'],
                                        'GND ID': ['4055382-6'],
                                        'Quora topic ID': ['Software-and-Applications', 'Logiciels'],
                                        'concept_name': 'software', 'OmegaWiki Defined Meaning': ['3493'],
                                        'P8408': ['Software'], 'Dewey Decimal Classification': ['005.3', '005'],
                                        'Guardian topic ID': ['technology/software'], 'TED topic ID': ['software'],
                                        'P6706': ['software'], 'alias': ['Software#754', 'softwares#39', 'Softwares#8'],
                                        'definition': 'Software as a service (SaaS), sometimes referred to as "on-demand software," is a software delivery model in which software and its associated data are hosted centrally (typically in the (Internet) cloud) and are typically accessed by users using a thin client, normally using a web browser over the Internet.',
                                        'IPTC Newscode': ['mediatopic/20000231'], 'pronunciation audio': [
                                 'LL-Q150 (fra)-Visiteuse JEP (Madehub)-logiciel libre.wav'],
                                        'PACTOLS thesaurus ID': ['pcrtfdq3v9ucyd'], 'sum_frequency': 3501,
                                        'Encyclopædia Britannica Online ID': ['technology/software'],
                                        'P9621': ['software'], 'Open Library subject ID': ['computer_software'],
                                        'UK Parliament thesaurus ID': ['90662'], 'BnF ID': ['133183707'],
                                        'wikidata_descriptions_en': ['non-tangible executable component of a computer'],
                                        'P8855': ['171-01-21'],
                                        'wikidata_aliases_en': ['computer software', 'computational tool'],
                                        'NDL Auth ID': ['00684642'],
                                        'Cultureel Woordenboek identifier': ['techologie-en-techniek/programmatuur']},
                         'labels': frozenset({'entity', 'concept', 'wikidata'})},
                        {'id': 12127, 'pagerank': 0.006739542111823018,
                         'properties': {'sotag_count': '180662', 'Freebase ID': ['/m/02bc6'],
                                        'sotag_excerpt_post_id': '4973766',
                                        'sotag_shortdescription': 'A database is an organized collection of data. It is the collection of schemas, tables, queries, reports, views, and other objects. The data are typically organized to model aspects of reality in a way that supports processes requiring information.\r\n\r\nUse this tag if you have questions about designing a database. If it is about a particular database management system, (e.g., MySQL), please use that tag instead.',
                                        'P6366': ['77088390'], 'subreddit': ['Database'], 'frequency': 24005,
                                        'TDKIV term ID': ['000000089'],
                                        'MeSH Code': ['L01.470.750', 'L01.313.500.750.300.188', 'V02.300'],
                                        'score': 0.9816348053941, 'pagerank_score': 0.006739542111823018,
                                        'P6009': ['1185'], 'UNESCO Thesaurus ID': ['concept501'],
                                        'Great Russian Encyclopedia Online ID': ['1845378'], 'P8309': ['18-216930'],
                                        'Stack Exchange tag': ['https://stackoverflow.com/tags/database'],
                                        'ASC Leiden Thesaurus ID': ['352624647'],
                                        'Library of Congress authority ID': ['sh86007767'], 'other_definitions': [
                                 'Databases that implement the Blueprints interfaces automatically support Blueprints-enabled applications.',
                                 'A database is an organized collection of data.',
                                 'The database is a simple data file containing records, each is a pair of a key and a value.',
                                 'Database (schema) optimization, where the database or schema itself is being optimized in order to minimize redundancy.'],
                                        'US National Archives Identifier': ['10634624'], 'P7818': ['Base_de_données'],
                                        'wikidata_label_en': 'database', 'IAB code': ['611'],
                                        'max_frequency': ['database#1241'], 'BNCF Thesaurus ID': ['3181'],
                                        'image': ['Database.svg'], 'wikidata_slug': 'database', 'AAT ID': ['300028543'],
                                        'Zhihu topic ID': ['19552067'], 'P6293': ['Y99512'],
                                        'Library of Congress Genre/Form Terms ID': ['gf2014026081'],
                                        'P8672': ['848921866995613696'], 'EuroVoc ID': ['4821'],
                                        'Gran Enciclopèdia Catalana ID': ['0221295', '0221296', '0221363'],
                                        'Store norske leksikon ID': ['database'], 'P8834': ['database'],
                                        'YSO ID': ['3056'], 'Commons category': ['Databases'], 'P7749': ['13673'],
                                        'P8519': ['80869'],
                                        'Dictionary of Algorithms and Data Structures ID': ['database'],
                                        'PhilPapers topic': ['databases'], 'BabelNet ID': ['00025333n'],
                                        'Encyclopedia of Modern Ukraine ID': ['38829'],
                                        'MeSH ID': ['D019991', 'D019992'],
                                        'JSTOR topic ID': ['databases', 'database-management-systems'],
                                        'sotag_wiki_post_id': '4973765', 'P7033': ['scot/4822'], 'sotag_id': '30',
                                        'wikidata_id': 'Q8513', 'GND ID': ['4113276-2'],
                                        'Quora topic ID': ['Databases-2'], 'concept_name': 'database',
                                        'alias': ['databases#2197', 'Database#4838', 'Databases#362', 'DATABASE#35',
                                                  'DataBase#136', 'dataBase#4', 'dAtabase#1', 'DatabasE#1'],
                                        'definition': 'The database is accessed via official drivers in Java, JavaScript, Python and .NET, or community-contributed drivers in PHP, Ruby, R, Golang, Elixir, Swift and more.',
                                        'PACTOLS thesaurus ID': ['pcrt1t50zTAfPG'], 'sum_frequency': 31579,
                                        'P9100': ['database'],
                                        'Encyclopædia Britannica Online ID': ['technology/database'],
                                        'UK Parliament thesaurus ID': ['90822'],
                                        'File Format Wiki page ID': ['Databases'], 'BnF ID': ['11931023c'],
                                        'wikidata_descriptions_en': ['organized collection of data in computing'],
                                        'P8855': ['171-09-21'], 'P8814': ['06650349-n'], 'P5748': ['54.64'],
                                        'wikidata_aliases_en': ['db', 'DB', 'database, DB'],
                                        'NDL Auth ID': ['00865521'],
                                        'Cultureel Woordenboek identifier': ['techologie-en-techniek/database']},
                         'labels': frozenset({'entity', 'concept', 'wikidata'})},
                        {'id': 985, 'pagerank': 0.005860706069730361,
                         'properties': {'sotag_count': '910', 'Freebase ID': ['/m/030v0'],
                                        'sotag_excerpt_post_id': '7056438', 'sotag_wiki_post_id': '7056437',
                                        'sotag_shortdescription': 'A file format is a particular way that information is encoded for storage in a computer file.',
                                        'sotag_id': '2322', 'wikidata_id': 'Q235557', 'P7497': ['FileFormat'],
                                        'GND ID': ['4433979-3'], 'Quora topic ID': ['File-Formats'],
                                        'P6366': ['97250363'], 'frequency': 331, 'concept_name': 'file format',
                                        'score': 0.9111283393827352, 'pagerank_score': 0.005860706069730361,
                                        'P8408': ['ComputerFileTypeByFormat'],
                                        'Stack Exchange tag': ['https://stackoverflow.com/tags/file-format'],
                                        'other_definitions': [
                                            'A file format is a particular way that information is encoded for storage in a computer file.',
                                            'This file format is designed for visual consistency, and very little useful normalized data can be extracted from its contents.',
                                            'File formats often have a published specification describing the encoding method.',
                                            'The file format was designed with a focus on both data integrity and decoder availability.'],
                                        'equivalent class': ['http://purl.org/dc/terms/FileFormat'],
                                        'alias': ['file formats#70', 'File format#27', 'FIle format#1',
                                                  'File Format#38', 'File Formats#7', 'FIle formats#1',
                                                  'File formats#2'],
                                        'definition': 'The BMP File Format, also known as Bitmap Image File or Device Independent Bitmap (DIB) file format or simply a Bitmap, is a Raster graphics image file format used to store bitmap digital images, independently of the display device (such as a graphics adapter), especially on Microsoft Windows and OS/2 operating systems.',
                                        'wikidata_label_en': 'file format', 'max_frequency': ['file format#37'],
                                        'exact match': ['https://schema.org/fileFormat'],
                                        'image': ['Image carte de points.png'], 'wikidata_slug': 'file-format',
                                        'AAT ID': ['300266011'], 'sum_frequency': 477,
                                        'Gran Enciclopèdia Catalana ID': ['0281508'], 'wikidata_descriptions_en': [
                                 'formalized structure of information stored on a computer'], 'P8834': ['fileFormat'],
                                        'Commons category': ['File formats'], 'wikidata_aliases_en': ['file type']},
                         'labels': frozenset({'entity', 'concept', 'wikidata'})},
                        {'id': 5836, 'pagerank': 0.005098152109366482,
                         'properties': {'Freebase ID': ['/m/04_tb'], 'subreddit': ['MapPorn', 'mapgore'],
                                        'frequency': 6937, 'TDKIV term ID': ['000000997'],
                                        'MeSH Code': ['V01.185.687', 'J01.897.280.500.426', 'L01.178.820.090.426',
                                                      'V02.700.450'], 'score': 0.9841357785518725,
                                        'pagerank_score': 0.005098152109366482, 'P9318': ['karta'],
                                        'page banner': ['Maps Pagebanner.jpg'], 'UNESCO Thesaurus ID': ['concept3270'],
                                        'Commons gallery': ['Map'],
                                        'Stack Exchange tag': ['https://stackoverflow.com/tags/maps'],
                                        'ASC Leiden Thesaurus ID': ['29492406X'],
                                        'Library of Congress authority ID': ['sh85080858', 'sh99002035'],
                                        'other_definitions': [
                                            "Maps are rendered via the MKMapView control, which offers scrolling, zooming, and optionally real-time highlighting of the user's current location on both traditional maps as well as satellite imagery.",
                                            'A map (also called dictionary or associative array) can be represented as a tree, typically a binary search tree.',
                                            'The map is ordered according to the natural ordering of its keys, or by a Comparator typically provided at sorted map creation time.',
                                            'Maps that depict the surface of the Earth also use a projection, a way of translating the three-dimensional real surface of the geoid to a two-dimensional picture.'],
                                        'US National Archives Identifier': ['10633667', '10640633'],
                                        'equivalent class': ['https://schema.org/Map'], 'P7818': ['Carte_(géographie)'],
                                        'wikidata_label_en': 'map', 'max_frequency': ['map#258'],
                                        'exact match': ['https://citationstyles.org/ontology/type/map'],
                                        'BNCF Thesaurus ID': ['1568', '1568'], 'image': ['World map.png'],
                                        'wikidata_slug': 'map', 'AAT ID': ['300028094'], 'Zhihu topic ID': ['19555554'],
                                        'P6293': ['Y95912'],
                                        'Library of Congress Genre/Form Terms ID': ['gf2011026387'],
                                        'EuroVoc ID': ['3930'], 'P6573': ['Landkarte'],
                                        'Store norske leksikon ID': ['kart'], 'P7305': ['3937450'], 'YSO ID': ['4987'],
                                        'P7749': ['13399'], 'Commons category': ['Maps'], 'P8519': ['92430'],
                                        'P7827': ['Mapa'], 'NYT topic ID': ['subject/maps'], 'PSH ID': ['4260'],
                                        'MeSH ID': ['D019532', 'D008377'], 'JSTOR topic ID': ['maps'],
                                        'P7033': ['scot/1877'], 'wikidata_id': 'Q4006', 'P8885': ['지도'],
                                        'GND ID': ['4029783-4'], 'P7712': ['T51-130'], 'concept_name': 'map',
                                        'OmegaWiki Defined Meaning': ['2249'], 'P7832': ['Mapa'], 'P8406': ['T054128'],
                                        'P8408': ['Map'], 'Dewey Decimal Classification': ['912'],
                                        'TED topic ID': ['map'],
                                        'alias': ['maps#923', 'Map#2466', 'Maps#402', 'MAP#43'],
                                        'definition': 'A map is a visual representation of an area—a symbolic depiction highlighting relationships between elements of that space such as objects, regions, and themes.',
                                        'pronunciation audio': ['LL-Q1860 (eng)-Adélaïde Calais WMFr-map.wav',
                                                                'LL-Q58635 (pan)-Gaurav Jhammat-ਨਕਸ਼ਾ.wav',
                                                                'LL-Q13955 (ara)-Spotless Mind1988-خريطة.wav'],
                                        'PACTOLS thesaurus ID': ['pcrteAptfa91ij'], 'Treccani ID': ['mappa'],
                                        'sum_frequency': 10771, 'Encyclopædia Britannica Online ID': ['science/map'],
                                        'Open Library subject ID': ['maps'], 'UK Parliament thesaurus ID': ['91927'],
                                        'File Format Wiki page ID': ['Maps'],
                                        'wikidata_descriptions_en': ['visual representation of a geographical area'],
                                        'wikidata_aliases_en': ['Map', 'geographic map'], 'NDL Auth ID': ['00573130'],
                                        'Cultureel Woordenboek identifier': ['aarde-weer-en-klimaat/kaart']},
                         'labels': frozenset({'entity', 'concept', 'wikidata'})},
                        {'id': 21815, 'pagerank': 0.004893100580453437, 'properties': {'Freebase ID': ['/m/081pkj'],
                                                                                       'Encyclopædia Universalis ID': [
                                                                                           'evenement-philosophie'],
                                                                                       'wikidata_id': 'Q1190554',
                                                                                       'P8168': ['Q9'],
                                                                                       'GND ID': ['4152718-5'],
                                                                                       'frequency': 467,
                                                                                       'concept_name': 'occurrence',
                                                                                       'score': 0.977568623421783,
                                                                                       'OmegaWiki Defined Meaning': [
                                                                                           '352392'],
                                                                                       'pagerank_score': 0.004893100580453437,
                                                                                       'P8408': ['Event'],
                                                                                       'Commons gallery': ['Event'],
                                                                                       'other_definitions': [
                                                                                           'An occurrence represents one information resource of a topic.',
                                                                                           'Every occurrence of an ORA-00600 should be reported to Oracle Support.'],
                                                                                       'alias': ['occurrences#508',
                                                                                                 'Occurrences#23',
                                                                                                 'Occurrence#13'],
                                                                                       'equivalent class': [
                                                                                           'http://www.popoloproject.com/specs/event.html',
                                                                                           'http://purl.org/dc/dcmitype/Event'],
                                                                                       'definition': 'The occurrence of zero elements in a large array is inefficient for both computation and storage.',
                                                                                       'wikidata_label_en': 'occurrence',
                                                                                       'max_frequency': [
                                                                                           'occurrence#17'],
                                                                                       'wikidata_slug': 'occurrence',
                                                                                       'AAT ID': ['300054722',
                                                                                                  '300069084'],
                                                                                       'Internet Encyclopedia of Philosophy ID': [
                                                                                           'events'],
                                                                                       'sum_frequency': 1011,
                                                                                       'Encyclopædia Britannica Online ID': [
                                                                                           'topic/event-occurrence'],
                                                                                       'wikidata_descriptions_en': [
                                                                                           'occurrence of a fact or object in space-time; instantiation of a property in an object'],
                                                                                       'Stanford Encyclopedia of Philosophy ID': [
                                                                                           'events'],
                                                                                       'Commons category': ['Events'],
                                                                                       'P8519': ['62960'],
                                                                                       'BabelNet ID': ['02131709n'],
                                                                                       'wikidata_aliases_en': [
                                                                                           'occurrant', 'perdurant',
                                                                                           'event', 'occurrences',
                                                                                           'occurants', 'perdurants',
                                                                                           'incident']},
                         'labels': frozenset({'entity', 'concept', 'wikidata'})},
                        {'id': 13, 'pagerank': 0.0041282634527656185,
                         'properties': {'sotag_count': '21947', 'Freebase ID': ['/m/0h1fn8h'],
                                        'MeSH ID': ['D000077321'], 'sotag_excerpt_post_id': '21494853',
                                        'Encyclopædia Universalis ID': ['apprentissage-profond-deep-learning'],
                                        'sotag_wiki_post_id': '21494852',
                                        'sotag_shortdescription': 'Deep Learning is an area of machine learning whose goal is to learn complex functions using special neural network architectures that are "deep"  (consist of many layers). This tag should be used for questions about implementation of deep learning architectures. General machine learning questions should be tagged "machine learning". Including a tag for the relevant software library (e.g., "keras", "tensorflow","pytorch","fast.ai" etc) is helpful.',
                                        'sotag_id': '100570', 'wikidata_id': 'Q197536',
                                        'P6363': ['http://data.thenextweb.com/tnw/entity/deep_learning'],
                                        'Quora topic ID': ['Deep-Learning'], 'P6366': ['108583219'],
                                        'subreddit': ['deeplearning'], 'concept_name': 'deep learning',
                                        'MeSH Code': ['L01.224.050.375.605.500', 'L01.224.050.375.530.250',
                                                      'G17.485.500', 'G17.035.250.500.250'],
                                        'score': 0.9805995603828482, 'pagerank_score': 0.0041282634527656185,
                                        'P6802': ['Computer vision sample in Simón Bolivar Avenue, Quito.jpg'],
                                        'P8529': ['461103'],
                                        'Stack Exchange tag': ['https://ai.stackexchange.com/tags/deep-learning',
                                                               'https://or.stackexchange.com/tags/deep-learning',
                                                               'https://stackoverflow.com/tags/deep-learning'],
                                        'other_definitions': [
                                            'Deep Learning is an area of machine learning whose goal is to learn complex functions using special neural network architectures that are "deep"  (consist of many layers).',
                                            'Deep Learning was introduced into machine learning research with the intention of moving machine learning closer to artificial intelligence.'],
                                        'definition': 'Deep Learning is a branch of machine-learning aimed at building neural-networks to learn complex functions using special neural network architectures with many layers (hence the term "deep").',
                                        'wikidata_label_en': 'deep learning', 'image': ['Deep Learning.jpg'],
                                        'wikidata_slug': 'deep-learning', 'Zhihu topic ID': ['19813032'],
                                        'P9100': ['deep-learning-tutorial', 'deep-learning', 'deeplearning'],
                                        'Store norske leksikon ID': ['Dyp_læring', 'dyp_læring'],
                                        'wikidata_descriptions_en': ['branch of machine learning'],
                                        'P7502': ['Deep_learning-PE5E9Y'], 'P9526': ['Deep_Learning'],
                                        'Commons category': ['Deep learning'],
                                        'wikidata_aliases_en': ['deep machine learning', 'deep structured learning',
                                                                'hierarchical learning', 'DL', 'Deep Learning']},
                         'labels': frozenset({'entity', 'concept', 'wikidata'})},
                        {'id': 637, 'pagerank': 0.003775668807192133,
                         'properties': {'sotag_count': '323', 'Freebase ID': ['/m/0fch0p'],
                                        'sotag_excerpt_post_id': '25006881',
                                        'sotag_shortdescription': 'Social media is the social interaction among people in which they create, share or exchange information and ideas in virtual communities and networks.',
                                        'P6200': ['c207p54m4pdt'], 'P6366': ['518677369'],
                                        'TDKIV term ID': ['000015958'],
                                        'MeSH Code': ['L01.178.751', 'L01.224.230.110.500.750'],
                                        'score': 0.9810864177766387, 'pagerank_score': 0.003775668807192133,
                                        'P9318': ['sosiala-mediat'], 'UNESCO Thesaurus ID': ['concept17089'],
                                        'P8309': ['18-209641'], 'ASC Leiden Thesaurus ID': ['363920803'],
                                        'Library of Congress authority ID': ['sh2006007023'],
                                        'Google News ID': ['CAAqJggKIiBDQkFTRWdvSkwyMHZNR1pqYURCd0VnVmxiaTFIUWlnQVAB'],
                                        'wikidata_label_en': 'social media', 'IAB code': ['1016'],
                                        'BNCF Thesaurus ID': ['61972'], 'image': ['Conversationprism.jpeg'],
                                        'wikidata_slug': 'social-media', 'AAT ID': ['300312269'], 'P6293': ['Y155091'],
                                        'P8672': ['1196446161223028736'], 'P6573': ['Soziale_Medien'],
                                        'YSO ID': ['20774'], 'Commons category': ['Social media'],
                                        'P6417': ['socialMedia'], 'NYT topic ID': ['subject/social-media'],
                                        'MeSH ID': ['D061108'],
                                        'Encyclopædia Universalis ID': ['reseaux-sociaux-internet'],
                                        'Dagens Nyheter topic ID': ['sociala-medier'],
                                        'JSTOR topic ID': ['social-media'], 'sotag_wiki_post_id': '25006879',
                                        'P7033': ['scot/16484'], 'sotag_id': '3641', 'wikidata_id': 'Q202833',
                                        'GND ID': ['4639271-3'], 'Quora topic ID': ['Social-Media'], 'P7952': ['1561'],
                                        'P9775': ['media-sociali'], 'concept_name': 'social media',
                                        'P8408': ['SocialMedia'], 'Guardian topic ID': ['media/social-media'],
                                        'TED topic ID': ['social+media'], 'alias': ['Social Media#19'],
                                        'IPTC Newscode': ['mediatopic/20001182'], 'P9100': ['social-media'],
                                        'P6870': ['4805'], 'Encyclopædia Britannica Online ID': ['topic/social-media'],
                                        'BnF ID': ['16629517q'], 'UK Parliament thesaurus ID': ['93050'],
                                        'wikidata_descriptions_en': [
                                            'interaction among people in which they create, share, and/or exchange information and ideas in virtual communities and networks'],
                                        'PolitiFact Personality ID': ['social-media'], 'wikidata_aliases_en': []},
                         'labels': frozenset({'entity', 'concept', 'wikidata'})}]
        return hot_concepts

    def cul_in_related_node(self, concept):
        in_re = self.get_in_relation_info_by_concept(concept)
        nodes = {}
        for in_concept in in_re:
            in_node = in_concept[0]
            if in_concept[1] not in self.constant.relation_score:
                re_score = 0.6 * 0.6 + float(self.re_weight[in_concept[1]])
            else:
                # 计算关系得分
                re_score = self.constant.relation_score[in_concept[1]] * 0.6 + float(
                    self.re_weight[in_concept[1]]) * 0.4
            # 计算结点得分
            pagerank_score = in_node['properties']['pagerank_score']
            p_score = math.log10(pagerank_score * 10000000) / math.log10(
                10000000.000021683)  # 10000000.000169972(V3.1.46)  (3.0.-10000000.000014795)
            if not 'frequency' in in_node['properties']:
                frequency = 1
            else:
                frequency = in_node['properties']['sum_frequency']
            f_score = math.log10(frequency) / math.log10(10820730)  # 10877974 (V3.1.46) (3.0.-  10021884)
            node_score = p_score * 0.7 + f_score * 0.3
            sum_score = re_score * node_score
            nodes[sum_score] = in_concept
        nodes = sorted(nodes.items(), key=lambda d: d[0], reverse=True)
        return nodes

    def cul_out_related_node(self, concept):
        # node = self.get_node_by_concept(concept)[0]
        # sum_pscore = self.get_sum_pagerank_score()
        # sum_frequency =
        out_re = self.get_out_relation_info_by_concept(concept)
        nodes = {}
        print('bbbb')
        for out_concept in out_re:
            out_node = out_concept[2]
            # 计算关系得分
            if out_concept[1] not in self.constant.relation_score:
                re_score = 0.6 * 0.6 + float(self.re_weight[out_concept[1]])
            else:
                re_score = self.constant.relation_score[out_concept[1]] * 0.6 + float(
                    self.re_weight[out_concept[1]]) * 0.4
            # 计算结点得分
            pagerank_score = out_node['properties']['pagerank_score']
            p_score = math.log10(pagerank_score * 10000000) / math.log10(10000000.000021683)
            if not 'frequency' in out_node['properties']:
                frequency = 1
            else:
                frequency = out_node['properties']['sum_frequency']
            f_score = math.log10(frequency) / math.log10(10820730)
            node_score = p_score * 0.7 + f_score * 0.3
            sum_score = re_score * node_score
            # print(sum_score)
            nodes[sum_score] = out_concept
        nodes = sorted(nodes.items(), key=lambda d: d[0], reverse=True)
        return nodes

    def get_upper_concept(self, concept):
        node = self.get_node_by_concept(concept)
        if not node:
            return []
        relations = self.get_out_relation_info_by_concept(concept)
        upper_concepts = []
        for relation in relations:
            if relation[1] == 'is a' or relation[1] == 'instance of' or relation[1] == 'subclass of':
                upper_concepts.append(relation[2])
        return upper_concepts

    def get_common_upper_concept(self, concept1, concept2):
        node1_upper_concepts = self.get_upper_concept(concept1)
        node2_upper_concepts = self.get_upper_concept(concept2)
        upper_concepts = []
        for upconcept in node1_upper_concepts:
            if upconcept in node2_upper_concepts:
                upper_concepts.append(upconcept)
        return upper_concepts

