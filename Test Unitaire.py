import unittest
import requests
from fastapi.testclient import TestClient
import sys
from app import app
from Model import Item
from main import updateItem, addItem, get_session


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.session = next(get_session())
        self.item = Item(task="test_task")
        self.session.add(self.item)
        self.session.commit()
        self.item_id = self.item.id

    def tearDown(self):
        self.session.delete(self.item)
        self.session.commit()
        self.session.close()

    def test_get_items(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_item(self):
        response = self.client.get(f"/{self.item_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.item_id)
        self.assertEqual(response.json()["task"], "test_task")

    def test_add_item(self):
        new_item = addItem(task="new_task")
        response = self.client.post("/", json=new_item.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["task"], "new_task")

    def test_update_item(self):
        updated_item = updateItem(task="updated_task")
        response = self.client.put(f"/{self.item_id}", json=updated_item.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["task"], "updated_task")

    def test_delete_item(self):
        response = self.client.delete(f"/{self.item_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'item terminated ')


if __name__ == '__main__':
    unittest.main()
    sys.path.insert('C:\\Users\\email\\PycharmProjects\\CrudApi\\')
