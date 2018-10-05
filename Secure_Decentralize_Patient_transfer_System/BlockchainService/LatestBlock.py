from BlockchainService.ContractFactory import ContractFactory

class LatestBlock:
    __LatestBlock_object = None
    __contract_object = None
    __contract_info=None
    __w3 = None

    @staticmethod
    def get_instance(*args):
        if LatestBlock.__contract_object is None:
            LatestBlock(args[0], args[1])
        return LatestBlock.__LatestBlock_object

    def __init__(self, w3,hospital_accounts):
        LatestBlock.__w3 = w3
        w3.personal.unlockAccount(w3.eth.accounts[0], '')
        with open(
                "C:\\Users\\badre\\OneDrive\\Bureau\\theses\\Secure_Decentralize_Patient_transfer_System\\Blockchain_Contracts\\LatestBlock.sol") as file:
            contract_code = file.read()
        LatestBlock.__contract_info = ContractFactory(contract_code, 'LatestBLock', LatestBlock.__w3.eth.accounts[0], LatestBlock.__w3,hospital_accounts).deploy_contract('')
        LatestBlock.__contract_object = LatestBlock.__w3.eth.contract(address=LatestBlock.__contract_info[0],
                                                        abi=LatestBlock.__contract_info[1])
        LatestBlock.__LatestBlock_object = self

    def set_new_latest_block_address(self, new_address):
        self.__contract_object.functions.set_new_latest_block_address(new_address).transact()

    def set_potential_block_address(self, new_potential_block):
        transaction_hash=self.__contract_object.functions.set_potential_block_address(new_potential_block).transact()
        self.__w3.eth.waitForTransactionReceipt(transaction_hash, timeout=600)

    def get_latest_block_address(self):
        return self.__contract_object.functions.get_latest_block_address().call()

    def get_potential_block_address(self):
        return self.__contract_object.functions.get_potential_block_address().call()

    def __call__(self):
        raise TypeError('Singletons must be accessed through `get_instance()`.')
