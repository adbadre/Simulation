pragma solidity ^0.4.24;

contract PhysicianHospitalServiceContract{

    mapping(uint128 => bool) physicians;
    uint128[] physicians_tab;

    mapping(address => bool) hospital_address;
    address[] hospital_address_tab;

    uint128[] subsample;

    mapping(address=> uint128[]) hospital_service;

    mapping (address => mapping(uint128 => uint128[])) physician_hospital_service;

    mapping(address => uint128) number_of_bed_per_hospital;

    mapping (uint128 => uint128) number_of_patient_per_physician;

    constructor(address[] new_hospital_address_tab) public {
        hospital_address_tab=new_hospital_address_tab;
        for(uint16 i=0;i<hospital_address_tab.length;i++){
            hospital_address[hospital_address_tab[i]]=true;
        }
    }

    function set_physicians_tab(uint128[] new_physicians_tab) public{
        assert(hospital_address[msg.sender]);
        physicians_tab=new_physicians_tab;
        for(uint16 i=0;i<physicians_tab.length;i++){
           physicians[physicians_tab[i]]=true;
        }
    }

    function set_number_of_patient_per_physician(uint128 physician,uint128 number) public{
        require(hospital_address[msg.sender]);
        number_of_patient_per_physician[physician]=number;
    }

    function set_number_of_bed_per_hospital( address hospital,uint128 number_of_bed) public{
        assert(hospital_address[msg.sender]);
        number_of_bed_per_hospital[hospital]=number_of_bed;
    }

    function set_hospital_service( address hospital, uint128[] id_service) public{
        assert(hospital_address[msg.sender]);
        hospital_service[hospital]=id_service;
    }

    function set_hospital_service_physician(uint128[] physician, address hospital, uint128 id_service) public{
        assert(hospital_address[hospital]);
        physician_hospital_service[hospital][id_service]=physician;
    }

    function delete_hospital_service( address hospital, uint128 id_service) public{
        assert(hospital_address[hospital]);
        delete physician_hospital_service[hospital][id_service];
    }

    function get_physicians_tab() public constant returns(uint128[]){
        return physicians_tab;
    }

    function get_physician_service_hospital_by_hospital(address hospital,uint128 id_service) public constant
    returns(uint128[]){
        return physician_hospital_service[hospital][id_service];
    }

     function get_physician_service_hospital_by_service(uint128 id_service) public
    returns(uint128[]){
        delete subsample;
        for (uint128 i=0; i<hospital_address_tab.length; i++){
            if(hospital_service[hospital_address_tab[i]][id_service]==1){
                for(uint128 k=0;k<physician_hospital_service[hospital_address_tab[i]][id_service].length;k++){
                    if(physician_hospital_service[hospital_address_tab[i]][id_service][k]==1){
                        subsample.push(k);
                    }
                }
            }
        }
        return subsample;
    }

    function get_hospital_service(address hospital) public constant returns(uint128[]){
        return hospital_service[hospital];
    }

    function get_number_of_bed_per_hospital(address hospital) public constant returns(uint128){
        return number_of_bed_per_hospital[hospital];
    }

    function get_hospital() public constant returns(address[]){
        assert(hospital_address[msg.sender]);
        return hospital_address_tab;
    }

    function get_number_of_patient_per_physician_by_id(uint128 physician_id) public constant returns(uint128){
       return number_of_patient_per_physician[physician_id];
    }

}