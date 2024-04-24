pragma solidity ^0.4.25;
pragma experimental ABIEncoderV2;

contract PassportDataStorage {
    
    // 定义PassportData结构体
    struct PassportData {
        string userPk;
        string govPk;
        string id;
        string name;
        string gender;
        string date_of_birth;
        string country;
        string number;
        string issuing_authority;
        string issuing_country;
        string start;
        string expiration;
        string photo;
        string prepp;
        string futurepp;
        string idcard;
    }
    
    mapping(string => PassportData) private passportDataMapping;
    mapping(string => string[]) private userPkToPassports;
    
    
    function addPassportData(string[] memory passportData) public {
        
        require(passportData.length == 16, "Invalid number of arguments");
        
        string memory userPk = passportData[0];
        string memory govPk = passportData[1];
        string memory id = passportData[2];
        
        
        PassportData memory newPassportData = PassportData({
            userPk: userPk,
            govPk: govPk,
            id: id,
            name: passportData[3],
            gender: passportData[4],
            date_of_birth: passportData[5],
            country: passportData[6],
            number: passportData[7],
            issuing_authority: passportData[8],
            issuing_country: passportData[9],
            start: passportData[10],
            expiration: passportData[11],
            photo: passportData[12],
            prepp: passportData[13],
            futurepp: passportData[14],
            idcard: passportData[15]
        });
        
        passportDataMapping[id] = newPassportData;
        userPkToPassports[userPk].push(id);
    }
    
    function getPassportDataByUserPk(string memory userPk) public view returns (PassportData[] memory) {
        string[] memory ids = userPkToPassports[userPk];
        PassportData[] memory result = new PassportData[](ids.length);
        
        for (uint i = 0; i < ids.length; i++) {
            result[i] = passportDataMapping[ids[i]];
        }
        
        return result;
    }
}