"""
Splitter ADO Integration for Andromeda Protocol
Minimal implementation for demo purposes
"""

import json
import requests
from typing import Dict, List, Any, Optional

# Andromeda Mainnet Configuration
ANDROMEDA_MAINNET_RPC = "https://rpc.andromeda-1.andromeda.io"
ANDROMEDA_MAINNET_REST = "https://rest.andromeda-1.andromeda.io"
ANDROMEDA_CHAIN_ID = "andromeda-1"
KERNEL_ADDRESS = "andr14hj2tavq8fpesdwxxcu44rty3hh90vhujrvcmstl4zr3txmfvw9s4anegh"  # Mainnet kernel

class SplitterADO:
    def __init__(self, rpc_url: str = ANDROMEDA_MAINNET_RPC, rest_url: str = ANDROMEDA_MAINNET_REST):
        self.rpc_url = rpc_url
        self.rest_url = rest_url
        self.chain_id = ANDROMEDA_CHAIN_ID
        
    def create_instantiate_msg(self, 
                              recipients: List[Dict[str, Any]], 
                              owner: str,
                              kernel_address: str = KERNEL_ADDRESS) -> Dict[str, Any]:
        """
        Create InstantiateMsg for Splitter ADO
        
        Args:
            recipients: List of recipient objects with address and percent
            owner: Owner address
            kernel_address: Kernel address for Andromeda protocol
            
        Returns:
            InstantiateMsg dictionary
        """
        return {
            "recipients": recipients,
            "lock_time": None,
            "default_recipient": None,
            "kernel_address": kernel_address,
            "owner": owner
        }
    
    def create_recipients(self, address1: str, address2: str, split1: str = "0.8", split2: str = "0.2") -> List[Dict[str, Any]]:
        """
        Create recipients list for 80/20 split
        
        Args:
            address1: First recipient address (gets 80%)
            address2: Second recipient address (gets 20%)
            split1: Percentage for first recipient (default: "0.8")
            split2: Percentage for second recipient (default: "0.2")
            
        Returns:
            List of recipient objects
        """
        return [
            {
                "recipient": {"address": address1},
                "percent": split1
            },
            {
                "recipient": {"address": address2}, 
                "percent": split2
            }
        ]
    
    def get_instantiate_tx_body(self, 
                               creator_address: str,
                               treasury_address: str,
                               code_id: int = 1215) -> Dict[str, Any]:
        """
        Get transaction body for instantiating Splitter contract
        
        Args:
            creator_address: Address instantiating the contract
            treasury_address: Second recipient address (20%)
            code_id: Code ID for Splitter ADO on mainnet
            
        Returns:
            Transaction body for CosmJS
        """
        recipients = self.create_recipients(creator_address, treasury_address)
        instantiate_msg = self.create_instantiate_msg(recipients, creator_address)
        
        return {
            "typeUrl": "/cosmwasm.wasm.v1.MsgInstantiateContract",
            "value": {
                "sender": creator_address,
                "admin": creator_address,
                "codeId": str(code_id),
                "label": f"Splitter-{creator_address[:8]}",
                "msg": json.dumps(instantiate_msg),
                "funds": []
            }
        }
    
    def get_send_tx_body(self, 
                        sender_address: str,
                        splitter_contract_address: str,
                        amount: str = "1000000") -> Dict[str, Any]:
        """
        Get transaction body for sending ANDR to Splitter contract
        
        Args:
            sender_address: Address sending the funds
            splitter_contract_address: Splitter contract address
            amount: Amount in uandr (default: 1 ANDR = 1000000 uandr)
            
        Returns:
            Transaction body for CosmJS
        """
        execute_msg = {"send": {}}
        
        return {
            "typeUrl": "/cosmwasm.wasm.v1.MsgExecuteContract",
            "value": {
                "sender": sender_address,
                "contract": splitter_contract_address,
                "msg": json.dumps(execute_msg),
                "funds": [{"denom": "uandr", "amount": amount}]
            }
        }
    
    async def query_splitter_config(self, contract_address: str) -> Dict[str, Any]:
        """
        Query Splitter contract configuration
        
        Args:
            contract_address: Splitter contract address
            
        Returns:
            Contract configuration and recipients
        """
        query_msg = {"get_splitter_config": {}}
        query_data = json.dumps(query_msg)
        
        try:
            # Using REST API for query
            url = f"{self.rest_url}/cosmwasm/wasm/v1/contract/{contract_address}/smart/{query_data}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def query_balance(self, address: str) -> Dict[str, Any]:
        """
        Query ANDR balance for an address
        
        Args:
            address: Address to query balance for
            
        Returns:
            Balance information
        """
        try:
            url = f"{self.rest_url}/cosmos/bank/v1beta1/balances/{address}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Find ANDR balance
            andr_balance = "0"
            for coin in data.get("balances", []):
                if coin["denom"] == "uandr":
                    andr_balance = coin["amount"]
                    break
                    
            return {
                "address": address,
                "andr_balance": andr_balance,
                "andr_balance_formatted": f"{int(andr_balance) / 1000000:.6f} ANDR"
            }
        except Exception as e:
            return {"error": str(e)}

# Demo helper functions
def create_demo_splitter_config(creator_addr: str, treasury_addr: str) -> Dict[str, Any]:
    """Create demo configuration for Splitter ADO"""
    splitter = SplitterADO()
    recipients = splitter.create_recipients(creator_addr, treasury_addr)
    return splitter.create_instantiate_msg(recipients, creator_addr)

def create_demo_tx_bodies(creator_addr: str, treasury_addr: str, splitter_addr: str) -> Dict[str, Any]:
    """Create all transaction bodies needed for demo"""
    splitter = SplitterADO()
    
    return {
        "instantiate": splitter.get_instantiate_tx_body(creator_addr, treasury_addr),
        "send": splitter.get_send_tx_body(creator_addr, splitter_addr),
        "query_config": {"get_splitter_config": {}},
        "addresses_to_check": [creator_addr, treasury_addr, splitter_addr]
    }

# Test checklist functions
async def run_splitter_demo_test(creator_addr: str, treasury_addr: str, splitter_addr: str):
    """
    Run the 3-step test flow:
    1. Instantiate Splitter (manual step - returns tx body)
    2. Send 1 ANDR to Splitter (manual step - returns tx body) 
    3. Verify balances and config (automated query)
    """
    splitter = SplitterADO()
    
    print("=== SPLITTER ADO DEMO TEST ===")
    print("\nStep 1: Instantiate Splitter Contract")
    instantiate_tx = splitter.get_instantiate_tx_body(creator_addr, treasury_addr)
    print(f"Transaction body ready for signing:")
    print(json.dumps(instantiate_tx, indent=2))
    
    print("\nStep 2: Send 1 ANDR to Splitter")
    send_tx = splitter.get_send_tx_body(creator_addr, splitter_addr)
    print(f"Transaction body ready for signing:")
    print(json.dumps(send_tx, indent=2))
    
    print("\nStep 3: Query Results")
    config = await splitter.query_splitter_config(splitter_addr)
    creator_balance = await splitter.query_balance(creator_addr)
    treasury_balance = await splitter.query_balance(treasury_addr)
    
    print(f"Splitter Config: {json.dumps(config, indent=2)}")
    print(f"Creator Balance: {creator_balance}")
    print(f"Treasury Balance: {treasury_balance}")
    
    return {
        "instantiate_tx": instantiate_tx,
        "send_tx": send_tx,
        "config": config,
        "creator_balance": creator_balance,
        "treasury_balance": treasury_balance
    } 