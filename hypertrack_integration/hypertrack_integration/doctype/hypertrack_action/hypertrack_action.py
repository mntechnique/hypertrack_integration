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
		new_hypertrack_action = hypertrack.Action.create( \
			name=self.hypertrack_name, \
			parent_group_id = self.parent_hypertrack_group)

	def on_update(self):
		pass

	def on_delete(self):
		pass
