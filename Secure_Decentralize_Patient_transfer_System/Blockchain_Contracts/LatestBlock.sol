pragma solidity ^0.4.24;

contract LatestBLock{

    address public latest_block;
    address potential_block;
    address[] hospital_address_tab;
    mapping(address => bool) hospital_address;

    constructor(address[] new_hospital_address_tab) public {
        hospital_address_tab=new_hospital_address_tab;
        for(uint16 i=0;i<hospital_address_tab.length;i++){
            hospital_address[hospital_address_tab[i]]=true;
        }
    }

    function set_new_latest_block_address(address new_latest_block) public {
        require(hospital_address[msg.sender]);
        latest_block=new_latest_block;
    }

    function set_potential_block_address(address new_potential_block) public {
        require(hospital_address[msg.sender]);
        potential_block=new_potential_block;
    }


    function get_latest_block_address() public constant returns(address) {
       return latest_block;
    }

    function get_potential_block_address() public constant returns(address){
        return potential_block;
    }


}