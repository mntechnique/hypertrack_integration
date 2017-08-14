# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import requests
from frappe.model.document import Document
from frappe.utils.nestedset import NestedSet
from hypertrack_integration.hypertrack_integration.doctype.hypertrack_settings.hypertrack_settings import get_hypertrack 

class HyperTrackGroup(NestedSet):
	nsm_parent_field = "parent_hypertrack_group"
	
	def validate(self):
		if self.hypertrack_group_name != "All HyperTrack Groups":
			hypertrack = HTGroup(frappe.db.get_value("HyperTrack Settings",None, "hypertrack_secret_key"))
			new_hypertrack_group = hypertrack.create(
				name = self.hypertrack_group_name,
				parent_group_id = self.parent_hypertrack_group
			)
			for x in xrange(1,10):
				print(new_hypertrack_group)

	# def on_update(self):
	# 	if self.hypertrack_group_name != "All HyperTrack Groups":
	# 		hypertrack = HTGroup(frappe.db.get_value("HyperTrack Settings", None, "hypertrack_secret_key"))
	# 		group = hypertrack.retrieve(self.hypertrack_id)

	# 		if self.hypertrack_group_name:
	# 			group.name = self.hypertrack_group_name
	# 		group.save()

	def on_delete(self):
		if self.hypertrack_group_name != "All HyperTrack Groups":
			hypertrack = get_hypertrack()
			group = hypertrack.Group.delete()

class HTGroup():
	def __init__(self, sk):
		self.headers = {
			'Authorization': sk,
			'Content-Type': 'application/json',
		}
		self.group_base_url = 'https://api.hypertrack.com/api/v1/groups/'

	def create(self, name, parent_group_id):
		data = {
			"name": name,
			"parent_group_id": parent_group_id
		}
		try:
			response = requests.post(self.group_base_url, headers=self.headers, data=data)
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
			return response.json()
		except Exception as e:
			raise e
