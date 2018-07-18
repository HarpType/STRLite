# _*_ coding: utf-8 _*_

import os
ros_pkg_path = os.path.join(os.path.dirname(__file__), '../../')


config = {
	'manager_config': {
		'subscribes': {
			'create_world': 'create_world',
			'destroy_world': 'destroy_world'
			},
		'name': 'world_manager',
		'rate': 1
	},

	'launch_paths': {
		'env': {
			'package': 'estr_nodes',
			'executable': 'env_run.py'
		},

		'RTS': {
			'package': 'estr_nodes',
			'r': 'r.py'
		}
	}
}
