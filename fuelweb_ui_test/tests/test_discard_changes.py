import time
from pageobjects.environments import Environments, DiscardChangesPopup
from pageobjects.nodes import Nodes, RolesPanel, DeleteNodePopup
from tests import preconditions
from tests.base import BaseTestCase


class TestDiscardEnvironmentChanges(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()

    def setUp(self):
        BaseTestCase.clear_nailgun_database()
        BaseTestCase.setUp(self)
        preconditions.Environment.simple_flat()
        Environments().create_cluster_boxes[0].click()
        time.sleep(1)
        preconditions.Environment().deploy_nodes(1, 2)

    def _discard_changes(self):
        Nodes().discard_changes.click()
        with DiscardChangesPopup() as p:
            p.discard.click()
            p.wait_until_exists()

        time.sleep(2)
        self.assertEqual(3, len(Nodes().nodes), 'Nodes amount')
        for node in Nodes().nodes:
            self.assertEqual('ready', node.status.text.lower(),
                             'Node status is READY')

    def test_discard_adding_node(self):
        Nodes().add_nodes.click()
        Nodes().nodes_discovered[0].checkbox.click()
        RolesPanel().compute.click()
        Nodes().apply_changes.click()
        time.sleep(1)
        self._discard_changes()

    def test_discard_deleting_node(self):
        with Nodes() as n:
            n.nodes[1].checkbox.click()
            n.delete_nodes.click()
        with DeleteNodePopup() as p:
            p.delete.click()
            p.wait_until_exists()
            time.sleep(1)
        self._discard_changes()
