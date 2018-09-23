from solc import compile_source


class ContractFactory:

    def __init__(self, contract_file_content, contract_name, account, w3):
        self.contract = None
        self.contract_code = str(contract_file_content)
        self.contract_name = contract_name
        self.contract_interface = None
        self.w3 = w3
        self.compiled_contract = None
        self.public_address = account
        self.transaction_hash = None
        self.transaction_receipt = None
        self.contract_object = None
        self.hospital_accounts = [self.w3.eth.accounts[0], self.w3.eth.accounts[1], self.w3.eth.accounts[2]]

    def compile_contract(self):
        self.compiled_contract = compile_source(self.contract_code)
        print(" Contract Compiled")

    def contract_interfacer(self):
        self.contract_interface = self.compiled_contract['<stdin>:' + str(self.contract_name)]

    def account_unlocking(self, password):
        self.w3.eth.defaultAccount = self.public_address
        self.w3.personal.unlockAccount(self.public_address, str(password))

    def send_contract_on_blockchain(self, hospital_address):
        self.contract = self.w3.eth.contract(abi=self.contract_interface['abi'],
                                             bytecode=self.contract_interface['bin'])
        self.transaction_hash = self.contract.constructor(hospital_address).transact()
        self.transaction_receipt = self.w3.eth.waitForTransactionReceipt(self.transaction_hash, timeout=600)
        print("Contract Mined")

    def instantiate_contract_object(self):
        self.contract_object = self.w3.eth.contract(address=self.transaction_receipt.contractAddress,
                                                    abi=self.contract_interface['abi'])

    def deploy_contract(self, password):
        self.compile_contract()
        self.contract_interfacer()
        self.account_unlocking(password)
        self.send_contract_on_blockchain(self.hospital_accounts)
        return [self.transaction_receipt.contractAddress, self.contract_interface['abi']]


