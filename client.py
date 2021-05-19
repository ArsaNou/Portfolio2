import requests
import sys
#from tkinter import *

BASE = "http://127.0.0.1:5000/"

#window = Tk()

#window.title("Client")

#window.mainloop()

#action_list = ["get", "put", "delete"]
#resource_list = ["product", "user", "chatroom"]
#index_list = []
#index = 0


#response = requests.put(BASE + "product/0", {"name": "This is name", "price": 100, "colors": 100})
#response = requests.patch(BASE + "product/0", {"price":300})
counter = 2
while True:
	name = input("Name: ")
	price = input("Price: ")
	colors = input("Colors: ")
	response = requests.put(BASE + "product/" + str(counter), {"name": name, "price": price, "colors": colors})
	print(response.json())
	br = input("Break")
	counter += 1
	if br:
		break



"""
while True:

	while True:
		selected_action = input("Action: ").lower()
		if selected_action.lower() == "quit" or selected_action.lower() == "exit":
			sys.exit()
		if selected_action in action_list:
			break
		print("Try again. Available actions:") 
		print(action_list)

	while True:
		selected_resource = input("Resource: ").lower()
		if selected_resource.lower() == "quit" or selected_resource.lower() == "exit":
			sys.exit()
		if selected_resource in resource_list:
			break
		print("Try again. Available resources:")
		print(resource_list)

	# USERS
	
	if selected_resource == 'users':
		if selected_action == 'put':
			while True:
				navn = input("Navn: ")
				alder = int(input("Alder: "))
				stilling = input("Stilling: ")
				response = requests.put(BASE + "/api/users", {"id": 0, "name": navn, "age": alder, "position": stilling})
				print(response)
				print(response.json().values())
				if input("Break? "):
					break
	
		if selected_action == 'get':
			response = requests.get(BASE + "/api/users")
			print(response)
			for elem in response.json():
				print(elem.values())

	# USER

	if selected_resource == 'user':
		if selected_action == 'get':
			while True:
				get_id = int(input("ID: "))
				#try:
				response = requests.get(BASE + f"/api/user/{get_id}")
				print(response)
				print(response.json().values())
				#except:
				#	print("Could not find user...")
				
				break
			#print(response.json())

		if selected_action == 'delete':
			#while True:
			get_id = int(input("ID: "))
				#if get_id in index_list:
				#	break
				#print("Error, no ID given")
			response = requests.delete(BASE + f"/api/user/{get_id}")
			print(response)
			print("User deleted")

	# CHATROOMS

	if selected_resource == 'chatrooms':
		if selected_action == 'put':
			while True:
				navn = input("Navn: ")
				response = requests.put(BASE + "/api/rooms", {"id": 0, "name": navn})
				print(response)
				print(response.json().values())
				if input("Break? "):
					break
	
		if selected_action == 'get':
			response = requests.get(BASE + "/api/rooms")
			print(response)
			for elem in response.json():
				print(elem.values())

	if selected_resource == 'chatroom':
		if selected_action == 'get':
			while True:
				get_id = int(input("ID: "))
				try:
					response = requests.get(BASE + f"/api/user/{get_id}")
					print(response)
					print(response.json().values())
				except:
					print("Could not find user...")
				
				break
			#print(response.json())

		if selected_action == 'delete':
			#while True:
			get_id = int(input("ID: "))
				#if get_id in index_list:
				#	break
				#print("Error, no ID given")
			response = requests.delete(BASE + f"/api/user/{get_id}")
			print(response)
			print("User deleted")

	#if input("Quit?"):
		#break


response = requests.get(BASE + "user/1")
print(response)
print(response.json())

response = requests.delete(BASE + "user/1")
print(response)
print(response.json())
"""