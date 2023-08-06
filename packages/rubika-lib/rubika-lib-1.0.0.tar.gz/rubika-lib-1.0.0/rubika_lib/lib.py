from re import findall
from random import randint, choice
from json import loads, dumps, JSONDecodeError
from requests import post,get
from datetime import datetime
from rubika_lib.encryption import encryption

class client:
	web = {
		"app_name": "Main",
		"app_version" : "4.0.4",
		"platform": "Web",
		"package": "web.rubika.ir",
		"lang_code": "fa"
	} # clients
	android = {
		"app_name" : "Main",
		"app_version" : "2.9.5",
		"platform": "Android",
		"package": "ir.resaneh1.iptv",
		"lang_code": "fa"
	}
		
class Bot:
	def __init__(self, auth):
		self.auth = auth
		if len(self.auth) != 32: print("Your auth is wrong!"); exit()
		print("The Rubika Robot Library began operations\nMade by Shayan Heydari\nstarting...")
		self.enc = encryption(auth)
		
	@staticmethod
	def __getUrl__():
		return "https://messengerg2c64.iranlms.ir/" # return random host
		
	@staticmethod
	def _parse(mode:str, text:str):
		results = []
		if mode.upper() == "HTML":
			realText = text.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","")
			bolds = findall("<b>(.*?)</b>",text)
			italics = findall("<i>(.*?)</i>",text)
			monos = findall("<pre>(.*?)</pre>",text)

			bResult = [realText.index(i) for i in bolds]
			iResult = [realText.index(i) for i in italics]
			mResult = [realText.index(i) for i in monos]

			for bIndex,bWord in zip(bResult,bolds):
				results.append({
					"from_index": bIndex,
					"length": len(bWord),
					"type": "Bold"
				})
			for iIndex,iWord in zip(iResult,italics):
				results.append({
					"from_index": iIndex,
					"length": len(iWord),
					"type": "Italic"
				})
			for mIndex,mWord in zip(mResult,monos):
				results.append({
					"from_index": mIndex,
					"length": len(mWord),
					"type": "Mono"
				})

		elif mode.lower() == "markdown":
			realText = text.replace("**","").replace("__","").replace("`","")
			bolds = findall(r"\*\*(.*?)\*\*",text)
			italics = findall(r"\_\_(.*?)\_\_",text)
			monos = findall("`(.*?)`",text)

			bResult = [realText.index(i) for i in bolds]
			iResult = [realText.index(i) for i in italics]
			mResult = [realText.index(i) for i in monos]

			for bIndex,bWord in zip(bResult,bolds):
				results.append({
					"from_index": bIndex,
					"length": len(bWord),
					"type": "Bold"
				})
			for iIndex,iWord in zip(iResult,italics):
				results.append({
					"from_index": iIndex,
					"length": len(iWord),
					"type": "Italic"
				})
			for mIndex,mWord in zip(mResult,monos):
				results.append({
					"from_index": mIndex,
					"length": len(mWord),
					"type": "Mono"
				})

		return results
		
	def sendMessage(self, chat, text, metadata=[], parse_mode=None, message_id=None):
		""" auth.sendMessage("guid", "your text") """ # send Message To group or Channel Or ...
		try:
			inData = { "method":"sendMessage", "input":{ "object_guid":chat, "rnd":f"{randint(100000,999999999)}", "text":text, "reply_to_message_id":message_id }, "client": client.web }
			if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}
			if parse_mode != None :
				inData["input"]["metadata"] = {"meta_data_parts":Bot._parse(parse_mode, text)}
				inData["input"]["text"] = text.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","") if parse_mode.upper() == "HTML" else text.replace("**","").replace("__","").replace("`","")
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps(inData))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: print("error sendMessage library")
		
	def reciveChatsUpdate(self):
		""" auth.reciveChatsUpdate() """ # Chats Update
		try:
			time_stamp = str(round(datetime.today().timestamp()) - 200)
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"getChatsUpdates", "input":{ "state":time_stamp,}, "client": client.android }))},url=Bot.__getUrl__()).json().get("data_enc"))).get("data").get("chats")
		except: print("error chatsUpdate library")
		
	def reciveMessages(self, guid ,min_id):
		""" auth.reciveMessages("guid", "min_id") """ # Get Group or Channel or pv Messages
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"getMessagesInterval", "input":{ "object_guid":guid, "middle_message_id":min_id },"client": client.web }))},url=Bot.__getUrl__()).json().get("data_enc"))).get("data").get("messages")
		except: print('error getMessages library')
		
	def reciveGroupInfo(self, guid):
		# recive Group Info
		try:
			return loads(self.enc.decrypt(post( json={ "api_version":"5", "auth": self.auth, "data_enc": self.enc.encrypt(dumps({ "method":"getGroupInfo", "input":{ "group_guid": guid, }, "client": client.web }))}, url=Bot.__getUrl__()).json()["data_enc"]))
		except: print("error getGroupInfo library")

	def reciveChannelInfo(self, guidChannel):
		try:
			return loads(self.enc.decrypt(post( json={ "api_version":"5", "auth": self.auth, "data_enc": self.enc.encrypt(dumps({ "method":"getChannelInfo","input":{ "channel_guid": guidChannel,}, "client": client.web }))}, url=Bot.__getUrl__()).json()["data_enc"])) # Get Channel Info, as name or ...
		except: print("error Channel Info Library")
		
	def editMessage(self, message_id, guid, newText):
		try:
			return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"editMessage", "input":{ "message_id": message_id, "object_guid": guid, "text": newText }, "client":{ "app_name":"Main", "app_version":"4.0.4","platform":"Web", "package":"web.rubika.ir", "lang_code":"fa"}}))},url=Bot.__getUrl__())
		except: print("error edit Message Library")
		
	def joinGroup(self, link):
		try:
			link = link[24:]
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"joinGroup","input":{"hash_link": link},"client": client.web}))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: print('Error, group membership failed!')
		
	def leaveGroup(self, group_guid):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"leaveGroup","input":{"group_guid": group_guid},"client": client.web}))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: print('Error, group exit operation failed!')
		
	def updateProfile(self, bio, first_name, last_name):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({"method":"updateProfile","input":{"bio": bio,"first_name": first_name,"last_name": last_name,"updated_parameters": ["first_name", "last_name", "bio"]},"client": client.web}))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: print(" error update Profile library ")
		
	def sendMusic(self, guid, file_id , mime , dc_id,music_performer, time, access_hash_rec, file_name,  size , width , height, text=None, message_id=None):
		try:
			p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({"method":"sendMessage","input":{"object_guid":guid,"rnd":f"{randint(100000,900000)}","text":text,"reply_to_message_id":message_id,"file_inline":{"dc_id":str(dc_id),"file_id":str(file_id),"type":"Music","music_performer":music_performer,"file_name":file_name,"size":size,"time":time, "mime":mime, "access_hash_rec":access_hash_rec, 'width':width, 'height':height}},"client":{ client.android}}))},url=Bot.__getUrl__()).text)['data_enc']))
		except: print("err send Music Library!")
			
	def clearMessages(self, guid, message_ids):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"deleteMessages", "input":{ "object_guid":guid, "message_ids":message_ids,"type":"Global" }, "client": client.web }))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: print('err delete Messages library!')
		
	def reciveUserInfo(self, guid):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"getUserInfo", "input":{ "user_guid": guid }, "client": client.web }))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: print('err recive info user library!')
		
	def reciveInfoByUsername(self, username): # user info without @
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"getObjectByUsername", "input":{ "username":username }, "client": client.web }))},url=Bot.__getUrl__()).json().get("data_enc")))
		except: print("err recive username by info library!")