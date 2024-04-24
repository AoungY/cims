pragma solidity ^0.4.25;
pragma experimental ABIEncoderV2;

contract IdDataStorage {
    
    // 定义IdData结构体
    struct IdData {
        string userPk;
        string govPk;
        string id;
        string name;
        string gender;
        string eth_group;
        string addr;
        string number;
        string date_of_birth;
        string authority;
        string start;
        string expiration;
        string photo;
        string preid;
        string futureid;
        string pp;
    }
    
    // 使用mapping存储IdData，key为string类型的id
    mapping(string => IdData) private idDataMapping;
    mapping(string => string[]) private userPkToIds;
    
    // 添加IdData
    function addIdData(string[] memory idData) public {
        
        require(idData.length == 16, "Invalid number of arguments");
        
        string memory userPk = idData[0];
        string memory govPk = idData[1];
        string memory id = idData[2];
        
        
        IdData memory newIdData = IdData({
            userPk: userPk,
            govPk: govPk,
            id: id,
            name: idData[3],
            gender: idData[4],
            eth_group: idData[5],
            addr: idData[6],
            number: idData[7],
            date_of_birth: idData[8],
            authority: idData[9],
            start: idData[10],
            expiration: idData[11],
            photo: idData[12],
            preid: idData[13],
            futureid: idData[14],
            pp: idData[15]
        });
        
        idDataMapping[id] = newIdData;
        userPkToIds[userPk].push(id);
    }
    
    // 根据userPk获取所有匹配的IdData记录
    function getIdDataByUserPk(string memory userPk) public view returns (IdData[] memory) {
        string[] memory ids = userPkToIds[userPk];
        IdData[] memory result = new IdData[](ids.length);
        
        for (uint i = 0; i < ids.length; i++) {
            result[i] = idDataMapping[ids[i]];
        }
        
        return result;
    }
}