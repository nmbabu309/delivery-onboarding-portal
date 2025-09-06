from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from extensions import db, login_manager
from models import User, Agent
from forms import LoginForm, RegistrationForm, PersonalInfoForm
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
            if existing_user:
                flash('Username or email already exists.', 'danger')
                return render_template('register.html', form=form)
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                role='agent'
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please complete your profile.', 'success')
            login_user(new_user)
            return redirect(url_for('personal_info'))
        return render_template('register.html', form=form)

    @app.route('/login/agent', methods=['GET', 'POST'])
    def agent_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data, role='agent').first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('agent_dashboard'))
            flash("Invalid credentials", "danger")
        return render_template('agent_login.html', form=form)

    @app.route('/login/admin', methods=['GET', 'POST'])
    def admin_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data, role='admin').first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('admin_dashboard'))
            flash("Invalid credentials", "danger")
        return render_template('admin_login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out successfully.', 'success')
        return redirect(url_for('index'))

    @app.route('/agent/dashboard')
    @login_required
    def agent_dashboard():
        if current_user.role != 'agent':
            return redirect(url_for('agent_login'))
        agent = Agent.query.filter_by(user_id=current_user.id).first()
        return render_template('agent_dashboard.html', agent=agent)

    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if current_user.role != 'admin':
            return redirect(url_for('admin_login'))
        agents = Agent.query.join(User).all()
        return render_template('admin_dashboard.html', agents=agents)

    @app.route('/agent/personal_info', methods=['GET', 'POST'])
    @login_required
    def personal_info():
        if current_user.role != 'agent':
            return redirect(url_for('agent_login'))

        form = PersonalInfoForm()
        agent = Agent.query.filter_by(user_id=current_user.id).first()

        if request.method == 'GET' and agent:
            form.first_name.data = agent.first_name
            form.last_name.data = agent.last_name
            form.phone.data = agent.phone
            form.dob.data = agent.dob
            form.address.data = agent.address
            form.city.data = agent.city
            form.state.data = agent.state
            form.pincode.data = agent.pincode
            form.emergency_contact_name.data = agent.emergency_contact_name
            form.emergency_contact_phone.data = agent.emergency_contact_phone

        if form.validate_on_submit():
            if not agent:
                agent = Agent(user_id=current_user.id)
                db.session.add(agent)

            agent.first_name = form.first_name.data
            agent.last_name = form.last_name.data
            agent.phone = form.phone.data
            agent.dob = form.dob.data
            agent.address = form.address.data
            agent.city = form.city.data
            agent.state = form.state.data
            agent.pincode = form.pincode.data
            agent.emergency_contact_name = form.emergency_contact_name.data
            agent.emergency_contact_phone = form.emergency_contact_phone.data  # FIXED TYPO

            db.session.commit()
            flash('Personal information saved successfully.', 'success')
            return redirect(url_for('agent_dashboard'))

        return render_template('personal_info.html', form=form)

    @app.route('/agent/upload_documents')
    @login_required
    def upload_documents():
        if current_user.role != 'agent':
            return redirect(url_for('agent_login'))
        return render_template('document_upload.html')

    @app.route('/admin/verify/<int:agent_id>/<string:action>', methods=['POST'])
    @login_required
    def verify_agent(agent_id, action):
        if current_user.role != 'admin':
            return redirect(url_for('admin_login'))
        agent = Agent.query.get_or_404(agent_id)
        if action.lower() in ['approve', 'reject', 'verify']:
            agent.application_status = action.capitalize()
            db.session.commit()
            flash(f"Application {action}d successfully.", 'success')
        return redirect(url_for('admin_dashboard'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
