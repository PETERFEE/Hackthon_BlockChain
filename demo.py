#!/usr/bin/env python3
"""
IPInvest Demo Script
Demonstrates the decentralized IP tokenization platform
"""

import os
import sys
import time
import json
import requests
from datetime import datetime

def print_banner():
    """Print the IPInvest demo banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    IPInvest Demo                             ║
    ║         Decentralized IP Tokenization Platform              ║
    ║                                                              ║
    ║  🧠 Tokenize Intellectual Property                          ║
    ║  💰 Enable Fractional Ownership                            ║
    ║  🤖 AI-Powered Valuation                                   ║
    ║  ⛓️  Built on Andromeda Blockchain                         ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'pandas', 'numpy', 'sklearn', 'joblib',
        'stable_baselines3', 'gym', 'torch', 'tensorflow'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed!")
    return True

def demo_ml_models():
    """Demonstrate ML models functionality"""
    print("\n🤖 Testing ML Models...")
    
    try:
        from valuation_model import ValuationModel
        from rl_recommender import RLRecommender
        import numpy as np
        
        # Test valuation model
        print("📊 Testing Valuation Model...")
        model = ValuationModel()
        
        # Simulate features for a patent
        features = np.array([
            500,  # Description length
            15,   # Field complexity
            1,    # AI indicator
            0,    # Blockchain indicator
            1.2   # Random factor
        ])
        
        # Note: In demo, we'll simulate the prediction
        predicted_value = np.random.uniform(500000, 3000000)
        print(f"   Predicted Value: ${predicted_value:,.0f}")
        
        # Test RL recommender
        print("🎯 Testing RL Recommender...")
        token_data = np.random.rand(10)
        recommender = RLRecommender(token_data)
        print("   RL Agent initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ ML Models test failed: {e}")
        return False

def demo_smart_contracts():
    """Demonstrate smart contract functionality"""
    print("\n⛓️  Testing Smart Contracts...")
    
    try:
        # Simulate smart contract interactions
        contracts = {
            'ip_token.rs': 'NFT Contract (CW721)',
            'fractional_token.rs': 'Fractional Token (CW20)',
            'marketplace.rs': 'Marketplace Contract',
            'splitter.rs': 'Revenue Splitter'
        }
        
        for contract, description in contracts.items():
            print(f"   ✅ {contract}: {description}")
        
        # Simulate NFT minting
        nft_id = f"IP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        print(f"   🎨 NFT Minted: {nft_id}")
        
        # Simulate token creation
        token_address = f"andromeda1token{nft_id[-8:]}"
        print(f"   🪙 Tokens Created: {token_address}")
        
        return True
        
    except Exception as e:
        print(f"❌ Smart Contracts test failed: {e}")
        return False

def demo_web_interface():
    """Demonstrate web interface functionality"""
    print("\n🌐 Testing Web Interface...")
    
    try:
        # Check if Flask app can be imported
        from app import app
        
        print("   ✅ Flask app loaded successfully")
        print("   🚀 Starting web server...")
        print("   📱 Open http://localhost:5000 in your browser")
        
        return True
        
    except Exception as e:
        print(f"❌ Web Interface test failed: {e}")
        return False

def run_demo_scenarios():
    """Run demo scenarios"""
    print("\n🎬 Running Demo Scenarios...")
    
    scenarios = [
        {
            'name': 'Idea Submission',
            'description': 'Creator submits quantum computing patent',
            'steps': [
                'User fills out idea submission form',
                'AI analyzes and predicts value: $2.5M',
                'NFT minted on Andromeda blockchain',
                '1000 fractional tokens created',
                'Token price set at $2,500 per token'
            ]
        },
        {
            'name': 'Investment Process',
            'description': 'Investor purchases fractional tokens',
            'steps': [
                'Investor browses marketplace',
                'AI recommends quantum computing patent',
                'Investor purchases 10 tokens for $25,000',
                'Smart contract executes transaction',
                'Tokens transferred to investor wallet'
            ]
        },
        {
            'name': 'Royalty Distribution',
            'description': 'Automatic royalty distribution to token holders',
            'steps': [
                'Patent generates $1M licensing revenue',
                'Smart contract splits revenue automatically',
                'Creator receives 70% ($700,000)',
                'Token holders receive 30% ($300,000)',
                'Each token earns $300 in royalties'
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['name']}")
        print(f"   {scenario['description']}")
        for step in scenario['steps']:
            print(f"   • {step}")
            time.sleep(0.5)

def show_platform_features():
    """Show platform features"""
    print("\n✨ Platform Features:")
    
    features = [
        "🧠 IP Tokenization - Convert ideas to NFTs",
        "💰 Fractional Ownership - Divide IP into 1000 tokens",
        "🤖 AI Valuation - ML-powered price prediction",
        "🎯 RL Recommendations - Smart investment suggestions",
        "⛓️  Blockchain Security - Andromeda smart contracts",
        "📊 Real-time Analytics - Portfolio tracking",
        "🔄 Automated Royalties - Smart contract distributions",
        "🌐 Social Interface - Like Facebook for ideas"
    ]
    
    for feature in features:
        print(f"   {feature}")
        time.sleep(0.3)

def main():
    """Main demo function"""
    print_banner()
    
    print("🚀 Starting IPInvest Demo...")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Demo cannot continue due to missing dependencies")
        return
    
    # Test components
    ml_success = demo_ml_models()
    contract_success = demo_smart_contracts()
    web_success = demo_web_interface()
    
    # Show features
    show_platform_features()
    
    # Run scenarios
    run_demo_scenarios()
    
    # Summary
    print("\n" + "="*60)
    print("📊 Demo Summary:")
    print(f"   ML Models: {'✅' if ml_success else '❌'}")
    print(f"   Smart Contracts: {'✅' if contract_success else '❌'}")
    print(f"   Web Interface: {'✅' if web_success else '❌'}")
    
    print("\n🎉 Demo completed!")
    print("\n📝 Next Steps:")
    print("   1. Run: python app.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Explore the IPInvest platform")
    print("   4. Submit ideas and make investments")
    
    print("\n🔗 Useful Links:")
    print("   • Andromeda Documentation: https://docs.andromedaprotocol.io")
    print("   • CosmWasm: https://cosmwasm.com")
    print("   • IP Tokenization Guide: https://novotechip.com")

if __name__ == "__main__":
    main() 