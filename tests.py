from Extract_Info import get_information, Node, Graph, find_median, find_max_time, within_sixty, main
import unittest
import datetime
import json
import ast
"inside tests"

#usefor testing purposes; tested manually, checking median output against pencil and paper work; tested for cases of payments within each other,
#payments out of order but within window, and out of order but not in 60 second window
#also tested for one connection versus multiple connections, removing and adding connections, making sure no nodes with no connections

nodes_list1 = []
mindate = datetime.datetime(year= datetime.MINYEAR, month = 1, day = 1, hour = 0, minute = 0, second = 0)
test1date = datetime.datetime(year= datetime.MINYEAR, month = 1, day = 1, hour = 0, minute = 0, second = 15)
test2date = datetime.datetime(year= datetime.MINYEAR, month = 1, day = 1, hour = 3, minute = 0, second = 59)
test3date = datetime.datetime(year= datetime.MINYEAR, month = 1, day = 1, hour = 3, minute = 0, second = 56)
testlist = [["wayne", "libby", test1date], ["wayne", "hammersmith", test1date], ["gretsky", "brick", test1date],
            ["libby", "scott", test2date], ["gretchen", "lionel", test1date], ["olivia", "nieman", mindate],
            ["brett", "johnny", test3date], ["brett", "gretchen", test3date], ["brett", "louisa", test3date], ["gretchen", "samuel", test2date]]
testlist2 = [["brett", "johnny", test3date], ["brett", "gretchen", test3date], ["brett", "louisa", test3date],
             ["johnny", "gretchen", test3date], ["johnny", "samuel", test3date], ["louisa", "samuel", test3date], ["samuel", "gretchen", test3date]]
node1 = Node("libby")
node2 = Node("louisa")
node3 = Node("wilma")

class testInsightChallenge(unittest.TestCase):
    def test_check_type_get_info(self):
        self.assertEqual(type(get_information()), type([["guacamole"],["orangutan"]]))
    def test_find_median_type(self):
        self.assertEqual(type(find_median([3, 4, 5, 6])), type(3.0))
    def test_find_median_even_list(self):
        self.assertTrue(find_median([3,4,5,6])==4.5)
    def test_find_median_odd_list(self):
        self.assertTrue(find_median([3,4,5,6,7])==5.0)
    def test_within_sixty(self):
        self.assertTrue(within_sixty(test2date, test3date))
    def test_within_sixt_not_true(self):
        self.assertFalse(within_sixty(test1date, test2date))
    def test_node_get_actor_type(self):
        self.assertEqual(type(Node("jamila").get_actor()), type("horace"))
    def test_nodes_are_equal(self):
        self.assertEqual(Node("lucy"), Node("lucy"))
    def test_add_node(self):
        g = Graph(nodes_list1, mindate)
        g.add_node(node1)
        self.assertTrue(len(g.get_nodes())==1)
        g.add_node(node2)
        self.assertTrue(len(g.get_nodes())==2)
        g.remove_node(node1)
        self.assertTrue(len(g.get_nodes())==1)
    def test_add_edge(self):
        gr = Graph(nodes_list1, mindate)
        gr.add_node(node1)
        gr.add_node(node3)
        gr.add_edge(node1, node3)
        self.assertTrue(node3 in gr.get_nodes()[node1])
        self.assertTrue(node1 in gr.get_nodes()[node3])
    def test_remove_node_after_adding_edge(self):
        gr = Graph(nodes_list1, mindate)
        gr.add_node(node1)
        gr.add_node(node1)
        gr.add_edge(node1, node1)
        self.assertTrue(len(gr.get_nodes()) == 1)
    #I tested that the main function manually using testlist, above, replacing list1 = get_information() with list1 = testlist or testlist2
    #as described in the first comment above
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(testInsightChallenge)

    unittest.TextTestRunner(verbosity=2).run(suite)
