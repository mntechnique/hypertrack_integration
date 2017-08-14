# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, pytz
from frappe.model.document import Document
from hypertrack_integration.hypertrack_integration.doctype.hypertrack_settings.hypertrack_settings import get_hypertrack 

class HyperTrackAction(Document):
	
	def validate(self):
		hypertrack = get_hypertrack()
		scheduled_at = frappe.utils.data.get_datetime(self.scheduled_at_dt)
		scheduled_at = scheduled_at.replace(tzinfo=pytz.timezone(frappe.utils.get_time_zone()))
		scheduled_at = scheduled_at.utcnow().isoformat()+"Z"

		place = frappe.get_doc("HyperTrack Place", self.expected_place)
		expected_place = { "address": place.address }

		if not self.hypertrack_id:
			new_hypertrack_action = hypertrack.Action.create(
					type=self.type,
					scheduled_at=scheduled_at,
					expected_place=expected_place,
					lookup_id=self.lookup_id
				)

			#self.lookup_id = new_hypertrack_action.lookup_id
			self.metadata = new_hypertrack_action.metadata
			self.name = new_hypertrack_action.id
			self.hypertrack_id = new_hypertrack_action.id
		else:
			action = hypertrack.Action.retrieve(self.hypertrack_id)

			action.type = self.type
			#action.lookup_id = self.lookup_id
			action.scheduled_at = self.scheduled_at
			action.expected_place = self.expected_place
			action.metadata = self.metadata

	def on_trash(self):
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

	
