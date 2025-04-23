import hash_functions
import net_functions

"""
NOTES:
- Command Messages: (All Caps) \n
- PeerAddress: “IP:port” \n
- Hashed Key: str( 128-bit integer) \n
- Acknowledgement: Yes ( 1\n ) or No ( 0\n )
- Integers in general: str ( int ) \n
"""

# local storage of the DHT
dht = {}

# finger table
finger_table: dict[str, str] = {}


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
