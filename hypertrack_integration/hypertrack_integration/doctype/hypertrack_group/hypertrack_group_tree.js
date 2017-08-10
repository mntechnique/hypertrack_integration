frappe.treeview_settings["HyperTrack Group"] = {
	breadcrumbs: "HyperTrack Integration",
	get_tree_root: false,
	root_label: "All HyperTrack Groups",
	get_tree_nodes: 'hypertrack_integration.doctype.hypertrack_group.hypertrack_group.get_children',
	add_tree_node: 'hypertrack_integration.doctype.hypertrack_group.hypertrack_group.add_node',
	fields:[
		{fieldtype:'Data', fieldname:'hypertrack_group_name', label:__('New HyperTrack Group Name'), reqd:true},
		{fieldtype:'Check', fieldname:'is_group', label:__('Is Group'),
			description:__('Further HyperTrack can be made under Groups but entries can be made against non-Groups')}
	],
	ignore_fields:["parent_hypertrack_group"]
}