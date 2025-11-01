from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from wtforms import StringField, TextAreaField, SelectField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed
from flask_admin.form import Select2Field
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import secrets
from PIL import Image

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blackstone_eg.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@blackstoneegpartners.com')

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/uploads/logos', exist_ok=True)
os.makedirs('static/uploads/blog', exist_ok=True)
os.makedirs('static/uploads/portfolio', exist_ok=True)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    service = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')  # new, contacted, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Contact {self.name} - {self.email}>'

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    author = db.Column(db.String(100), nullable=False)
    featured_image = db.Column(db.String(200))
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = db.Column(db.String(200))

    def __repr__(self):
        return f'<BlogPost {self.title}>'

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    client = db.Column(db.String(100))
    value = db.Column(db.String(50))  # Investment value
    completion_date = db.Column(db.Date)
    featured_image = db.Column(db.String(200))
    gallery_images = db.Column(db.Text)  # JSON string of image paths
    status = db.Column(db.String(50), default='completed')  # completed, ongoing, planned
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Portfolio {self.title}>'

class CompanySettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logo_path = db.Column(db.String(200))
    company_name = db.Column(db.String(200), default='Blackstone EG & Partners')
    tagline = db.Column(db.String(300), default='Your Trusted Partner In Equatorial Guinea')
    phone = db.Column(db.String(20), default='+240 555 312 711')
    email = db.Column(db.String(120), default='info@blackstoneegpartners.com')
    address = db.Column(db.String(200), default='Malabo, Equatorial Guinea')
    google_analytics_id = db.Column(db.String(50))
    facebook_pixel_id = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    service = SelectField('Investment Interest', choices=[
        ('', 'Select Investment Interest'),
        ('energy', 'Energy & Infrastructure'),
        ('real-estate', 'Real Estate Development'),
        ('manufacturing', 'Manufacturing'),
        ('technology', 'Technology & Innovation'),
        ('other', 'Other Opportunities')
    ], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Admin Views
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))

class ContactAdminView(SecureModelView):
    column_list = ['name', 'email', 'service', 'status', 'created_at']
    column_searchable_list = ['name', 'email', 'message']
    column_filters = ['service', 'status', 'created_at']
    column_editable_list = ['status', 'notes']
    form_excluded_columns = ['created_at']
    
    # Enable details view with a clickable button
    can_view_details = True
    column_details_list = ['id', 'name', 'email', 'phone', 'service', 'message', 'status', 'notes', 'created_at']

class BlogAdminView(SecureModelView):
    column_list = ['title', 'author', 'published', 'created_at']
    column_searchable_list = ['title', 'content']
    column_filters = ['published', 'author', 'created_at']
    form_excluded_columns = ['created_at', 'updated_at']
    
    # Configure file upload field
    form_extra_fields = {
        'image_upload': FileField('Featured Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], 'Images only!')])
    }
    
    def on_model_change(self, form, model, is_created):
        # Handle file upload
        if hasattr(form, 'image_upload') and form.image_upload.data:
            file = form.image_upload.data
            if file and hasattr(file, 'filename') and file.filename:
                # Secure the filename and save
                filename = secure_filename(file.filename)
                # Add timestamp to avoid conflicts
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
                
                # Save to blog uploads folder
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'blog', filename)
                file.save(filepath)
                
                # Store relative path in database
                model.featured_image = f"uploads/blog/{filename}"
        
        super().on_model_change(form, model, is_created)

class PortfolioAdminView(SecureModelView):
    column_list = ['title', 'category', 'client', 'status', 'completion_date']
    column_searchable_list = ['title', 'description']
    column_filters = ['category', 'status', 'completion_date']

class DashboardView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))

    @expose('/')
    def index(self):
        contact_count = ContactSubmission.query.count()
        new_contacts = ContactSubmission.query.filter_by(status='new').count()
        blog_count = BlogPost.query.count()
        portfolio_count = PortfolioItem.query.count()
        
        recent_contacts = ContactSubmission.query.order_by(ContactSubmission.created_at.desc()).limit(5).all()
        
        return self.render('admin/dashboard.html', 
                         contact_count=contact_count,
                         new_contacts=new_contacts,
                         blog_count=blog_count,
                         portfolio_count=portfolio_count,
                         recent_contacts=recent_contacts)

