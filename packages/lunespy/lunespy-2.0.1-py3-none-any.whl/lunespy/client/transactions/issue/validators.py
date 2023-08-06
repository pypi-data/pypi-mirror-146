from lunespy.client.account import Wallet


def mount_issue(sender: Account, issue_data: dict) -> dict:
    from lunespy.client.transactions.constants import IssueType
    from lunespy.utils.crypto.converters import string_to_bytes
    from lunespy.utils.crypto.converters import sign
    from lunespy.utils import now
    from base58 import b58decode
    import struct

    timestamp: int = issue_data.get('timestamp', now())
    fee: int = issue_data.get('fee', IssueType.fee.value)
    reissuable: bool = issue_data.get('reissuable', False)
    description: str = issue_data.get('description', '')
    timestamp: int = issue_data.get('timestamp', now())
    quantity: int = issue_data.get('quantity', 0)
    decimals: str = issue_data.get('decimals', 0)
    name: str = issue_data.get('name', '')

    bytes_data: bytes = IssueType.to_byte.value + \
        b58decode(sender.public_key) + \
        struct.pack(">H", len(name)) + \
        string_to_bytes(name) + \
        struct.pack(">H", len(description)) + \
        string_to_bytes(description) + \
        struct.pack(">Q", quantity) + \
        struct.pack(">B", decimals) + \
        (b'\1' if reissuable else b'\0') + \
        struct.pack(">Q", fee) + \
        struct.pack(">Q", timestamp)

    signature: bytes = sign(sender.private_key, bytes_data)
    mount_tx = {
        "type": IssueType.to_int.value,
        "senderPublicKey": sender.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": fee,

        "description": description,
        "reissuable": reissuable,
        "decimals": decimals,
        "quantity": quantity,
        "name": name
    }
    return mount_tx


def validate_issue(sender: Account, issue_data: dict) -> bool:
    from lunespy.utils import bcolors

    quantity: int = issue_data.get('quantity', -1)
    name: str = issue_data.get('name', '')

    if not sender.private_key:
        print(bcolors.FAIL + 'Creator `Account` not have a private key' + bcolors.ENDC)
        return False

    if quantity < 0:
        print(bcolors.FAIL + 'To Issue the `quantity` cannot be less than 0' + bcolors.ENDC)
        return False

    if len(name) not in range(4, 16 + 1):
        print(bcolors.FAIL + 'Asset name must be between 4 and 16 characters long' + bcolors.ENDC)
        return False

    return True


# todo async
def send_issue(mount_tx: dict, node_url: str) -> dict:
    from requests import post

    response = post(
        f'{node_url}/transactions/broadcast',
        json=mount_tx,
        headers={
            'content-type':
            'application/json'
        })

    if response.status_code in range(200, 300):
        mount_tx.update({
            'send': True,
            'response': response.json()
        })
        return mount_tx
    else:
        mount_tx.update({
            'send': False,
            'response': response.text
        })
        return mount_tx
