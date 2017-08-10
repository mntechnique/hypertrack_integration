# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.nestedset import NestedSet
from hypertrack_integration.hypertrack_integration.doctype.hypertrack_settings.hypertrack_settings import get_hypertrack 

class HyperTrackGroup(NestedSet):
	nsm_parent_field = "parent_hypertrack_group"
	
	def after_insert(self):
		hypertrack = get_hypertrack()
		new_hypertrack_group = hypertrack.Group.create( \
			name=self.hypertrack_name, \
			parent_group_id = self.parent_hypertrack_group)

	def on_update(self):
		hypertrack = get_hypertrack()
		group = hypertrack.Group.retrieve(self.hypertrack_id)
		
		if self.hypertrack_group_name:
			group.name = self.hypertrack_group_name
		group.save()

	def on_delete(self):
		hypertrack = get_hypertrack()
		group = hypertrack.Group.delete()
