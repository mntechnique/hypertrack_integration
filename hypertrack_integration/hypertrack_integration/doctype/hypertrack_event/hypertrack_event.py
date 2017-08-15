# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document

class HyperTrackEvent(Document):
	pass

@frappe.whitelist(allow_guest=True)
def events_hook(*args, **kwargs):
	data = json.loads(kwargs.get("data"))
	ht_event = frappe.new_doc("HyperTrack Event")
	ht_user = frappe.db.get_value("HyperTrack User", {"hypertrack_id":data.get("user_id")}, "name")

	if not ht_user:
		raise Exception("HyperTrack User not found")

	ht_event.hypertrack_user = ht_user
	ht_event.hypertrack_id = data.get("id")
	ht_event.event_type = data.get("type")
	ht_event.recorded_at = data.get("recorded_at")
	ht_event.hypertrack_data = json.dumps(data.get("data"))
	ht_event.created_at = data.get("created_at")

	# ht_event.has_been_delivered = data.get("has_been_delivered")
	# ht_event.delivered_at = data.get("delivered_at")
	# ht_event.modified_at = data.get("modified_at")

	ht_event.save(ignore_permissions=True)
	frappe.db.commit()

	return ht_event
