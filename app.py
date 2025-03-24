from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = '4f3c2d5a6e7b8c9d1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p'  # Required for session management

# Admin credentials
ADMIN_USERNAME = "Thiru"
ADMIN_PASSWORD = "Thiru0454"

# List to store candidates
candidates = []

@app.route('/')
def home():
    """Render the main dashboard."""
    return render_template('dashboard.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    """Admin login route."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_page'))
        else:
            return render_template('admin.html', error="Invalid username or password.")

    return render_template('admin.html')

@app.route('/adminpage')
def admin_page():
    """Render the admin panel."""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    return render_template('adminpage.html', candidates=candidates)

@app.route('/logout')
def logout():
    """Clear session and logout the user."""
    session.clear()
    return redirect(url_for('home'))

@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    """Add a candidate to the list."""
    candidate_name = request.json.get('name')
    if candidate_name and candidate_name not in candidates:
        candidates.append(candidate_name)
        return jsonify({'success': True, 'message': f'Candidate "{candidate_name}" added.', 'candidates': candidates})
    return jsonify({'success': False, 'message': 'Candidate already exists or invalid input.', 'candidates': candidates})

@app.route('/remove_candidate', methods=['POST'])
def remove_candidate():
    """Remove a candidate from the list."""
    candidate_name = request.json.get('name')
    if candidate_name in candidates:
        candidates.remove(candidate_name)
        return jsonify({'success': True, 'message': f'Candidate "{candidate_name}" removed.', 'candidates': candidates})
    return jsonify({'success': False, 'message': 'Candidate not found.', 'candidates': candidates})

@app.route('/get_candidates')
def get_candidates():
    """Fetch the updated list of candidates."""
    return jsonify({'candidates': candidates})

@app.route('/update_dashboard', methods=['POST'])
def update_dashboard():
    """Trigger a dashboard update."""
    return jsonify({'success': True, 'message': 'Dashboard updated successfully.'})

if __name__ == '__main__':
    app.run(debug=True)
