# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from hypertrack_integration.hypertrack_integration.doctype.hypertrack_settings.hypertrack_settings import get_hypertrack 
import json

class HyperTrackUser(Document):
	def validate(self):
		hypertrack = get_hypertrack()

		new_hypertrack_user = None

		mobile_no = "+91" + self.phone if self.phone else ""

		if self.hypertrack_id:
			existing_htuser = hypertrack.User.retrieve(self.hypertrack_id)
			if existing_htuser:
				self.availability_status = existing_htuser.availability_status
				return
		else:
			if self.group_id:
				group_hypertrack_id = frappe.db.get_value("HyperTrack Group", self.group_id, "hypertrack_id")

				new_hypertrack_user = hypertrack.User.create( \
					name=self.hypertrack_name, \
					phone=mobile_no, \
					group_id=group_hypertrack_id)
			else:
				try:
					new_hypertrack_user = hypertrack.User.create( \
						name=self.hypertrack_name, \
						phone=mobile_no)
				
					print ("NEW HT USER", new_hypertrack_user)
						
					self.hypertrack_name = new_hypertrack_user.get("name")
					self.hypertrack_id = new_hypertrack_user.get("id")
					self.phone = new_hypertrack_user.get("phone")
					self.group_id = new_hypertrack_user.get("group_id")
					self.lookup_id = new_hypertrack_user.get("lookup_id")
					self.availability_status = new_hypertrack_user.get("availability_status") 
					self.location_status = new_hypertrack_user.get("location_status")
					self.pending_actions = json.dumps(new_hypertrack_user.get("pending_actions"))
					self.last_location = json.dumps(new_hypertrack_user.get("last_location"))
					self.last_heartbeat_at = new_hypertrack_user.get("last_heartbeat_at")
					self.last_battery = new_hypertrack_user.get("last_battery")
					self.created_at = new_hypertrack_user.get("created_at")
					self.modified_at = new_hypertrack_user.get("modified_at")
					self.vehicle_type = new_hypertrack_user.get("vehicle_type")
					self.display = json.dumps(new_hypertrack_user.get("display"))
					self.is_connected = new_hypertrack_user.get("is_connected")

				except Exception as e:
					print("Cant make new HT User", e)
			
	def on_trash(self):
		try:
			hypertrack = get_hypertrack()
			user = hypertrack.User.retrieve(self.hypertrack_id)
			user.delete()
		except Exception as e:
			pass#raise e

	def assign_actions(self, actions):
		hypertrack = get_hypertrack()	
		user = hypertrack.User.retrieve(self.hypertrack_id)	
			
		print ("USER", user)

		action_ids = [action.name for action in actions]

		print ("HT ACTION IDS", action_ids)

		user.assign_actions(action_ids=action_ids)
