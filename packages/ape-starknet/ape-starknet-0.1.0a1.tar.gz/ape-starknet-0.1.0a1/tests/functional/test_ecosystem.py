import pytest
from ape.types import AddressType
from eth_typing import HexAddress, HexStr
from hexbytes import HexBytes

INT_ADDRESS = 14543129564252315649550252856970912276603599239311963926081534426621736121411
STR_ADDRESS = "0x20271ea04cB854E105d948019Ba1FCdFa61d76D73539700Ff6DD456bcB7bF443"
HEXBYTES_ADDRESS = HexBytes(STR_ADDRESS)
EVENT_NAME = "balance_increased"


@pytest.fixture
def raw_logs():
    return [
        {
            "data": ["0", "4321"],
            "from_address": "0x14acf3b7e92f97adee4d5359a7de3d673582f0ce03d33879cdbdbf03ec7fa5d",
            "keys": [
                "1744303484486821561902174603220722448499782664094942993128426674277214273437"
            ],
        }
    ]


@pytest.fixture
def event_abi_dict():
    return {
        "type": "event",
        "name": "Upgraded",
        "inputs": [{"name": "implementation", "type": "felt", "indexed": False}],
    }


@pytest.mark.parametrize("value", (INT_ADDRESS, STR_ADDRESS, HEXBYTES_ADDRESS))
def test_encode_and_decode_address(value, ecosystem):
    decoded_address = ecosystem.decode_address(value)
    expected = AddressType(HexAddress(HexStr(STR_ADDRESS)))
    assert decoded_address == expected

    # The values should _always_ encode back to the INT_ADDRESS.
    re_encoded_address = ecosystem.encode_address(decoded_address)
    assert re_encoded_address == INT_ADDRESS


def test_decode_logs(ecosystem, event_abi_dict, raw_logs):
    actual = [log for log in ecosystem.decode_logs(event_abi_dict, raw_logs)]
    assert len(actual) == 1
