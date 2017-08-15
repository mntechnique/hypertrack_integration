# see license.txt
import frappe
import requests
import json

class HTApi():
	def __init__(self, sk):
		self.headers = {
			'Authorization': "token " + sk,
			'Content-Type': 'application/json',
		}
		self.group_base_url = 'https://api.hypertrack.com/api/v1/groups/'
		self.geofence_base_url = 'https://api.hypertrack.com/api/v1/geofences/'

class HTGroup(HTApi):
	"""
	API for communicating with HyperTrack Group entity

	:param sk: API Secret Key provided by HyperTrack
	"""
	def create(self, name, parent_group_id=None):
		"""
		Creates Group
		
		:param name: Group name
		:param parent_group_id: Parent Group ID
		"""
		data = {
			"name": name
		}
		if parent_group_id:
			data["parent_group_id"] = parent_group_id

		try:
			response = requests.post(self.group_base_url, headers=self.headers, data=json.dumps(data))
			return response.json()
		except Exception as e:
			raise e

	def retrieve(self, group_uuid):
		"""
		Retrieves Group
		
		:param group_uuid: Group UUID
		"""		
		try:
			response = requests.get(self.group_base_url + group_uuid, headers=self.headers)
			return response.json()
		except Exception as e:
			raise e

	def delete(self, group_uuid):
		"""
		Deletes Group
		
		:param group_uuid: Group UUID
		"""
		try:
			response = requests.delete(self.group_base_url + group_uuid, headers=self.headers)
			return response.text
		except Exception as e:
			raise e

	def list(self):
		"""
		Lists all Groups
		"""
		try:
			response = requests.get(self.group_base_url, headers=self.headers)
			return response.json()
		except Exception as e:
			raise e

	def update(self, group_uuid, changed_group_name):
		"""
		Updates Group
		
		:param group_uuid: Group UUID
		:param changed_group_name: New name for the Group
		"""
		data = {
			"name": changed_group_name
		}
		try:
			response = requests.patch(self.group_base_url + group_uuid, headers=self.headers, data=json.dumps(data))
			return response.json()
		except Exception as e:
			raise e

class HTGeoFence(HTApi):
	"""
	API for communicating with HyperTrack GeoFence entity

	:param sk: API Secret Key provided by HyperTrack
	"""
	def create(self, user_id=None, geofence_type=None, place=None, min_duration=None,
				max_duration=None, expire_at=None):
		"""
		Creates GeoFence
		
		:param user_id: User ID
		:param geofence_type: Type
		:param place: Place
		:param min_duration: Min Duration
		:param max_duration: Max Duration
		:param expire_at: Expire At
		"""
		data = {
			"user_id": user_id,
			"type": geofence_type
		}

		if place:
			data["place"] = place
		if min_duration:
			data["min_duration"] = min_duration
		if max_duration:
			data["max_duration"] = max_duration
		if expire_at:
			data["expire_at"] = expire_at

		try:
			response = requests.post(self.geofence_base_url, headers=self.headers, data=json.dumps(data))
			return response.json()
		except Exception as e:
			raise e

	def retrieve(self, geofence_id):
		"""
		Retrieves GeoFence
		
		:param geofence_id: GeoFence UUID
		"""		
		try:
			response = requests.get(self.geofence_base_url + geofence_id, headers=self.headers)
			return response.json()
		except Exception as e:
			raise e

	def delete(self, geofence_id):
		"""
		Deletes GeoFence
		
		:param geofence_id: Group UUID
		"""
		try:
			response = requests.delete(self.geofence_base_url + geofence_id, headers=self.headers)
			return response.text
		except Exception as e:
			raise e

	def list(self):
		"""
		Lists all GeoFences
		"""
		try:
			response = requests.get(self.geofence_base_url, headers=self.headers)
			return response.json()
		except Exception as e:
			raise e

	def update(self, geofence_id, user_id=None, group_type=None, place=None,
				min_duration=None, max_duration=None, expire_at=None):
		"""
		Updates GeoFence
		
		:param geofence_id: GeoFence UUID
		:param user_id: User ID
		:param group_type: Type
		:param place: Place
		:param min_duration: Min Duration
		:param max_duration: Max Duration
		:param expire_at: Expire At
		"""
		data = {}
		if group_type:
			data["type"] = group_type
		if user_id:
			data["user_id"] = user_id,
		if place:
			data["place"] = place
		if min_duration:
			data["min_duration"] = min_duration
		if max_duration:
			data["max_duration"] = max_duration
		if expire_at:
			data["expire_at"] = expire_at
		try:
			response = requests.patch(self.geofence_base_url + geofence_id, headers=self.headers, data=json.dumps(data))
			return response.json()
		except Exception as e:
			raise e
