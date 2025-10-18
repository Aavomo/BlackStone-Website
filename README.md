# Blackstone EG & Partners - Python Flask Website

A modern, responsive website for Blackstone EG & Partners built with Python Flask.

## Features

- **Python Flask Backend**: Clean, maintainable Python web application
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI**: Glass-morphism design with smooth animations
- **Contact Form**: Functional contact form with form validation
- **Template Engine**: Uses Jinja2 for dynamic content rendering
- **Professional Layout**: Services, Team, About, and Contact sections

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/
│   └── css/
│       └── style.css     # Stylesheet
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── services.html     # Services page
│   ├── team.html         # Team page
│   ├── about.html        # About page
│   ├── contact.html      # Contact page
│   └── 404.html          # Error page
└── README.md             # This file
```

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Open your browser** and visit:
   ```
   http://localhost:5000
   ```

## Development

### Adding New Pages

1. Create a new route in `app.py`:
   ```python
   @app.route('/new-page')
   def new_page():
       return render_template('new-page.html')
   ```

2. Create the template file in `templates/new-page.html`:
   ```html
   {% extends "base.html" %}
   
   {% block content %}
   <!-- Your content here -->
   {% endblock %}
   ```

### Customizing Data

- **Team Members**: Edit the `team_members` list in `app.py`
- **Services**: Modify the `services` list in `app.py`
- **Contact Information**: Update contact details in `templates/contact.html`

### Styling

- Main styles are in `static/css/style.css`
- CSS variables for colors are defined in `:root`
- Responsive breakpoints are handled with media queries

## Configuration

### Environment Variables

For production deployment, set these environment variables:

- `FLASK_ENV=production`
- `SECRET_KEY=your-secure-secret-key`

### Database Integration

To add database functionality:

1. Install Flask-SQLAlchemy:
   ```bash
   pip install Flask-SQLAlchemy
   ```

2. Add database models to `app.py`
3. Update the contact form to save to database

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

For production, consider using:
- **Gunicorn** as WSGI server
- **Nginx** as reverse proxy
- **Docker** for containerization

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Features in Detail

### Contact Form
- Form validation
- Flash messages for user feedback
- Form data logging (console output)
- Ready for email integration

### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Optimized for all screen sizes

### Modern UI Elements
- Glass-morphism design
- Smooth hover animations
- Professional color scheme
- High-quality background images

## Browser Support

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## License

© 2025 Blackstone EG & Partners. All rights reserved.
