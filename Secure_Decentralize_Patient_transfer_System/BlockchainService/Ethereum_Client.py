from web3 import Web3
from solc import compile_source


class EthereumClient:

    def __init__(self, contract_file_content, contract_name):
        self.contract = None
        self.contract_code = str(contract_file_content)
        self.contract_name = contract_name
        self. contract_interface = None
        self.w3 = Web3(Web3.IPCProvider('\\\\.\\pipe\\geth.ipc'))
        self.compiled_contract = None
        self.public_address = self.w3.eth.accounts[0]
        self.transaction_hash = None
        self.transaction_receipt = None
        self.contract_object = None

    def compile_contract(self):
        self.compiled_contract = compile_source(self.contract_code)
        print(" Contract Compiled")

    def contract_interfacer(self):
        self.contract_interface=self.compiled_contract['<stdin>:'+str(self.contract_name)]

    def account_unlocking(self,password):
        self.w3.eth.defaultAccount=self.public_address
        self.w3.personal.unlockAccount(self.public_address, str(password))

    def send_contract_on_blockchain(self,hospital_address):
        self.contract= self.w3.eth.contract(abi=self.contract_interface['abi'],
                                            bytecode=self.contract_interface['bin'])
        self.transaction_hash=self.contract.constructor([hospital_address]).transact()
        self.transaction_receipt = self.w3.eth.waitForTransactionReceipt(self.transaction_hash, timeout=600)
        print("Contract Mined")

    def instanciate_contract_object(self):
        self.contract_object = self.w3.eth.contract(address=self.transaction_receipt.contractAddress,
                                                    abi=self.contract_interface['abi'])

    def deploy_contract(self, password):
        self.compile_contract()
        self.contract_interfacer()
        self.account_unlocking(password)
        self.send_contract_on_blockchain(self.public_address)
        self.instanciate_contract_object()
        return self.contract_object


if __name__ == "__main__":
    with open("C:\\Users\\badre\\OneDrive\\Bureau\\theses\\Secure_Decentralize_Patient_transfer_System\\Blockchain_Contracts\\LatestBlock.sol") as file:
        contact_code = file.read()
    contract = EthereumClient(contact_code, 'LatestBLock')
    cc=contract.deploy_contract('')
    w3= Web3(Web3.IPCProvider('\\\\.\\pipe\\geth.ipc'))
    w3.eth.defaultAccount = w3.eth.accounts[1]
    w3.personal.unlockAccount(w3.eth.accounts[1], '')
    hash=cc.functions.set_new_address(w3.eth.accounts[0]).transact({'from':str(w3.eth.accounts[1]),'gas':210000})
    w3.eth.waitForTransactionReceipt(hash)
    print(cc.functions.get_new_address().call())
    print(contract)


