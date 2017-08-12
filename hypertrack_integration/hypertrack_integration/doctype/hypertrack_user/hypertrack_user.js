// Copyright (c) 2017, MN Technique and contributors
// For license information, please see license.txt

frappe.ui.form.on('HyperTrack User', {
	onload: function(frm) {
		frm.add_fetch("frappe_user", "full_name", "hypertrack_name");
		frm.add_fetch("frappe_user", "mobile_no", "phone");
		frm.add_fetch("frappe_user", "name", "lookup_id");
		frm.set_query("group_id", function() {
			return {
				filters: [["name", "!=", "All HyperTrack Groups"]]
			}
		})
	},
	refresh: function(frm) {

	},
});
