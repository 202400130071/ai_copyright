// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract ContentRegistry {
    // 内容注册事件
    event ContentRegistered(
        bytes32 indexed contentHash,
        address indexed owner,
        string license,
        uint256 timestamp
    );

    // 许可证更新事件
    event LicenseUpdated(
        bytes32 indexed contentHash,
        string oldLicense,
        string newLicense,
        uint256 timestamp
    );

    // 内容结构
    struct Content {
        address owner;
        string license;
        uint256 timestamp;
        string aiModel;
        bool exists;
    }

    // 存储内容信息
    mapping(bytes32 => Content) public contents;

    // 用户拥有的内容
    mapping(address => bytes32[]) public userContents;

    // 支持的许可证类型
    string[] public supportedLicenses = [
        "All rights reserved",
        "MIT",
        "Creative Commons BY-SA 4.0",
        "Apache 2.0"
    ];

    // 支持的AI模型
    string[] public supportedAIModels = [
        "GPT-4",
        "GPT-3.5",
        "DALL-E 3",
        "Claude 2",
        "Gemini Pro"
    ];

    // 检查许可证是否支持
    modifier validLicense(string memory license) {
        bool found = false;
        for (uint i = 0; i < supportedLicenses.length; i++) {
            if (keccak256(bytes(supportedLicenses[i])) == keccak256(bytes(license))) {
                found = true;
                break;
            }
        }
        require(found, "Unsupported license type");
        _;
    }

    // 检查AI模型是否支持
    modifier validAIModel(string memory model) {
        bool found = false;
        for (uint i = 0; i < supportedAIModels.length; i++) {
            if (keccak256(bytes(supportedAIModels[i])) == keccak256(bytes(model))) {
                found = true;
                break;
            }
        }
        require(found, "Unsupported AI model");
        _;
    }

    // 检查内容所有权
    modifier onlyContentOwner(bytes32 contentHash) {
        require(contents[contentHash].exists, "Content does not exist");
        require(contents[contentHash].owner == msg.sender, "Not the content owner");
        _;
    }

    // 注册内容
    function registerContent(
        bytes32 contentHash,
        string memory license,
        string memory aiModel
    )
        external
        validLicense(license)
        validAIModel(aiModel)
        returns (bool)
    {
        require(!contents[contentHash].exists, "Content already registered");

        contents[contentHash] = Content({
            owner: msg.sender,
            license: license,
            timestamp: block.timestamp,
            aiModel: aiModel,
            exists: true
        });

        userContents[msg.sender].push(contentHash);

        emit ContentRegistered(
            contentHash,
            msg.sender,
            license,
            block.timestamp
        );

        return true;
    }

    // 更新许可证
    function updateLicense(
        bytes32 contentHash,
        string memory newLicense
    )
        external
        onlyContentOwner(contentHash)
        validLicense(newLicense)
        returns (bool)
    {
        string memory oldLicense = contents[contentHash].license;
        contents[contentHash].license = newLicense;

        emit LicenseUpdated(
            contentHash,
            oldLicense,
            newLicense,
            block.timestamp
        );

        return true;
    }

    // 验证内容所有权
    function verifyContent(
        bytes32 contentHash
    )
        external
        view
        returns (
            bool exists,
            address owner,
            string memory license,
            uint256 timestamp,
            string memory aiModel
        )
    {
        Content memory content = contents[contentHash];
        return (
            content.exists,
            content.owner,
            content.license,
            content.timestamp,
            content.aiModel
        );
    }

    // 获取用户的内容列表
    function getUserContents(
        address user
    )
        external
        view
        returns (bytes32[] memory)
    {
        return userContents[user];
    }

    // 获取支持的许可证类型
    function getSupportedLicenses()
        external
        view
        returns (string[] memory)
    {
        return supportedLicenses;
    }

    // 获取支持的AI模型
    function getSupportedAIModels()
        external
        view
        returns (string[] memory)
    {
        return supportedAIModels;
    }
}