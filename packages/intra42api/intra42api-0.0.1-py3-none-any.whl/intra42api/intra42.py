from typing import Union
import requests

class Intra42:
	def __init__(self):
		self.token = ''

	def setToken(self, uid: str, secret: str) -> dict:
		response = requests.post("https://api.intra.42.fr/oauth/token", data={
			"grant_type": "client_credentials",
			"client_id": uid,
			"client_secret": secret
		})
		self.token = response.json()
	
	def getUser(self, id: str) -> Union[dict, list]:
		response = requests.get(f"https://api.intra.42.fr/v2/users/{id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getCoalition(self, coalition_id: str) -> Union[dict, list]:
		response = requests.get(f"https://api.intra.42.fr/v2/coalitions/{coalition_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getCoalitionUsers(self, coalition_id: str) -> list:
		response = requests.get(f"https://api.intra.42.fr/v2/coalitions/{coalition_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())
	
	def getCampus(self, campus_id: str) -> Union[dict, list]:
		campus_id = campus_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/campus/{campus_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getCampusUsers(self, campus_id: str) -> list:
		campus_id = campus_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/campus/{campus_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())
		
	def getCursus(self, cursus_id: str) -> Union[dict, list]:
		cursus_id = cursus_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/cursus/{cursus_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getCursusUsers(self, cursus_id: str) -> list:
		cursus_id = cursus_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/cursus/{cursus_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())
	
	def getAchievement(self, achievement_id: str) -> Union[dict, list]:
		achievement_id = achievement_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/achievements/{achievement_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getAchievementUsers(self, achievement_id: str) -> list:
		achievement_id = achievement_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/achievements/{achievement_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getGroup(self, group_id: str) -> Union[dict, list]:
		group_id = group_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/groups/{group_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getGroupUsers(self, group_id: str) -> list:
		group_id = group_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/groups/{group_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getDash(self, dash_id: str) -> Union[dict, list]:
		dash_id = dash_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/dashes/{dash_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getDashUsers(self, dash_id: str) -> list:
		dash_id = dash_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/dashes/{dash_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getAccreditation(self, accreditation_id: str) -> Union[dict, list]:
		accreditation_id = accreditation_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/accreditations/{accreditation_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())
	
	def getAccreditationUsers(self, accreditation_id: str) -> list:
		accreditation_id = accreditation_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/accreditations/{accreditation_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getEvent(self, event_id: str) -> Union[dict, list]:
		event_id = event_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/events/{event_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())
	
	def getEventUsers(self, event_id: str) -> list:
		event_id = event_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/events/{event_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getProject(self, project_id: str) -> Union[dict, list]:
		project_id = project_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/projects/{project_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getProjectUsers(self, project_id: str) -> list:
		project_id = project_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/projects/{project_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())
	
	def getPartnership(self, partnership_id: str) -> Union[dict, list]:
		partnership_id = partnership_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/partnerships/{partnership_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getPartnershipUsers(self, partnership_id: str) -> list:
		partnership_id = partnership_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/partnerships/{partnership_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())

	def getExpertise(self, expertise_id: str) -> Union[dict, list]:
		expertise_id = expertise_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/expertises/{expertise_id}", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())
	
	def getExpertiseUsers(self, expertise_id: str) -> Union[dict, list]:
		expertise_id = expertise_id.lower()
		response = requests.get(f"https://api.intra.42.fr/v2/expertises/{expertise_id}/users", headers={
			"Authorization": self.token['token_type'] + ' ' + self.token['access_token']
		})
		return (response.json())
