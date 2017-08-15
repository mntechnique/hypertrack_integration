# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from hypertrack_integration.hypertrack import HTGeoFence
import json
import geojson
import pytz

class HyperTrackGeofence(Document):
	def validate(self):
		if not self.hypertrack_id:
			hypertrack = HTGeoFence(frappe.db.get_value("HyperTrack Settings",None, "hypertrack_secret_key"))
			expire_at = None
			place_by_type = None
			if self.geofence_type == "location":
				if self.address:
					place_by_type = {"address":frappe.db.get_value("HyperTrack Place", self.place, "address")}
				if self.point:
					place_by_type = geojson.Point(tuple(json.loads(self.point)))

			if self.expire_at:
				expire_at = frappe.utils.data.get_datetime(self.expire_at)
				expire_at = expire_at.replace(tzinfo=pytz.timezone(frappe.utils.get_time_zone()))
				expire_at = expire_at.astimezone(pytz.utc).isoformat()

			new_hypertrack_geofence = hypertrack.create(
				user_id = frappe.db.get_value("HyperTrack User", self.user_id, "hypertrack_id"),
				geofence_type = self.geofence_type,
				place = place_by_type,
				min_duration = self.min_duration,
				max_duration = self.max_duration,
				expire_at = expire_at
			)

			if not new_hypertrack_geofence.get("id"):
				raise Exception(new_hypertrack_geofence)

			self.name = new_hypertrack_geofence.get("id")
			self.hypertrack_id = new_hypertrack_geofence.get("id")


		elif self.hypertrack_id:
			hypertrack = HTGeoFence(frappe.db.get_value("HyperTrack Settings",None, "hypertrack_secret_key"))
			place_by_type = {"address":frappe.db.get_value("HyperTrack Place", self.place, "address")}
			expire_at = None
			if self.expire_at:
				expire_at = frappe.utils.data.get_datetime(self.expire_at)
				expire_at = expire_at.replace(tzinfo=pytz.timezone(frappe.utils.get_time_zone()))
				expire_at = expire_at.astimezone(pytz.utc).isoformat()

			if self.point:
				place_by_type = geojson.Point(json.loads(self.point))

			updated_geofence = hypertrack.update(
				geofence_id = self.hypertrack_id,
				user_id = frappe.db.get_value("HyperTrack User", self.user_id, "hypertrack_id"),
				geofence_type = self.geofence_type,
				place = place_by_type,
				min_duration = self.min_duration,
				max_duration = self.max_duration,
				expire_at = expire_at
			)


	def on_trash(self):
		hypertrack = HTGeoFence(frappe.db.get_value("HyperTrack Settings",None, "hypertrack_secret_key"))
		hypertrack.delete(self.hypertrack_id)
