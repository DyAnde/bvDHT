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
	"Peer1" : None,
	"Peer2" : None,
	"Peer3" : None,
	"Peer4" : None,
}


def locate(hashed_key: str) -> str:
	"""
	Find the peer that has the hashed_key

	### Protocol:
	- [Self->Peer] LOCATE
	- [Self->Peer] HashedKey
	- [Peer->Self] PeerAddress

	@param hashed_key: The hashed key to locate
	@return: The peer that has ownership of the hashed_key
	"""
	pass

def recvLocateReq(connInfo: tuple) -> str:
	"""
	Receive a locate request from a peer and process it

	### Protocol:
	- [Peer->Self] LOCATE (already received in "handleClient")
	- [Peer->Self] HashedKey
	- [Self->Peer] PeerAddress

	@return: The peer that has ownership of the hashed_key
	"""
	pass

def connect(peer_addr: str) -> bool:
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
	- [Self->Peer] PeerAddress of Self
	
	*** Ownership Officially Transferred by completing this ***

	@param peer_addr: The address of the peer to connect to
	@return: True if connected, False otherwise
	"""
	pass

def recvConnectReq(connInfo: tuple) -> bool:
	"""
	Receive a connect request from a peer and process it

	### Protocol:
	- [Peer->Self] CONNECT (already received in "handleClient")
	- [Peer->Self] HashedKey (of Self's PeerAddress)
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

	@return: True if connected, False otherwise
	"""
	pass

def disconnect() -> None:
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
	pass

def recvDisconnectReq(connInfo: tuple) -> None:
	"""
	Receive a disconnect request from a peer and process it

	### Protocol:
	- [Peer->Self] DISCONNECT (already received in "handleClient")
	- [Peer->Self] Peer's Next PeerAddress
	- Transfer all entries
		- [Peer->Self] integer numEntries
		- For loop - numEntries times do the following:
			- [Peer->Self] HashKey of entry
			- [Peer->Self] integer len(ValueData)
			- [Peer->Self] byteArray of ValueData
	- Prev performs UpdatePrev on Next
	- [Self->Peer] Acknowledgement

	@return: None
	"""
	pass

def update_prev(peer_addr: str) -> bool:
	"""
	Update your "Next" that you are their new "Prev"

	### Protocol:
	- [Self->Next] UPDATE_PREV
	- [Self->Next] PeerAddress of self
	- [Next->Self] Acknowledgement

	@param peer_addr: The address of the peer to update
	@return: True if updated, False otherwise
	"""
	pass

def recvUpdatePrevReq(connInfo: tuple) -> bool:
	"""
	Receive an update request from a peer and process it

	### Protocol:
	- [Peer->Self] UPDATE_PREV (already received in "handleClient")
	- [Peer->Self] PeerAddress of self
	- [Self->Peer] Acknowledgement

	@param peer_addr: The address of the peer to update
	@return: True if updated, False otherwise
	"""
	pass

def contains(hashed_key: str) -> bool:
	"""
	Ask if the DHT contains the hashed_key, similar to "locate"

	### Protocol:
	- [Self->Peer] CONTAINS
	- [Self->Peer] HashedKey
	- [Peer->Self] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Peer->Self] Acknowledgement of having entry
	
	@param hashed_key: The hashed key to find
	@return: True if the hashed_key exists, False otherwise
	"""
	pass

def recvContainsReq(connInfo: tuple) -> bool:
	"""
	Receive a contains request from a peer and process it
	
	### Protocol:
	- [Peer->Self] CONTAINS (already received in "handleClient")
	- [Peer->Self] HashedKey
	- [Self->Peer] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Self->Peer] Acknowledgement of having entry

	@return: True if the hashed_key exists, False otherwise
	"""
	pass

def get(hashed_key: str) -> bool:
	"""
	Ask the DHT for the value associated with the hashed_key
	
	### Protocol:
	- [Self->Peer] GET
	- [Self->Peer] HashedKey
	- [Peer->Self] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Peer->Self] integer len(ValueData)
	- [Peer->Self] byteArray of ValueData

	@param hashed_key: The hashed key to get the value for
	@return: True if the value was retrieved, False otherwise
	"""
	pass

def recvGetReq(connInfo: tuple) -> bool:
	"""
	Receive a get request from a peer and process it
	
	### Protocol:
	- [Peer->Self] GET (already received in "handleClient")
	- [Peer->Self] HashedKey
	- [Self->Peer] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Self->Peer] integer len(ValueData)
	- [Self->Peer] byteArray of ValueData

	@return: True if the value was retrieved, False otherwise
	"""
	pass

def insert(hashed_key: str, value: bytes) -> bool:
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
	@return: True if the value was inserted, False otherwise
	"""
	pass

