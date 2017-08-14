# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import requests
import json
from frappe.model.document import Document
from frappe.utils.nestedset import NestedSet
from hypertrack_integration.hypertrack_integration.doctype.hypertrack_settings.hypertrack_settings import get_hypertrack 

class HyperTrackGroup(NestedSet):
	nsm_parent_field = "parent_hypertrack_group"
	
	def validate(self):
		if self.hypertrack_group_name != "All HyperTrack Groups" and not self.hypertrack_id:
			hypertrack = HTGroup(frappe.db.get_value("HyperTrack Settings",None, "hypertrack_secret_key"))
			parent_group_id = None
			if self.parent_hypertrack_group and self.parent_hypertrack_group != "All HyperTrack Groups":
				parent_group_id = frappe.db.get_value("HyperTrack Group", self.parent_hypertrack_group, "hypertrack_id")

			new_hypertrack_group = hypertrack.create(
				name = self.hypertrack_group_name,
				parent_group_id = parent_group_id
			)

			self.created_at = new_hypertrack_group.get("created_at")
			self.hypertrack_id = new_hypertrack_group.get("id")
			self.modified_at = new_hypertrack_group.get("modified_at")
			self.hypertrack_group_name = new_hypertrack_group.get("name")

			parent_hypertrack_group = self.parent_hypertrack_group \
				if self.parent_hypertrack_group == "All HyperTrack Groups" else None

			if new_hypertrack_group.get("parent_group_id"):
				parent_hypertrack_group = frappe.db.get_value("HyperTrack Group", {"hypertrack_id": new_hypertrack_group.get("parent_group_id")}, "hypertrack_group_name")

			self.parent_hypertrack_group = parent_hypertrack_group
			self.token = new_hypertrack_group.get("token")

		elif self.hypertrack_group_name != "All HyperTrack Groups" and self.hypertrack_id:
			hypertrack = HTGroup(frappe.db.get_value("HyperTrack Settings", None, "hypertrack_secret_key"))
			updated_group = hypertrack.update(self.hypertrack_id, self.hypertrack_group_name)
			for x in xrange(1,10):
				print(updated_group or "Nogroup")
			self.hypertrack_group_name = updated_group.get("name")
			self.modified_at = updated_group.get("modified_at")

	def on_trash(self):
		if self.hypertrack_group_name != "All HyperTrack Groups":
			hypertrack = HTGroup(frappe.db.get_value("HyperTrack Settings",None, "hypertrack_secret_key"))
			group = hypertrack.delete(self.hypertrack_id)

class HTGroup():
	def __init__(self, sk):
		self.headers = {
			'Authorization': "token " + sk,
			'Content-Type': 'application/json',
		}
		self.group_base_url = 'https://api.hypertrack.com/api/v1/groups/'

	def create(self, name, parent_group_id=None):
		data = {
			"name": name
		}
		if parent_group_id:
			data["parent_group_id"] = parent_group_id

		try:
			response = requests.post(self.group_base_url, headers=self.headers, data=json.dumps(data))
			return response.json()
		except Exception as e:
			raise e

	def retrieve(self, group_uuid):
		try:
			response = requests.get(self.group_base_url + group_uuid, headers=self.headers)
			return response.json()
		except Exception as e:
			raise e

	def delete(self, group_uuid):
		try:
			response = requests.delete(self.group_base_url + group_uuid, headers=self.headers)
			return response.text
		except Exception as e:
			raise e

	def list(self):
		try:
			response = requests.get(self.group_base_url, headers=self.headers)
			return response.json()
		except Exception as e:
			raise e

	def update(self, group_uuid, changed_group_name):
		data = {
			"name": changed_group_name
		}
		try:
			response = requests.patch(self.group_base_url + group_uuid, headers=self.headers, data=json.dumps(data))
			return response.json()
		except Exception as e:
			raise e