# Initialize Admin
admin = Admin(app, name='Blackstone EG Admin', index_view=DashboardView())
admin.add_view(ContactAdminView(ContactSubmission, db.session, name='Contact Forms'))
admin.add_view(BlogAdminView(BlogPost, db.session, name='Blog Posts'))
admin.add_view(PortfolioAdminView(PortfolioItem, db.session, name='Portfolio'))
admin.add_view(SecureModelView(User, db.session, name='Users'))
admin.add_view(SecureModelView(CompanySettings, db.session, name='Settings'))

# Utility Functions
def send_email(subject, recipient, template, **kwargs):
    """Send email notification"""
    try:
        msg = Message(subject=subject, recipients=[recipient])
        msg.html = render_template(f'emails/{template}', **kwargs)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def get_company_settings():
    """Get company settings from database"""
    settings = CompanySettings.query.first()
    if not settings:
        settings = CompanySettings()
        db.session.add(settings)
        db.session.commit()
    return settings

# Sample data
services = [
    {
        'title': 'Strategic Market Access',
        'subtitle': 'Connect with high-value investment opportunities through our comprehensive market analysis and strategic facilitation services.',
        'features': [
            'In-depth market analysis and feasibility studies.',
            'Facilitation and vetting of exclusive investment opportunities.',
            'Risk assessment and mitigation strategies.',
            'Support for joint ventures and strategic partnerships.'
        ],
        'image': 'https://images.unsplash.com/39/lIZrwvbeRuuzqOoWJUEn_Photoaday_CSD%20%281%20of%201%29-5.jpg?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    },
    {
        'title': 'Government Relations',
        'subtitle': 'Benefit from elite-level engagement with key decision-makers and policy influencers for seamless regulatory navigation.',
        'features': [
            'Facilitation of high-level government meetings.',
            'Guidance on licensing, permits, and regulatory compliance.',
            'Advocacy and policy monitoring.',
            'Building and maintaining strong public-private partnerships.'
        ],
        'image': 'https://images.unsplash.com/photo-1564509116882-d206b69f76c2?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    },
    {
        'title': 'ESG Excellence',
        'subtitle': 'Facilitate sustainable investment frameworks aligned with global standards and local community impact objectives.',
        'features': [
            'Facilitation of ESG and impact investment strategies.',
            'Compliance guidance for international sustainability standards.',
            'Community engagement and social impact program design.',
            'Green energy and sustainable infrastructure project consultation.'
        ],
        'image': 'https://images.unsplash.com/photo-1591491096274-c131b36d16db?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    },
    {
        'title': 'Investor Concierge Services',
        'subtitle': 'Experience white-glove investor facilitation including logistics, secure accommodations, and personalized itinerary management.',
        'features': [
            'Executive travel and accommodation arrangements.',
            'Personalized business itineraries and meeting coordination.',
            'Secure transportation and executive protection.',
            'On-demand business support and translation services.'
        ],
        'image': 'https://images.unsplash.com/photo-1521791136064-7986c2920216?q=80&w=1169&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    }
]

team_members = [
    {
        'name': 'Teresa Nnang Avomo',
        'title': 'Directora General',
        'bio': 'Visionary leader with extensive experience in the oil and energy sector. As the first female Managing Director of GEPetrol, Teresa brings over 10 years of engineering expertise and strategic leadership in STEAM industries to drive Blackstone EG\'s consulting and facilitation initiatives.',
        'image': 'teresa.jpg'
    },
    {
        'name': 'Dionisia Alogo',
        'title': 'Encargada de Captación Comercial y Legal',
        'bio': 'Founder of ALOGO LAW FIRM, specializing in corporate law and business development. Expert in international legal standards with deep understanding of commercial frameworks that drive competitive business environments in Equatorial Guinea.',
        'image': 'dionisia.jpg'
    },
    {
        'name': 'Yvone Bekale',
        'title': 'Encargado de Captación Internacional',
        'bio': 'International business development specialist with expertise in cross-border investment facilitation. Leads strategic partnerships and investor relations across global markets, connecting international capital with African opportunities.',
        'image': 'yvone-bekale.jpg'
    },
    {
        'name': 'Rufino Esono',
        'title': 'Encargado de Operaciones de Campo e Institucionales',
        'bio': 'Operations and institutional relations expert with extensive field experience. Manages on-ground logistics, government liaisons, and ensures seamless execution of consulting projects while maintaining strong institutional partnerships.',
        'image': 'rufino-esono.jpg'
    },
    {
        'name': 'Catalina Esono Abomo',
        'title': 'Encargada de Redes Sociales y Medios Digitales',
        'bio': 'Digital marketing strategist and social media expert. Manages Blackstone EG\'s digital presence, investor communications, and multimedia content strategy to enhance market visibility and stakeholder engagement across digital platforms.',
        'image': 'catalina-esono-abomo.jpg'
    },
    {
        'name': 'Diana',
        'title': 'Encargada de Relaciones Internacionales, Visibilidad e Imagen Corporativa',
        'bio': 'International relations and corporate communications specialist. Oversees brand positioning, public relations, and corporate image management while building strategic relationships with international stakeholders and media partners.',
        'image': 'diana.jpg'
    }
]

# Routes
@app.route('/')
def home():
    settings = get_company_settings()
    recent_posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    featured_portfolio = PortfolioItem.query.filter_by(status='completed').limit(4).all()
    return render_template('enhanced/index.html', 
                         services=services[:4], 
                         settings=settings,
                         recent_posts=recent_posts,
                         featured_portfolio=featured_portfolio)

@app.route('/services')
def services_page():
    settings = get_company_settings()
    return render_template('enhanced/services.html', services=services, settings=settings)

@app.route('/team')
def team_page():
    settings = get_company_settings()
    return render_template('enhanced/team.html', team_members=team_members, settings=settings)

@app.route('/about')
def about_page():
    settings = get_company_settings()
    return render_template('enhanced/about.html', settings=settings)

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    settings = get_company_settings()
    form = ContactForm()
    
    if form.validate_on_submit():
        # Save to database
        submission = ContactSubmission(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            service=form.service.data,
            message=form.message.data
        )
        db.session.add(submission)
        db.session.commit()
        
        # Send email notification to admin
        admin_email = settings.email
        send_email(
            subject=f'New Contact Form Submission from {form.name.data}',
            recipient=admin_email,
            template='contact_notification.html',
            submission=submission
        )
        
        # Send confirmation email to user
        send_email(
            subject='Thank you for contacting Blackstone EG & Partners',
            recipient=form.email.data,
            template='contact_confirmation.html',
            name=form.name.data
        )
        
        flash('Thank you for your interest! Our investment team will contact you within 24 hours.', 'success')
        return redirect(url_for('contact_page'))
    
    return render_template('enhanced/contact.html', form=form, settings=settings)

@app.route('/blog')
def blog_page():
    settings = get_company_settings()
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False
    )
    return render_template('enhanced/blog.html', posts=posts, settings=settings)

@app.route('/blog/<slug>')
def blog_post(slug):
    settings = get_company_settings()
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    related_posts = BlogPost.query.filter(
        BlogPost.id != post.id,
        BlogPost.published == True
    ).order_by(BlogPost.created_at.desc()).limit(3).all()
    return render_template('enhanced/blog_post.html', post=post, related_posts=related_posts, settings=settings)

@app.route('/portfolio')
def portfolio_page():
    settings = get_company_settings()
    category = request.args.get('category', 'all')
    
    if category == 'all':
        projects = PortfolioItem.query.filter_by(status='completed').order_by(PortfolioItem.created_at.desc()).all()
    else:
        projects = PortfolioItem.query.filter_by(category=category, status='completed').order_by(PortfolioItem.created_at.desc()).all()
    
    categories = db.session.query(PortfolioItem.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('enhanced/portfolio.html', 
                         projects=projects, 
                         categories=categories, 
                         active_category=category,
                         settings=settings)

@app.route('/portfolio/<int:project_id>')
def portfolio_detail(project_id):
    settings = get_company_settings()
    project = PortfolioItem.query.get_or_404(project_id)
    related_projects = PortfolioItem.query.filter(
        PortfolioItem.id != project.id,
        PortfolioItem.category == project.category
    ).limit(3).all()
    return render_template('enhanced/portfolio_detail.html', 
                         project=project, 
                         related_projects=related_projects,
                         settings=settings)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_admin:
            login_user(user)
            return redirect(url_for('admin.index'))
        flash('Invalid username or password', 'error')
    
    return render_template('enhanced/admin_login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('home'))

# API endpoints for analytics
@app.route('/api/analytics/contact-stats')
@login_required
def contact_stats():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    total = ContactSubmission.query.count()
    new = ContactSubmission.query.filter_by(status='new').count()
    contacted = ContactSubmission.query.filter_by(status='contacted').count()
    closed = ContactSubmission.query.filter_by(status='closed').count()
    
    return jsonify({
        'total': total,
        'new': new,
        'contacted': contacted,
        'closed': closed
    })

# Context processors for templates
@app.context_processor
def inject_settings():
    return dict(company_settings=get_company_settings())

@app.context_processor
def inject_analytics():
    settings = get_company_settings()
    return dict(
        google_analytics_id=settings.google_analytics_id,
        facebook_pixel_id=settings.facebook_pixel_id
    )

# Error handlers
@app.errorhandler(404)
def not_found(error):
    settings = get_company_settings()
    return render_template('enhanced/404.html', settings=settings), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    settings = get_company_settings()
    return render_template('enhanced/500.html', settings=settings), 500

# Initialize database and create admin user
def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Create admin user if doesn't exist
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@blackstoneegpartners.com',
                is_admin=True
            )
            admin_user.set_password('YOUR_SECURE_PASSWORD_HERE')  # ⚠️ CHANGE THIS!
            db.session.add(admin_user)
        
        # Create sample blog posts
        if BlogPost.query.count() == 0:
            sample_posts = [
                {
                    'title': 'Investment Opportunities in Equatorial Guinea 2025',
                    'slug': 'investment-opportunities-equatorial-guinea-2025',
                    'content': '''<p>Equatorial Guinea presents unprecedented investment opportunities in 2025...</p>''',
                    'excerpt': 'Discover the latest investment opportunities in one of Africa\'s most promising markets.',
                    'author': 'Teresa Nnang Avomo',
                    'published': True,
                    'tags': 'investment, africa, opportunities'
                },
                {
                    'title': 'ESG Investing in African Markets',
                    'slug': 'esg-investing-african-markets',
                    'content': '''<p>Environmental, Social, and Governance investing is reshaping African markets...</p>''',
                    'excerpt': 'How ESG principles are driving sustainable investment in Africa.',
                    'author': 'Dionisia Alogo',
                    'published': True,
                    'tags': 'esg, sustainability, africa'
                }
            ]
            
            for post_data in sample_posts:
                post = BlogPost(**post_data)
                db.session.add(post)
        
        # Create sample portfolio items
        if PortfolioItem.query.count() == 0:
            sample_projects = [
                {
                    'title': 'Malabo Infrastructure Development',
                    'description': 'Large-scale infrastructure development project in Malabo including roads, utilities, and commercial buildings.',
                    'category': 'Infrastructure',
                    'client': 'Government of Equatorial Guinea',
                    'value': '$250M',
                    'location': 'Malabo, Equatorial Guinea',
                    'status': 'completed'
                },
                {
                    'title': 'Renewable Energy Initiative',
                    'description': 'Solar and wind energy projects across multiple locations in Equatorial Guinea.',
                    'category': 'Energy',
                    'client': 'Private Consortium',
                    'value': '$180M',
                    'location': 'Multiple Locations',
                    'status': 'completed'
                }
            ]
            
            for project_data in sample_projects:
                project = PortfolioItem(**project_data)
                db.session.add(project)
        
        db.session.commit()
        print("✅ Database initialized with sample data")
        print("🔑 Admin login: username='admin', password='admin123'")

if __name__ == '__main__':
    init_db()
    print("🚀 Starting Enhanced Blackstone EG & Partners website...")
    print("📍 Website: http://localhost:5000")
    print("🛠️ Admin Panel: http://localhost:5000/admin")
    app.run(debug=True, host='0.0.0.0', port=5000)
