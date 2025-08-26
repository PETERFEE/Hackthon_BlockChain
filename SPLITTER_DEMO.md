# Splitter ADO Demo - Andromeda Protocol Integration

## Quick Start (20-30 minutes)

This is a minimal proof-of-concept integration of the **Splitter ADO** into your existing app for demo purposes.

### What's Included

✅ **Function to instantiate** a Splitter contract on Andromeda mainnet with 2 recipients (80/20 split)  
✅ **Function to send** ANDR tokens to the Splitter contract address to trigger distribution  
✅ **Function to query** the Splitter config and recipients' balances for demo proof  
✅ **Web interface** for easy testing  
✅ **API endpoints** for programmatic access  

---

## Files Added/Modified

### New Files
- `splitter_ado.py` - Core Splitter ADO integration functions
- `templates/splitter_demo.html` - Web interface for testing
- `test_splitter.py` - Test script with examples
- `SPLITTER_DEMO.md` - This guide

### Modified Files
- `app.py` - Added Splitter demo endpoints
- `requirements.txt` - Added `aiohttp==3.8.5`

---

## Setup & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask App
```bash
python app.py
```

### 3. Access the Demo Interface
Visit: **http://localhost:5000/splitter-demo**

### 4. Replace Demo Addresses
Enter your actual Keplr wallet addresses:
- **Creator Address (80%)**: Your main wallet
- **Treasury Address (20%)**: Your second wallet

---

## 3-Step Test Flow

### Step 1: Instantiate Splitter Contract
1. Enter your two wallet addresses in the web interface
2. Click **"Generate Instantiate TX"**
3. Copy the transaction body
4. Sign and broadcast with Keplr or CosmJS
5. **Save the contract address** from the transaction result

### Step 2: Send ANDR to Splitter
1. Enter the contract address from Step 1
2. Set amount (default: 1 ANDR)
3. Click **"Generate Send TX"**
4. Sign and broadcast the transaction

### Step 3: Verify Split Results
1. Click **"Query Results"** 
2. Check that:
   - Creator received ~0.8 ANDR (80%)
   - Treasury received ~0.2 ANDR (20%)
   - Contract config shows correct recipients

---

## API Endpoints

### Instantiate Splitter
```bash
POST /api/splitter/instantiate
Content-Type: application/json

{
  "creator_address": "andr1...",
  "treasury_address": "andr1..."
}
```

### Send to Splitter
```bash
POST /api/splitter/send
Content-Type: application/json

{
  "sender_address": "andr1...",
  "splitter_address": "andr1...",
  "amount": "1000000"
}
```

### Query Configuration
```bash
POST /api/splitter/query
Content-Type: application/json

{
  "splitter_address": "andr1...",
  "creator_address": "andr1...",
  "treasury_address": "andr1..."
}
```

---

## Example Transaction Bodies

### Instantiate Message
```json
{
  "recipients": [
    {"recipient": {"address": "andr1creator..."}, "percent": "0.8"},
    {"recipient": {"address": "andr1treasury..."}, "percent": "0.2"}
  ],
  "lock_time": null,
  "default_recipient": null,
  "kernel_address": "andr14hj2tavq8fpesdwxxcu44rty3hh90vhujrvcmstl4zr3txmfvw9s4anegh",
  "owner": "andr1creator..."
}
```

### Send Message
```json
{
  "send": {}
}
```

### Query Message
```json
{
  "get_splitter_config": {}
}
```

---

## Configuration

### Andromeda Mainnet Settings
- **RPC**: `https://rpc.andromeda-1.andromeda.io`
- **REST**: `https://rest.andromeda-1.andromeda.io`
- **Chain ID**: `andromeda-1`
- **Kernel**: `andr14hj2tavq8fpesdwxxcu44rty3hh90vhujrvcmstl4zr3txmfvw9s4anegh`

### Default Split Configuration
- **Recipient 1**: 80% (Creator/Main wallet)
- **Recipient 2**: 20% (Treasury/Second wallet)
- **No lock time** (can update recipients)
- **No default recipient** (MVP configuration)

---

## Testing Without Real Transactions

Run the test script to see example outputs:
```bash
python test_splitter.py
```

This will show you:
- Instantiate configuration
- Transaction bodies for signing
- API endpoint documentation
- Step-by-step checklist

---

## CosmJS Integration Example

```javascript
// Example for frontend integration
const instantiateTx = {
  "typeUrl": "/cosmwasm.wasm.v1.MsgInstantiateContract",
  "value": {
    "sender": "andr1creator...",
    "admin": "andr1creator...", 
    "codeId": "1",
    "label": "Splitter-andr1cre",
    "msg": /* base64 encoded instantiate message */,
    "funds": []
  }
};

// Sign with Keplr
const result = await window.keplr.signAndBroadcast(
  "andromeda-1",
  "andr1creator...",
  [instantiateTx],
  "auto"
);
```

---

## Troubleshooting

### Common Issues

1. **"Module not found" error**
   - Run: `pip install -r requirements.txt`

2. **"Template not found" error**
   - Ensure `templates/` directory exists
   - Check that `splitter_demo.html` is in the templates folder

3. **Query failures**
   - Verify contract address is correct
   - Check network connectivity
   - Ensure contract is deployed on Andromeda mainnet

4. **Transaction signing**
   - Use Keplr browser extension or CosmJS
   - Ensure you have ANDR tokens for gas fees
   - Verify wallet is connected to Andromeda mainnet

### Need Help?
- Check the console logs in your browser developer tools
- Run `python test_splitter.py` to verify configuration
- Ensure your wallet addresses start with `andr1`

---

## Next Steps

This is an MVP integration. For production use, consider adding:
- Error handling and retry logic
- Transaction status monitoring
- Gas estimation
- Multi-signature support
- Lock time configuration
- Default recipient settings
- Integration with existing user management

---

**Ready to test!** 🚀

Start the Flask app and visit `/splitter-demo` to begin your Andromeda Splitter ADO integration demo. 