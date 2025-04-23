import hash_functions
import net_functions
from socket import *
import threading
from sys import argv, exit

"""
NOTES:
- Command Messages: (All Caps) \n
- PeerAddress: “IP:port” \n
- Hashed Key: str( 160-bit integer) \n
- Acknowledgement: Yes ( 1\n ) or No ( 0\n )
- Integers in general: str ( int ) \n
"""

def getLine(conn: socket):
	"""
	Receive a message from the socket until a newline character is found
	
	NOTE: This will remove the newline character from the message

	@param conn: The socket connection to receive the message from
	"""
	msg = b""
	while True:
		ch = conn.recv(1)
		msg += ch
		if ch == b"\n" or len(ch) == 0:
			break
	return msg.decode()

# local storage of the DHT
dht = {}

# finger table
finger_table: dict[str, str] = {
	"Self" : None,
	"Prev" : None,
	"Next" : None,
	"1" : None,
	"2" : None,
	"3" : None,
	"4" : None,
}

def locate(hashed_key: str):
	"""
	Find the peer that has the hashed_key

	### Protocol:
	- [Self->Peer] LOCATE
	- [Self->Peer] HashedKey
	- [Peer->Self] PeerAddress

	@param hashed_key: The hashed key to locate
	"""
	pass

def recvLocateReq(connInfo: tuple):
	"""
	Receive a locate request from a peer and process it

	### Protocol:
	- [Peer->Self] LOCATE (already received in "handleClient")
	- [Peer->Self] HashedKey
	- [Self->Peer] PeerAddress
	"""
	pass

def connect(peer_address: str):
	"""
	Enter into the DHT and get a "spot" for yourself

	### Protocol:
	- [Self->Peer] CONNECT
	- [Self->Peer] HashedKey (of Self's PeerAddress)
	- [Peer->Self] Acknowledgement if 1, continue on - if 0, bail out of protocol
	- Transfer all entries
		- [Peer->Self] integer numEntries
		- For loop - numEntries times do the following:
		- [Peer->Self] HashKey of entry
		- [Peer->Self] integer len(ValueData)
		- [Peer->Self] byteArray of ValueData
	- [Peer->Self] PeerAddress of it's Next peer
	- Complete Update Prev on Next Node sub-protocol
	- [Self->Peer] selfAddress
	
	*** Ownership Officially Transferred by completing this ***

	@param peer_addr: The address and port of the peer to connect to as <IP:port>
	"""
	# create a socket object given the peer address
	peer_ip, peer_port = peer_address.split(":")
	peer_port = int(peer_port)
	connInfo = socket(AF_INET, SOCK_STREAM)
	connInfo.connect((peer_ip, peer_port))
	# Do the connect protocol
	connInfo.send(b"CONNECT\n")
	connInfo.send(hashedKey.encode())
	ack = getLine(connInfo)
	if ack == "0":
		print("Peer does not own the 'hashed_key' space in DHT.")
		return
	# Begin transfer of all entries
	num_entries = int(getLine(connInfo))
	for _ in range(num_entries):
		entry_hashed_key = getLine(connInfo)
		len_value_data = int(getLine(connInfo))
		value_data = connInfo.recv(len_value_data)
		dht[entry_hashed_key] = value_data
	# Get the next peer address
	next_peer_addr = getLine(connInfo)
	finger_table["Next"] = next_peer_addr # Update the finger table
	# Update the previous peer
	update_prev(next_peer_addr)
	connInfo.send(selfAddress.encode())
	connInfo.close()

def recvConnectReq(connInfo: tuple):
	"""
	Receive a connect request from a new peer and process it

	### Protocol:
	- [Peer->Self] CONNECT (already received in "handleClient")
	- [Peer->Self] HashedKey (of Peer's PeerAddress)
	- [Self->Peer] Acknowledgement if 1, continue on - if 0, bail out of protocol
	- Transfer all entries
		- [Self->Peer] integer numEntries
		- For loop - numEntries times do the following:
			- [Self->Peer] HashKey of entry
			- [Self->Peer] integer len(ValueData)
			- [Self->Peer] byteArray of ValueData
	- [Self->Peer] PeerAddress of it's Next peer
	- Complete Update Prev on Next Node sub-protocol
	- [Self->Peer] PeerAddress of Self
	"""
	peer_hashed_key = getLine(connInfo)
	connInfo.send(b"1\n")  # Acknowledgement
	# Begin transfer of all entries
	num_entries = len(dht)
	connInfo.send(str(num_entries+"\n").encode())
	for key, value in dht.items():
		connInfo.send(str(key+"\n").encode())
		connInfo.send(str(len(value)+"\n").encode())
		connInfo.send(value)
	# Send your next peer address
	connInfo.send((finger_table["Next"]+"\n").encode())
	# The peer does update_prev on next
	connInfo.send(selfAddress.encode())
	connInfo.close()
	# Update the finger table
	finger_table["Next"] = peer_hashed_key

