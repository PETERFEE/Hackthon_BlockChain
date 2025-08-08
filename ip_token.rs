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
