from Simulation.BlockChainGenesis import BlockchainGenesis
from web3 import Web3
from Data_Manager.SystemInfo import HospitalInfo
from BlockchainService.TransfertBlock import TransfertBlock
from BlockchainService.ContractFactory import ContractFactory

class Simulation:

    def __init__(self):
        self.w3=Web3(Web3.IPCProvider('\\\\.\\pipe\\geth.ipc'))
        self.genesis = None
        self.LatestBlock = None
        self.PhysicianHospitalService = None
        self.SystemInfo= HospitalInfo(self.w3)

    def init_simulation(self):
        self.w3.personal.unlockAccount(self.w3.eth.accounts[0], '')
        self.genesis = BlockchainGenesis().genesis(self.w3, self.SystemInfo)
        self.LatestBlock = self.genesis['latest_block']
        self.PhysicianHospitalService = self.genesis['physician_hospital_service']

    def transfert_block_generation(self):
        with open(
                "C:\\Users\\badre\\OneDrive\\Bureau\\theses\\Secure_Decentralize_Patient_transfer_System\\Blockchain_Contracts\\TransfertBlock.sol") as file:
            contract_code = file.read()
        contract = ContractFactory(contract_code, 'TransfertBlock', self.w3.eth.accounts[0], self.w3)
        contract_info = contract.deploy_contract('')
        return TransfertBlock(contract_info[0], contract_info[1], self.w3)
