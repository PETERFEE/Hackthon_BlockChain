#!/usr/bin/env python3
"""
Test script for Splitter ADO integration
Run this to see example transaction bodies and test the integration
"""

import asyncio
import json
from splitter_ado import SplitterADO, create_demo_splitter_config, create_demo_tx_bodies

# Your actual Keplr wallet addresses
CREATOR_ADDR = "andr1tjw6yhv5ln0tlgph3g352dvrssn898qzncv6kz"  # Your main wallet (80%)
TREASURY_ADDR = "andr1ddja765fy64v432dydm0ggfaqejgtzlfyr9l8c"  # Your second wallet (20%)
SPLITTER_ADDR = "andr1splitter123456789abcdef"  # Contract address (after instantiation)

def print_section(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def main():
    print("🚀 Splitter ADO Demo - Andromeda Protocol Integration")
    print("Replace the demo addresses with your actual Keplr wallet addresses!")
    
    # 1. Show instantiate configuration
    print_section("1. INSTANTIATE CONFIGURATION")
    config = create_demo_splitter_config(CREATOR_ADDR, TREASURY_ADDR)
    print("Splitter configuration:")
    print(json.dumps(config, indent=2))
    
    # 2. Generate transaction bodies
    print_section("2. TRANSACTION BODIES")
    splitter = SplitterADO()
    
    # Instantiate transaction
    print("📝 Instantiate Transaction Body:")
    instantiate_tx = splitter.get_instantiate_tx_body(CREATOR_ADDR, TREASURY_ADDR)
    print(json.dumps(instantiate_tx, indent=2))
    
    print("\n" + "-"*50)
    
    # Send transaction
    print("💰 Send Transaction Body (1 ANDR):")
    send_tx = splitter.get_send_tx_body(CREATOR_ADDR, SPLITTER_ADDR)
    print(json.dumps(send_tx, indent=2))
    
    # 3. Test checklist
    print_section("3. DEMO TEST CHECKLIST")
    print("""
    ✅ Step-by-Step Test Process:
    
    1. INSTANTIATE SPLITTER:
       - Copy the instantiate transaction body above
       - Sign and broadcast with Keplr or CosmJS
       - Note the contract address from the transaction result
    
    2. SEND FUNDS:
       - Update SPLITTER_ADDR with the actual contract address
       - Copy the send transaction body above
       - Sign and broadcast 1 ANDR to the splitter
    
    3. VERIFY SPLIT:
       - Check balances of both recipient addresses
       - Creator should receive ~0.8 ANDR
       - Treasury should receive ~0.2 ANDR
       - Use the query endpoints to verify configuration
    
    🌐 Web Interface:
       - Start Flask app: python app.py
       - Visit: http://localhost:5000/splitter-demo
       - Enter your wallet addresses and test!
    """)
    
    # 4. API endpoints summary
    print_section("4. API ENDPOINTS")
    print("""
    Available endpoints for integration:
    
    POST /api/splitter/instantiate
    - Body: {"creator_address": "andr1...", "treasury_address": "andr1..."}
    - Returns: Transaction body for instantiation
    
    POST /api/splitter/send  
    - Body: {"sender_address": "andr1...", "splitter_address": "andr1...", "amount": "1000000"}
    - Returns: Transaction body for sending funds
    
    POST /api/splitter/query
    - Body: {"splitter_address": "andr1...", "creator_address": "andr1...", "treasury_address": "andr1..."}
    - Returns: Contract config and balance information
    
    POST /api/splitter/tx-bodies
    - Body: {"creator_address": "andr1...", "treasury_address": "andr1..."}
    - Returns: All transaction bodies needed for demo
    """)

async def test_queries():
    """Test the query functions (requires actual contract address)"""
    print_section("5. QUERY TEST (Optional)")
    print("⚠️  This requires an actual deployed contract address")
    
    if SPLITTER_ADDR.startswith("andr1splitter123"):
        print("❌ Using demo address - replace with actual contract address to test queries")
        return
    
    splitter = SplitterADO()
    
    try:
        print("🔍 Querying splitter configuration...")
        config = await splitter.query_splitter_config(SPLITTER_ADDR)
        print("Config:", json.dumps(config, indent=2))
        
        print("💰 Querying creator balance...")
        creator_balance = await splitter.query_balance(CREATOR_ADDR)
        print("Creator:", creator_balance)
        
        print("💰 Querying treasury balance...")
        treasury_balance = await splitter.query_balance(TREASURY_ADDR)
        print("Treasury:", treasury_balance)
        
    except Exception as e:
        print(f"❌ Query failed: {e}")

if __name__ == "__main__":
    main()
    
    # Uncomment to test queries with real addresses
    # asyncio.run(test_queries()) 