def recvInsertReq(connInfo: tuple) -> bool:
	"""
	Receive an insert request from a peer and process it
	
	### Protocol:
	- [Peer->Self] INSERT (already received in "handleClient")
	- [Peer->Self] HashedKey
	- [Self->Peer] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Peer->Self] integer len(ValueData)
	- [Peer->Self] byteArray of ValueData
	- [Self->Peer] Acknowledgement of successful INSERT

	@return: True if the value was inserted, False otherwise
	"""
	pass

def remove(hashed_key: str) -> bool:
	"""
	Remove data from the DHT
	
	### Protocol:
	- [Self->Peer] REMOVE
	- [Self->Peer] HashedKey
	- [Peer->Self] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Peer->Self] Acknowledgement of successful REMOVE
		- Also acknowledge "1\\n" if key didn't exist. Remove didn't fail.
	
	@param hashed_key: The hashed key to remove
	@return: True if the value was removed, False otherwise
	"""
	pass

def recvRemoveReq(connInfo: tuple) -> bool:
	"""
	Receive a remove request from a peer and process it
	
	### Protocol:
	- [Peer->Self] REMOVE (already received in "handleClient")
	- [Peer->Self] HashedKey
	- [Self->Peer] Acknowledgement of ownership of HashedKey Space Bail out if answer is "0\\n"
	- [Self->Peer] Acknowledgement of successful REMOVE
		- Also acknowledge "1\\n" if key didn't exist. Remove didn't fail.
	
	@return: True if the value was removed, False otherwise
	"""
	pass

def handleClient(connInfo: tuple) -> None:
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
if len(argv) > 2:
	print('Too many arguments\nUsage:\npython3 bvDHT.py <IP>:<Port>\
	   \nOR\npython3 bvDHT.py')
	exit(1)
elif len(argv) == 2:
	if ":" not in argv[1]:
		print('Invalid argument\nUsage:\npython3 bvDHT.py <IP>:<Port>\
		   \nOR\npython3 bvDHT.py')
		exit(1)

# This is us listening for any incoming connections
listener = socket(AF_INET, SOCK_STREAM)
listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
listener.bind(('', 0))  # Bind to any available port
listener.listen(5)  # Listen for incoming connections
localPort = listener.getsockname()[1]  # Get the port number
localIP = net_functions.getLocalIPAddress()
print(f"Listening on {localIP}:{localPort}")

hashedPosition = hash_functions.getHashIndex((localIP, localPort))

def run():
	"""
	Main function to run the DHT
	"""
	if len(argv) == 2:
		peer_addr = argv[1]
		if not connect(peer_addr):
			print("Failed to connect to peer")
			exit(1)
	else:
		print("No peer address provided, creating DHT")
	running = True
	while running:
		try:
			commands = ["insert", "get", "remove", "disconnect"]
			command = input("What do?: ").lower()
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
			print("Shutting down...")
			running = False
			break

threading.Thread(target=run, args=(), daemon=True).start()

while True:
	try:
		threading.Thread(target=handleClient, args=(listener.accept(), ), daemon=True).start()
	except KeyboardInterrupt:
		print("Shutting down...")
		listener.close()
		break