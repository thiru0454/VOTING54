from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///votes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for storing the vote counts
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, default=0)

# Initialize the database (run this once to create the tables)
@app.before_first_request
def create_tables():
    db.create_all()

# Route to get current vote counts
@app.route('/votes', methods=['GET'])
def get_votes():
    votes = Vote.query.all()
    vote_counts = {vote.candidate: vote.count for vote in votes}
    return jsonify(vote_counts)

# Route to submit a vote
@app.route('/vote', methods=['POST'])
def submit_vote():
    data = request.json
    candidate = data.get('candidate')

    if candidate not in ['candidate1', 'candidate2', 'candidate3']:
        return jsonify({"error": "Invalid candidate"}), 400

    # Check if the candidate exists in the database
    vote = Vote.query.filter_by(candidate=candidate).first()
    if not vote:
        # If the candidate does not exist, create a new record
        vote = Vote(candidate=candidate)
        db.session.add(vote)
    
    # Increment the vote count
    vote.count += 1
    db.session.commit()

    return jsonify({"message": "Vote submitted successfully!"})

# Home route (you can serve your HTML from here if needed)
@app.route('/')
def home():
    return render_template('index.html')  # Serve your front-end HTML here

if __name__ == '__main__':
    app.run(debug=True)
