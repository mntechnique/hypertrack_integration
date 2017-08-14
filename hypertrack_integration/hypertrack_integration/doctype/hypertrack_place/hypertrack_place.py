# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from hypertrack_integration.hypertrack_integration.doctype.hypertrack_settings.hypertrack_settings import get_hypertrack 
import json

class HyperTrackPlace(Document):
	def validate(self):
		address_line1, address_line2 = frappe.get_value("Address", self.frappe_address, ["address_line1", "address_line2"])
		self.address = " ".join([address_line1 or "", address_line2 or ""])
		
		hypertrack = get_hypertrack()

		if self.hypertrack_id:
			existing_place = hypertrack.Place.retrieve(self.hypertrack_id)
			if existing_place:
				if self.modified_at != existing_place.modified_at:
					self.modified_at = existing_place.modified_at
				return
		else:
			new_hypertrack_place = hypertrack.Place.create(
				address=self.address,
				city=self.city,
				name=self.hypertrack_name,
				landmark=self.landmark,
				zip_code=self.zip_code,
				state=self.state,
				country=self.country
			)
			for x in xrange(1,10):
				print(new_hypertrack_place)

			self.hypertrack_id = new_hypertrack_place.id
			self.location = json.dumps(new_hypertrack_place.location)

	def on_trash(self):
		hypertrack = get_hypertrack()
		place = hypertrack.Place.retrieve(self.hypertrack_id)
		place.delete()
