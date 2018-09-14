pragma solidity ^0.4.24;

contract physician_hospital_service_contract{

    mapping(uint128 => bool) physicians;
    uint128[] physicians_tab;

    mapping(address => bool) hospital_address;
    address[] hospital_address_tab;

    mapping (address => mapping(uint128 =>bool[])) physician_hospital_service;

    constructor(address[] new_hospital_address_tab) public {
        hospital_address_tab=new_hospital_address_tab;
        for(uint16 i=0;i<hospital_address_tab.length;i++){
            hospital_address[hospital_address_tab[i]]=true;
        }
    }

    function set_hospital_service_physician(bool[] physician, address hospital, uint128 id_service) public{
        assert(hospital_address[hospital]);
        assert(physician.length==physicians_tab.length);
        physician_hospital_service[hospital][id_service]=physician;
    }

    function delete_hospital_service( address hospital, uint128 id_service) public{
        assert(hospital_address[hospital]);
        delete physician_hospital_service[hospital][id_service];
    }

    function get_physician_service_hospital_by_hospital(address hospital,uint128 service) public
    returns(bool[]){
        return physician_hospital_service[hospital][service];
    }

}