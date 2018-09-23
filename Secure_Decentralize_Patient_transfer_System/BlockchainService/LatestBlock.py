from web3 import Web3


class LatestBlock:
    __LatestBlock_object = None
    __contract_object = None
    __w3 = None

    @staticmethod
    def get_instance(*args):
        if LatestBlock.__contract_object is None:
            print(args[0], args[1])
            LatestBlock(args[0], args[1], args[2])
        return LatestBlock.__LatestBlock_object

    def __init__(self, address, abi, w3):
        LatestBlock.__w3 = w3
        LatestBlock.__contract_object = w3.eth.contract(address=address, abi=abi)
        LatestBlock.__LatestBlock_object = self

    def set_new_address(self, new_address):
        self.__w3.eth.waitForTransactionReceipt(self.__contract_object.functions
                                                .set_new_address(new_address).transact())

    def get_new_address(self):
        return self.__contract_object.functions.get_new_address().call()

    def __call__(self):
        raise TypeError('Singletons must be accessed through `get_instance()`.')
