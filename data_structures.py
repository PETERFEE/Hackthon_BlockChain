# data_structures.py

class IdeaMetadata:
    def __init__(self, title, description, field, inventor, predicted_value, total_tokens):
        self.title = title
        self.description = description
        self.field = field
        self.inventor = inventor
        self.predicted_value = predicted_value
        self.total_tokens = total_tokens

class InvestorProfile:
    def __init__(self, name, wallet_address, risk_preference):
        self.name = name
        self.wallet_address = wallet_address
        self.risk_preference = risk_preference
        self.investments = []

    def add_investment(self, idea_title, tokens_owned):
        self.investments.append({"idea": idea_title, "tokens": tokens_owned})
2. CosmWasm Smart Contracts (Rust)
ip_token.rs – NFT Contract (CW721)
rust
Copy
Edit
// ip_token.rs
use cosmwasm_std::{Binary, DepsMut, Env, MessageInfo, Response, StdResult};
use cw721_base::{ContractError, ExecuteMsg, InstantiateMsg};

pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    msg: InstantiateMsg,
) -> StdResult<Response> {
    cw721_base::Cw721Contract::default().instantiate(deps, _env, info, msg)
}
