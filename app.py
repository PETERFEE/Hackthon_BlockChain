from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np

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

    return jsonify({
        'success': True,
        'transaction_hash': investment.transaction_hash,
        'tokens_purchased': tokens_to_buy,
        'total_cost': total_cost
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
    app.run(debug=True, host='0.0.0.0', port=5000)