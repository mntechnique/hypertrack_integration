# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from hypertrack_integration.hypertrack_integration.doctype.hypertrack_settings.hypertrack_settings import get_hypertrack 

class HyperTrackPlace(Document):
	def before_insert(self):
		hypertrack = get_hypertrack()
		new_hypertrack_place = hypertrack.Action.create( \
			name=self.hypertrack_name, \
			parent_group_id = self.parent_hypertrack_group)

		self.hypertrack_name = new_hypertrack_place.name
		self.address = new_hypertrack_place.address
		self.landmark = new_hypertrack_place.landmark
		self.zip_code = new_hypertrack_place.zip_code
		self.city = new_hypertrack_place.city
		self.state = new_hypertrack_place.state
		self.country = new_hypertrack_place.country
		self.location = new_hypertrack_place.location

	def on_update(self):
		hypertrack = get_hypertrack()
		action = hypertrack.Action.retrieve(self.hypertrack_id)

		action.type = self.type
		action.lookup_id = self.lookup_id
		action.scheduled_at = self.scheduled_at
		action.expected_place = self.expected_place
		action.metadata = self.metadata

		action.save()

	def on_delete(self):
		hypertrack = get_hypertrack()
		action = hypertrack.Action.retrieve(self.hypertrack_id)
		action.delete():

