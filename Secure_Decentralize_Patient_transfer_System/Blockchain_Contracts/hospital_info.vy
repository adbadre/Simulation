# Contract defining the service in hospitals

hospital_service: public({hospital: bytes[25], service: bytes[25]}[address])
manager: address


@public
def __init__(_manager: address):
    self.manager = _manager


@public
def add_physician(_physician: address, _hospital: bytes[25], _service: bytes[25]):
    assert msg.sender == self.manager
    self.hospital_service[_physician] = {
        hospital: _hospital,
        service: _service
    }


@public
def remove_physician(_physician: address):
    assert msg.sender == self.manager
    self.hospital_service[_physician] = None


@public
def change_manager(new_manager: address):
    assert msg.sender == self.manager
    self.manager = new_manager