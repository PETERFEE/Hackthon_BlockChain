// marketplace.rs
use cosmwasm_std::{DepsMut, Env, MessageInfo, Response, StdResult};

pub fn list_ip_asset(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    price: u128,
) -> StdResult<Response> {
    Ok(Response::new().add_attribute("action", "list_ip_asset").add_attribute("price", price.to_string()))
}
