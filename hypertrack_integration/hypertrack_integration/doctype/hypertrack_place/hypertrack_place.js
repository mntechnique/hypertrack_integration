// Copyright (c) 2017, MN Technique and contributors
// For license information, please see license.txt

frappe.ui.form.on('HyperTrack Place', {
	onload: function (frm) {
		frm.add_fetch("frappe_address", "city", "city");
		frm.add_fetch("frappe_address", "pincode", "zip_code");
		frm.add_fetch("frappe_address", "state", "state");
		frm.add_fetch("frappe_address", "address_title", "hypertrack_name");
		frm.add_fetch("frappe_address", "country", "country");
	},
	refresh: function(frm) {

	}
});
