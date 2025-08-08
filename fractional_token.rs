// fractional_token.rs
use cw20_base::contract::{instantiate as cw20_instantiate, execute as cw20_execute};
use cosmwasm_std::{DepsMut, Env, MessageInfo, Response, StdResult};

pub fn instantiate(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    msg: cw20_base::msg::InstantiateMsg,
) -> StdResult<Response> {
    cw20_instantiate(deps, env, info, msg)
}
