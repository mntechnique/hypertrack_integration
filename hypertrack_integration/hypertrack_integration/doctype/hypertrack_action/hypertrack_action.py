# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from hypertrack_integration.hypertrack_integration.doctype.hypertrack_settings.hypertrack_settings import get_hypertrack 

class HyperTrackAction(Document):
	
	def after_insert(self):
		hypertrack = get_hypertrack()
		new_hypertrack_action = hypertrack.Action.create(\
			type=self.type,
			scheduled_at=self.scheduled_at,
			expected_place=self.expected_place)

		self.lookup_id = new_hypertrack_action.lookup_id
		self.metadata = new_hypertrack_action.metadata

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
		action.delete()

	def assign_to_user(self, frappe_user):
		hypertrack_user_id = frappe.db.get_value("User", frappe_user, "hypertrack_id")

		hypertrack = get_hypertrack()
		user = hypertrack.User.retrieve(hypertrack_user_id)
		user.assign_actions(action_ids=[self.hypertrack_id])

	def complete(self):
		hypertrack = get_hypertrack()
		action = hypertrack.Action.retrieve(self.hypertrack_id)
		action.complete()

	def cancel_action(self):
		hypertrack = get_hypertrack()
		action = hypertrack.Action.retrieve(self.hypertrack_id)
		action.cancel()

	
