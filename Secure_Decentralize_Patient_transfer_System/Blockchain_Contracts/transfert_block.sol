pragma solidity ^0.4.24;

contract transfert_block{

    struct Ambulance_Cost_Struct{
       address hospital;
        bytes32 cost ;
    }

    struct Cost_Struct{
        uint128 service;
        bytes32 cost;
    }

    address previous_block;
    address miner_rewarded;
    event ReadyForMining(string message);
    event TransactionMined(string message);


    mapping(address => bool) hospital_address_real;
    address[] hospital_address_tab_real;

    mapping(address => bool) hospital_address;
    address[] hospital_address_tab;

    mapping(uint128 => bool) patients;
    uint128[] patients_tab;

    mapping(uint128 => bool) physicians;
    uint128[] physicians_tab;

    mapping (uint128 => Ambulance_Cost_Struct) ambulance_cost;

    mapping (uint128 => uint128) number_of_patient_per_physician;

    mapping (uint128 => uint128) severity_of_illness;

    mapping (uint128 => uint128[]) patient_matched_physician;

    mapping (address => Cost_Struct) cost_of_loosing_patient;

    constructor(address[] new_hospital_address_tab_real) public {
        hospital_address_tab_real=new_hospital_address_tab_real;
        for(uint16 i=0;i<hospital_address_tab_real.length;i++){
            hospital_address[hospital_address_tab_real[i]]=true;
        }
    }

    function add_hospital(address new_hospital_for_transaction) public{
        require(hospital_address_real[new_hospital_for_transaction]);
        hospital_address_real[new_hospital_for_transaction]=true;
        hospital_address_tab_real.push(new_hospital_for_transaction);
        if(hospital_address_tab_real.length==hospital_address_tab.length){
            emit ReadyForMining("Contract Filled");
        }
    }

    function add_patient(uint128 patient_id) public{
        require(hospital_address_real[msg.sender]);
        patients[patient_id]=true;
        patients_tab.push(patient_id);
    }

    function add_physician(uint128 physician_id) public{
        require(hospital_address_real[msg.sender]);
        physicians[physician_id]=true;
        physicians_tab.push(physician_id);
    }

    function set_ambulance_cost(uint128 patient_id, address hospital, bytes32 cost)public {
       require(patients[patient_id]);
        ambulance_cost[patient_id]=Ambulance_Cost_Struct(hospital,cost);
    }

    function set_number_of_patient_per_physician(uint128 physician,uint128 number) public{
        require(hospital_address[msg.sender]);
        number_of_patient_per_physician[physician]=number;
    }

    function set_patient_matched_physician(uint128 patient,uint128[] physicians_matched)public {
          require(hospital_address_real[msg.sender]);
          patient_matched_physician[patient]=physicians_matched;
    }

    function set_cost_of_loosing_patient(uint128 service,bytes32 cost) public{
        require(hospital_address_real[msg.sender]);
        cost_of_loosing_patient[msg.sender]=Cost_Struct(service,cost);
    }

    function get_patients() public constant returns(uint128[]){
       return patients_tab;
    }

    function get_hospitals() public constant returns(address[]){
       return hospital_address_tab;
    }

   function get_physician() public constant returns(uint128[]){
       return patients_tab;
    }


    function get_ambulance_cost_by_id(uint128 patiend_id) public constant returns(address hospital,bytes32 cost){
       hospital=ambulance_cost[patiend_id].hospital;
       cost=ambulance_cost[patiend_id].cost;
    }

    function get_cost_of_loosing_patient_by_address(address hospital) public constant returns(uint128 service,bytes32 cost){
       service=cost_of_loosing_patient[hospital].service;
       cost=cost_of_loosing_patient[hospital].cost;
    }

    function get_number_of_patient_per_physician_by_id(uint128 physician_id) public constant returns(uint128){
       return number_of_patient_per_physician[physician_id];
    }

    function get_severity_of_illness_by_id(uint128 patiend_id) public constant returns(uint128){
       return severity_of_illness[patiend_id];
    }

    function get_number_of_patient_matched_physician_by_id(uint128 patiend_id) public constant returns(uint128[]){
       return patient_matched_physician[patiend_id];
    }

    function solution_filled(){
        emit TransactionMined("Solution Mined");
    }

}