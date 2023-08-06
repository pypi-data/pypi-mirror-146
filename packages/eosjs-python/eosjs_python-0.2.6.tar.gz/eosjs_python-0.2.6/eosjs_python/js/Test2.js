const { createInitialTypes, getType, getTypesFromAbi, deserializeActionData } = require('eosjs-deserialize/dist/eosjs-serialize')
const { hexToUint8Array } = require('eosjs-deserialize/dist/eosjs-serialize')
const util = require('util');


jason = `{"version": "eosio::abi/1.0", "types": [{"new_type_name": "account_name", "type": "name"}], "structs": [{"name": "transfer", "base": "", "fields": [{"name": "from", "type": "account_name"}, {"name": "to", "type": "account_name"}, {"name": "quantity", "type": "asset"}, {"name": "memo", "type": "string"}]}, {"name": "create", "base": "", "fields": [{"name": "issuer", "type": "account_name"}, {"name": "maximum_supply", "type": "asset"}]}, {"name": "issue", "base": "", "fields": [{"name": "to", "type": "account_name"}, {"name": "quantity", "type": "asset"}, {"name": "memo", "type": "string"}]}, {"name": "account", "base": "", "fields": [{"name": "balance", "type": "asset"}]}, {"name": "currency_stats", "base": "", "fields": [{"name": "supply", "type": "asset"}, {"name": "max_supply", "type": "asset"}, {"name": "issuer", "type": "account_name"}]}], "actions": [{"name": "transfer", "type": "transfer", "ricardian_contract": ""}, {"name": "issue", "type": "issue", "ricardian_contract": ""}, {"name": "create", "type": "create", "ricardian_contract": ""}], "tables": [{"name": "accounts", "index_type": "i64", "key_names": ["currency"], "key_types": ["uint64"], "type": "account"}, {"name": "stat", "index_type": "i64", "key_names": ["currency"], "key_types": ["uint64"], "type": "currency_stats"}], "ricardian_clauses": [], "error_messages": [], "abi_extensions": [], "variants": []}`
cAccount = "eosio.token";
actName = "transfer";
actDataHex = "000000015983CC56E0E528E5D2B393F000CA9A3B00000000044556410000000021494E495449414C5F414D4F554E545F434F52504F524154455F425553494E455353"
cAbiJson = JSON.parse(jason);

function deserializeActData(cAbiJson, cAccount, actName, actDataHex) { 
    
    //cAbiJson = JSON.parse(cAbiJson);
    console.log('Deserialized');
    const types = getTypesFromAbi(createInitialTypes(), cAbiJson);
    const actions = new Map();
    for (const { name, type } of cAbiJson.actions) {
        actions.set(name, getType(types, type));
    }
    console.log('actions', actions);
    const contract = { types, actions };

    const actDataJson = deserializeActionData(
                contract,
                cAccount,
                actName,
                actDataHex,
                new util.TextEncoder(),
                new util.TextDecoder());

    console.log(JSON.stringify(actDataJson));
}

deserializeActData(cAbiJson, cAccount, actName, actDataHex);