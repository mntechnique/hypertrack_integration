# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.nestedset import NestedSet
from hypertrack_integration.hypertrack_integration.doctype.hypertrack_settings.hypertrack_settings import get_hypertrack 

class HyperTrackGroup(NestedSet):
	nsm_parent_field = "parent_hypertrack_group";
	
	def after_insert(self):
		hypertrack = get_hypertrack()
		new_hypertrack_group = hypertrack.Group.create( \
			name=self.hypertrack_name, \
			parent_group_id = self.parent_hypertrack_group)

	def on_update(self):
		

@frappe.whitelist()
def get_children():
	ctype = frappe.local.form_dict.get('ctype')
	parent_field = 'parent_' + ctype.lower().replace(' ', '_')
	parent = frappe.form_dict.get("parent") or ""

	return frappe.db.sql("""select name as value,
		if(is_group='Yes', 1, 0) as expandable
		from `tab{ctype}`
		where docstatus < 2
		and ifnull(`{parent_field}`,'') = %s
		order by name""".format(ctype=frappe.db.escape(ctype), parent_field=frappe.db.escape(parent_field)),
		parent, as_dict=1)


@frappe.whitelist()
def add_node():
	ctype = frappe.form_dict.get('ctype')
	parent_field = 'parent_' + ctype.lower().replace(' ', '_')
	name_field = ctype.lower().replace(' ', '_') + '_name'

	doc = frappe.new_doc(ctype)
	doc.update({
		name_field: frappe.form_dict['name_field'],
		parent_field: frappe.form_dict['parent'],
		"is_group": frappe.form_dict['is_group']
	})

	doc.save()
	frappe.db.commit()