def disconnect():
	"""
	Disconnect from the DHT nicely by transferring ownership of your data to "Prev"

	### Protocol:
	- [Self->Prev] DISCONNECT
	- [Self->Prev] Self's Next PeerAddress
	- Transfer all entries
		- [Self->Prev] integer numEntries
		- For loop - numEntries times do the following:
			- [Self->Prev] HashKey of entry
			- [Self->Prev] integer len(ValueData)
			- [Self->Prev] byteArray of ValueData
	- Prev performs UpdatePrev on Next
	- [Prev->Self] Acknowledgement

	*** Ownership Officially Transferred by completing this ***
	"""
	# create socket object from the finger table
	peer_ip, peer_port = finger_table["Prev"].split(":")
	peer_port = int(peer_port)
	connInfo = socket(AF_INET, SOCK_STREAM)
	connInfo.connect((peer_ip, peer_port))
	# Do the disconnect protocol
	connInfo.send(b"DISCONNECT\n")
	connInfo.send(finger_table["Next"].encode())
	# Transfer all entries
	connInfo.send(str(len(dht)+"\n").encode())
	for key, value in dht.items():
		connInfo.send(key.encode())
		connInfo.send(str(len(value)+"\n").encode())
		connInfo.send(value)
	# Receive acknowledgement
	ack = getLine(connInfo)
	if ack == "0":
		print("DISCONNECT: Something went wrong.")
	print("Exiting...")
	connInfo.close()
	exit(0)

def recvDisconnectReq(connInfo: tuple):
	"""
	Receive a disconnect request from a peer and process it

	### Protocol:
	- [Next->Self] DISCONNECT (already received in "handleClient")
	- [Next->Self] Next's Next PeerAddress (update the finger table)
	- Transfer all entries
		- [Next->Self] integer numEntries
		- For loop - numEntries times do the following:
			- [Next->Self] HashKey of entry
			- [Next->Self] integer len(ValueData)
			- [Next->Self] byteArray of ValueData
	- Prev performs UpdatePrev on Next
	- [Self->Next] Acknowledgement
	"""
	new_next_peer_addr = getLine(connInfo)
	finger_table["Next"] = new_next_peer_addr # Update the finger table
	# Transfer all entries
	num_entries = int(getLine(connInfo))
	for _ in range(num_entries):
		entry_hashed_key = getLine(connInfo)
		len_value_data = int(getLine(connInfo))
		value_data = connInfo.recv(len_value_data)
		dht[entry_hashed_key] = value_data
	# Perform UpdatePrev on Next
	update_prev(new_next_peer_addr)
	connInfo.send(b"1\n")  # Acknowledgement
	connInfo.close()

def update_prev(peer_addr: str):
	"""
	Update your "Next" that you are their new "Prev"

	### Protocol:
	- [Self->Next] UPDATE_PREV
	- [Self->Next] PeerAddress of self
	- [Next->Self] Acknowledgement

	@param peer_addr: The address of the peer to update
	"""
	# create a socket object given the peer address
	peer_ip, peer_port = peer_addr.split(":")
	peer_port = int(peer_port)
	connInfo = socket(AF_INET, SOCK_STREAM)
	connInfo.connect((peer_ip, peer_port))
	# Do the update_prev protocol
	connInfo.send(b"UPDATE_PREV\n")
	connInfo.send(selfAddress.encode())
	ack = getLine(connInfo)
	if ack == "0":
		print("UPDATE_PREV: Something went wrong.")
	else:
		print("UPDATE_PREV: Successfully updated the previous peer.")
	connInfo.close()
	return

def recvUpdatePrevReq(connInfo: tuple):
	"""
	Receive an update request from a peer and process it

	### Protocol:
	- [Peer->Self] UPDATE_PREV (already received in "handleClient")
	- [Peer->Self] PeerAddress of self
	- [Self->Peer] Acknowledgement
	"""
	peer_addr = getLine(connInfo)
	finger_table["Prev"] = peer_addr  # Update the finger table
	connInfo.send(b"1\n")  # Acknowledgement
	connInfo.close()

def contains(hashed_key: str):
	"""
	Ask if the DHT contains the hashed_key, similar to "locate"

	### Protocol:
	- [Self->Peer] CONTAINS
	- [Self->Peer] HashedKey
	- [Peer->Self] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Peer->Self] Acknowledgement of having entry
	
	@param hashed_key: The hashed key to find
	"""
	pass

def recvContainsReq(connInfo: tuple):
	"""
	Receive a contains request from a peer and process it
	
	### Protocol:
	- [Peer->Self] CONTAINS (already received in "handleClient")
	- [Peer->Self] HashedKey
	- [Self->Peer] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Self->Peer] Acknowledgement of having entry
	"""
	pass

def get(hashed_key: str):
	"""
	Ask the DHT for the value associated with the hashed_key
	
	### Protocol:
	- [Self->Peer] GET
	- [Self->Peer] HashedKey
	- [Peer->Self] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Peer->Self] integer len(ValueData)
	- [Peer->Self] byteArray of ValueData

	@param hashed_key: The hashed key to get the value for
	"""
	pass

