# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from hypertrack_integration.hypertrack_integration.doctype.hypertrack_settings.hypertrack_settings import get_hypertrack 
import json

class HyperTrackUser(Document):
	def after_insert(self):
		hypertrack = get_hypertrack()

		if self.group_id:
			new_hypertrack_user = hypertrack.User.create( \
				name=self.hypertrack_name, \
				phone=self.phone, \
				group_id=self.group_id)
		else:
			new_hypertrack_user = hypertrack.User.create( \
				name=self.hypertrack_name, \
				phone=self.phone)

		self.created_at = new_hypertrack_user.created_at
		self.availability_status = new_hypertrack_user.availability_status 
		self.display = new_hypertrack_user.display
		self.group_id = new_hypertrack_user.group_id
		self.hypertrack_id = new_hypertrack_user.id
		self.is_connected = new_hypertrack_user.is_connected
		self.last_battery = new_hypertrack_user.last_battery
		self.last_heartbeat_at = new_hypertrack_user.last_heartbeat_at
		self.last_location = new_hypertrack_user.last_location
		self.location_status = new_hypertrack_user.location_status
		self.lookup_id = new_hypertrack_user.lookup_id
		self.modified_at = new_hypertrack_user.modified_at
		self.name = new_hypertrack_user.name
		self.pending_actions = json.dumps(new_hypertrack_user.pending_actions)
		self.phone = new_hypertrack_user.phone
		self.vehicle_type = new_hypertrack_user.vehicle_type


	def on_update(self):
		#Update hypertrack user from local user.
		hypertrack = get_hypertrack()
		user = hypertrack.User.retrieve(self.hypertrack_id)

		if self.availability_status:
			user.availability_status = self.availability_status 
		if self.display:
			user.display = self.display
		if self.group_id:
			user.group_id = self.group_id
		if self.is_connected:
			user.is_connected = self.is_connected
		if self.last_battery:
			user.last_battery = self.last_battery
		if self.last_heartbeat_at:
			user.last_heartbeat_at = self.last_heartbeat_at
		if self.location_status:
			user.location_status = self.location_status
		if self.lookup_id:
			user.lookup_id = self.lookup_id
		if self.modified_at:
			user.modified_at = self.modified_at
		if self.name:
			user.name = self.name
		if self.vehicle_type:
			user.vehicle_type = self.vehicle_type

		user.save()

	def on_delete(self):
		hypertrack = get_hypertrack()
		user = hypertrack.User.retrieve(self.hypertrack_id)

		user.delete()


