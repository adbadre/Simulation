# Contract defining the established communication

established_communication: public({patient: address}[address])
setup: int128


@public
def __init__():
    self.setup = 1


@public
def add_communication(_physician: address, _patient: address):
    self.established_communication[_physician] = {
        patient: _patient
    }

