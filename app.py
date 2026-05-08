from flask import Flask, render_template, request, redirect, url_for, flash
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    disputes = Dispute.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', disputes=disputes)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create_listing', methods=['GET', 'POST'])
@login_required
def create_listing():

    if current_user.role != 'owner':
        flash('Only owners can create listings')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        listing = Listing(
            title=request.form['title'],
            location=request.form['location'],
            rent=request.form['rent'],
            deposit=request.form['deposit'],
            description=request.form['description']
        )

        db.session.add(listing)
        db.session.commit()

        flash('Listing created successfully!')
        return redirect(url_for('index'))

    return render_template('create_listing.html')


@app.route('/listings')
def listings():
    listings = Listing.query.all()
    return render_template('listings.html', listings=listings)


@app.route('/dispute', methods=['GET', 'POST'])
@login_required
def dispute():

    if request.method == 'POST':
        issue = request.form['issue']

        new_dispute = Dispute(
            issue=issue,
            user_id=current_user.id
        )

        db.session.add(new_dispute)
        db.session.commit()

        flash('Dispute submitted successfully!')
        return redirect(url_for('dashboard'))

    return render_template('dispute.html')


# =========================
# MAIN
# =========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)