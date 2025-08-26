from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import asyncio
from splitter_ado import SplitterADO, create_demo_splitter_config, create_demo_tx_bodies, run_splitter_demo_test

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ipinvest-demo-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ipinvest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    field = db.Column(db.String(100), nullable=False)
    inventor = db.Column(db.String(100), nullable=False)
    predicted_value = db.Column(db.Float, nullable=False)
    total_tokens = db.Column(db.Integer, nullable=False)
    tokens_sold = db.Column(db.Integer, default=0)
    token_price = db.Column(db.Float, nullable=False)
    nft_id = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investor_address = db.Column(db.String(100), nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'), nullable=False)
    tokens_purchased = db.Column(db.Integer, nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    transaction_hash = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    wallet_address = db.Column(db.String(100), unique=True, nullable=False)
    risk_preference = db.Column(db.String(20), default='moderate')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Sample data for demo
SAMPLE_IDEAS = [
    {
        "title": "Quantum Computing Patent",
        "description": "Revolutionary quantum algorithm for cryptography",
        "field": "Quantum Computing",
        "inventor": "Dr. Alice Chen",
        "predicted_value": 2500000,
        "total_tokens": 1000,
        "token_price": 2500
    },
    {
        "title": "AI-Powered Medical Diagnosis",
        "description": "Machine learning system for early disease detection",
        "field": "Healthcare AI",
        "inventor": "Dr. Bob Johnson",
        "predicted_value": 1800000,
        "total_tokens": 1000,
        "token_price": 1800
    },
    {
        "title": "Sustainable Energy Storage",
        "description": "Next-generation battery technology for renewable energy",
        "field": "Clean Energy",
        "inventor": "Dr. Sarah Williams",
        "predicted_value": 3200000,
        "total_tokens": 1000,
        "token_price": 3200
    },
    {
        "title": "Blockchain Supply Chain",
        "description": "Transparent and secure supply chain management system",
        "field": "Blockchain",
        "inventor": "Dr. Mike Rodriguez",
        "predicted_value": 1500000,
        "total_tokens": 1000,
        "token_price": 1500
    }
]

@app.route('/')
def index():
    ideas = Idea.query.filter_by(status='active').order_by(Idea.created_at.desc()).all()
    return render_template('index.html', ideas=ideas)

@app.route('/idea/<int:idea_id>')
def idea_detail(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    investments = Investment.query.filter_by(idea_id=idea_id).all()
    return render_template('idea_detail.html', idea=idea, investments=investments)

@app.route('/submit_idea', methods=['GET', 'POST'])
def submit_idea():
    if request.method == 'POST':
        data = request.form

        # Use random/demo values for predicted_value and token_price
        predicted_value = np.random.uniform(500000, 3000000)
        token_price = predicted_value / 1000

        idea = Idea(
            title=data['title'],
            description=data['description'],
            field=data['field'],
            inventor=data['inventor'],
            predicted_value=predicted_value,
            total_tokens=1000,
            token_price=token_price,
            nft_id=f"IP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        db.session.add(idea)
        db.session.commit()

        flash('Idea submitted successfully! NFT minted on Andromeda blockchain.', 'success')
        return redirect(url_for('idea_detail', idea_id=idea.id))

    return render_template('submit_idea.html')

@app.route('/invest/<int:idea_id>', methods=['POST'])
def invest(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    data = request.get_json()

    tokens_to_buy = int(data['tokens'])
    total_cost = tokens_to_buy * idea.token_price

    # Simulate blockchain transaction
    investment = Investment(
        investor_address=data['wallet_address'],
        idea_id=idea_id,
        tokens_purchased=tokens_to_buy,
        amount_paid=total_cost,
        transaction_hash=f"TX-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )

    idea.tokens_sold += tokens_to_buy
    db.session.add(investment)
    db.session.commit()

    # Calculate revenue sharing percentages
    creator_percentage = 70.0
    investor_percentage = 30.0
    investor_share = (tokens_to_buy / idea.total_tokens) * investor_percentage
    
    return jsonify({
        'success': True,
        'transaction_hash': investment.transaction_hash,
        'tokens_purchased': tokens_to_buy,
        'total_cost': total_cost,
        'revenue_sharing': {
            'creator_gets': f"{creator_percentage}%",
            'investor_pool': f"{investor_percentage}%", 
            'your_share': f"{investor_share:.2f}%",
            'explanation': f"You own {tokens_to_buy}/{idea.total_tokens} tokens = {investor_share:.2f}% of future royalties"
        }
    })

@app.route('/marketplace')
def marketplace():
    ideas = Idea.query.filter_by(status='active').all()
    return render_template('marketplace.html', ideas=ideas)

@app.route('/portfolio/<wallet_address>')
def portfolio(wallet_address):
    investments = Investment.query.filter_by(investor_address=wallet_address).all()
    total_value = sum(inv.tokens_purchased * inv.idea.token_price for inv in investments)
    return render_template('portfolio.html', investments=investments, total_value=total_value)

@app.route('/api/recommendations')
def get_recommendations():
    # Simulate recommendations with random scores
    ideas = Idea.query.filter_by(status='active').all()
    if ideas:
        recommendations = []
        for idea in ideas:
            score = np.random.uniform(0.6, 0.95)  # Simulated recommendation score
            recommendations.append({
                'idea_id': idea.id,
                'title': idea.title,
                'score': score,
                'reason': f"High potential in {idea.field} sector"
            })
        return jsonify(recommendations)
    return jsonify([])

@app.route('/api/analytics')
def analytics():
    total_ideas = Idea.query.count()
    total_investments = Investment.query.count()
    total_value = sum(inv.amount_paid for inv in Investment.query.all())

    return jsonify({
        'total_ideas': total_ideas,
        'total_investments': total_investments,
        'total_value': total_value,
        'avg_token_price': total_value / max(total_investments, 1)
    })

# Splitter ADO Demo Endpoints
@app.route('/splitter-demo')
def splitter_demo():
    """Demo page for Splitter ADO integration"""
    return render_template('splitter_demo.html')

@app.route('/splitter-test')
def splitter_test():
    """Interactive Splitter ADO testing page"""
    return render_template('splitter_test.html')

@app.route('/api/splitter/instantiate', methods=['POST'])
def api_instantiate_splitter():
    """Generate transaction body for instantiating Splitter contract"""
    try:
        data = request.get_json()
        creator_addr = data.get('creator_address')
        treasury_addr = data.get('treasury_address')
        
        if not creator_addr or not treasury_addr:
            return jsonify({'error': 'creator_address and treasury_address are required'}), 400
            
        splitter = SplitterADO()
        tx_body = splitter.get_instantiate_tx_body(creator_addr, treasury_addr)
        config = create_demo_splitter_config(creator_addr, treasury_addr)
        
        return jsonify({
            'success': True,
            'transaction_body': tx_body,
            'config_preview': config,
            'instructions': 'Sign and broadcast this transaction with Keplr or CosmJS'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/splitter/send', methods=['POST'])
def api_send_to_splitter():
    """Generate transaction body for sending ANDR to Splitter contract"""
    try:
        data = request.get_json()
        sender_addr = data.get('sender_address')
        splitter_addr = data.get('splitter_address')
        amount = data.get('amount', '1000000')  # Default 1 ANDR
        
        if not sender_addr or not splitter_addr:
            return jsonify({'error': 'sender_address and splitter_address are required'}), 400
            
        splitter = SplitterADO()
        tx_body = splitter.get_send_tx_body(sender_addr, splitter_addr, amount)
        
        return jsonify({
            'success': True,
            'transaction_body': tx_body,
            'amount_andr': f"{int(amount) / 1000000:.6f} ANDR",
            'instructions': 'Sign and broadcast this transaction with Keplr or CosmJS'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/splitter/query', methods=['POST'])
def api_query_splitter():
    """Query Splitter contract configuration and recipient balances"""
    try:
        data = request.get_json()
        splitter_addr = data.get('splitter_address')
        creator_addr = data.get('creator_address')
        treasury_addr = data.get('treasury_address')
        
        if not splitter_addr:
            return jsonify({'error': 'splitter_address is required'}), 400
            
        splitter = SplitterADO()
        
        # Run async queries
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        config = loop.run_until_complete(splitter.query_splitter_config(splitter_addr))
        
        result = {
            'success': True,
            'config': config
        }
        
        # Query balances if addresses provided
        if creator_addr:
            creator_balance = loop.run_until_complete(splitter.query_balance(creator_addr))
            result['creator_balance'] = creator_balance
            
        if treasury_addr:
            treasury_balance = loop.run_until_complete(splitter.query_balance(treasury_addr))
            result['treasury_balance'] = treasury_balance
            
        loop.close()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/splitter/demo-test', methods=['POST'])
def api_splitter_demo_test():
    """Run complete Splitter ADO demo test"""
    try:
        data = request.get_json()
        creator_addr = data.get('creator_address')
        treasury_addr = data.get('treasury_address') 
        splitter_addr = data.get('splitter_address')
        
        if not all([creator_addr, treasury_addr, splitter_addr]):
            return jsonify({'error': 'creator_address, treasury_address, and splitter_address are required'}), 400
            
        # Run async test
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(run_splitter_demo_test(creator_addr, treasury_addr, splitter_addr))
        loop.close()
        
        return jsonify({
            'success': True,
            'demo_results': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/setup-royalty-sharing/<int:idea_id>', methods=['POST'])
def setup_royalty_sharing(idea_id):
    """Setup royalty sharing for an IP idea"""
    try:
        idea = Idea.query.get_or_404(idea_id)
        data = request.get_json()
        creator_wallet = data.get('creator_wallet', 'andr1creator...')
        
        # Get all investors for this idea
        investments = Investment.query.filter_by(idea_id=idea_id).all()
        
        if not investments:
            return jsonify({'error': 'No investments found for this idea'}), 400
        
        # Create recipients list: Creator (70%) + Investors (30% split proportionally)
        recipients = []
        
        # Creator gets 70%
        recipients.append({
            "recipient": {"address": creator_wallet},
            "percent": "0.7"
        })
        
        # Investors split 30% proportionally
        total_investor_tokens = sum(inv.tokens_purchased for inv in investments)
        for investment in investments:
            investor_percentage = (investment.tokens_purchased / total_investor_tokens) * 0.3
            recipients.append({
                "recipient": {"address": investment.investor_address},
                "percent": str(investor_percentage)
            })
        
        # Generate Splitter contract instantiation
        splitter = SplitterADO()
        instantiate_msg = {
            "recipients": recipients,
            "lock_time": None,
            "default_recipient": None,
            "kernel_address": KERNEL_ADDRESS,
            "owner": creator_wallet
        }
        
        return jsonify({
            'success': True,
            'message': 'Royalty sharing configured!',
            'revenue_split': {
                'creator': '70%',
                'investors': '30% (split proportionally)',
                'total_investors': len(investments)
            },
            'next_step': 'Creator can now deploy this contract to start automatic royalty distribution'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/splitter/tx-bodies', methods=['POST'])
def api_get_tx_bodies():
    """Get all transaction bodies needed for Splitter demo"""
    try:
        data = request.get_json()
        creator_addr = data.get('creator_address')
        treasury_addr = data.get('treasury_address')
        splitter_addr = data.get('splitter_address', 'SPLITTER_CONTRACT_ADDRESS_HERE')
        
        if not creator_addr or not treasury_addr:
            return jsonify({'error': 'creator_address and treasury_address are required'}), 400
            
        tx_bodies = create_demo_tx_bodies(creator_addr, treasury_addr, splitter_addr)
        
        return jsonify({
            'success': True,
            'transaction_bodies': tx_bodies,
            'instructions': {
                '1': 'First, sign and broadcast the instantiate transaction',
                '2': 'Get the contract address from the transaction result',
                '3': 'Update splitter_address and sign the send transaction',
                '4': 'Use query endpoints to verify the split worked'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def init_demo_data():
    """Initialize demo data"""
    with app.app_context():
        db.create_all()

        # Add sample ideas if none exist
        if Idea.query.count() == 0:
            for idea_data in SAMPLE_IDEAS:
                idea = Idea(**idea_data)
                db.session.add(idea)

            # Add sample user
            user = User(
                name="Demo Investor",
                wallet_address="andromeda1demoinvestor123456789",
                risk_preference="moderate"
            )
            db.session.add(user)

            db.session.commit()

if __name__ == '__main__':
    init_demo_data()
    app.run(debug=True, host='0.0.0.0', port=5001)