def recvGetReq(connInfo: tuple):
	"""
	Receive a get request from a peer and process it
	
	### Protocol:
	- [Peer->Self] GET (already received in "handleClient")
	- [Peer->Self] HashedKey
	- [Self->Peer] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Self->Peer] integer len(ValueData)
	- [Self->Peer] byteArray of ValueData
	"""
	pass

def insert(hashed_key: str, value: bytes):
	"""
	Insert data into the DHT
	
	### Protocol:
	- [Self->Peer] INSERT
	- [Self->Peer] HashedKey
	- [Peer->Self] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Self->Peer] integer len(ValueData)
	- [Self->Peer] byteArray of ValueData
	- [Peer->Self] Acknowledgement of successful INSERT

	@param hashed_key: The hashed key to insert the value for
	@param value: The value to insert as a bytearray
	"""
	pass

def recvInsertReq(connInfo: tuple):
	"""
	Receive an insert request from a peer and process it
	
	### Protocol:
	- [Peer->Self] INSERT (already received in "handleClient")
	- [Peer->Self] HashedKey
	- [Self->Peer] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Peer->Self] integer len(ValueData)
	- [Peer->Self] byteArray of ValueData
	- [Self->Peer] Acknowledgement of successful INSERT
	"""
	pass

def remove(hashed_key: str):
	"""
	Remove data from the DHT
	
	### Protocol:
	- [Self->Peer] REMOVE
	- [Self->Peer] HashedKey
	- [Peer->Self] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Peer->Self] Acknowledgement of successful REMOVE
		- Also acknowledge "1\\n" if key didn't exist. Remove didn't fail.
	
	@param hashed_key: The hashed key to remove
	"""
	pass

def recvRemoveReq(connInfo: tuple):
	"""
	Receive a remove request from a peer and process it
	
	### Protocol:
	- [Peer->Self] REMOVE (already received in "handleClient")
	- [Peer->Self] HashedKey
	- [Self->Peer] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Self->Peer] Acknowledgement of successful REMOVE
		- Also acknowledge "1\\n" if key didn't exist. Remove didn't fail.
	"""
	pass

def handleClient(connInfo: tuple):
	"""
	Handle incoming client connections and process commands
	
	### Protocol:
	- [Peer->Self] Command
	- [Self] Do that command function
	"""
	commands = {
		"LOCATE": recvLocateReq,
		"CONNECT": recvConnectReq,
		"DISCONNECT": recvDisconnectReq,
		"UPDATE_PREV": recvUpdatePrevReq,
		"CONTAINS": recvContainsReq,
		"GET": recvGetReq,
		"INSERT": recvInsertReq,
		"REMOVE": recvRemoveReq,
	}

	sock = connInfo[0]
	command = getLine(sock)
	if command in commands:
		print(f"Received command: {command}")
		func = commands[command]
		func(connInfo)
	else:
		print(f"Unknown command: {command}")
	# Close the socket after processing
	sock.close()

# Ensure the program is launched correctly
if len(argv) > 3 or (len(argv) <= 2 and len(argv) != 1):
	print('Incorrect number of arguments\nUsage:\npython3 bvDHT.py <IP> <Port>\
	   \nOR\npython3 bvDHT.py')
	exit(1)

# This is us listening for any incoming connections
listener = socket(AF_INET, SOCK_STREAM)
listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
listener.bind(('', 0))  # Bind to any available port
listener.listen(5)  # Listen for incoming connections
localPort = listener.getsockname()[1]  # Get the port number
localIP = net_functions.getLocalIPAddress()
selfAddress = f"{localIP}:{localPort}\n"
print(f"Listening on {selfAddress}")

hashedKey: str = str(hash_functions.getHashIndex((localIP, localPort))) + "\n"

def start_listen():
	while True:
		try:
			threading.Thread(target=handleClient, args=(listener.accept(), ), daemon=True).start()
		except KeyboardInterrupt:
			listener.close()
			break

# Main code to run the DHT
if len(argv) == 3:
	peer_addr = argv[1:]
	peer_addr = ":".join(peer_addr) # Join the list into a string
	if not connect(peer_addr):
		print("Failed to connect to peer")
		exit(1)
else:
	print("No peer address provided, creating DHT")
# Start listening for incoming connections
threading.Thread(target=start_listen, args=(), daemon=True).start()

commands = ["insert", "get", "remove", "disconnect"]
running = True
while running:
	try:
		command = input("What do?: ").strip().lower()
		match command:
			case "insert":
				pass
			case "get":
				pass
			case "remove":
				pass
			case "disconnect":
				pass
			case _: # This is the default case, catches invalid commands
				print("Invalid command. Please use one of the following:")
				print(commands)
				continue
	except KeyboardInterrupt:
		running = False
		print("Exiting...\n")
		break
