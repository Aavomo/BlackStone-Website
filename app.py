from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)

# More secure secret key generation
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production-12345')

# Sample data
team_members = [
    {
        'name': 'Teresa Nnang Avomo',
        'title': 'Directora General',
        'bio': 'Visionary leader with extensive experience in the oil and energy sector. As the first female Managing Director of GEPetrol, Teresa brings over 10 years of engineering expertise and strategic leadership in STEAM industries to drive Blackstone EG\'s investment initiatives.',
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
        'bio': 'Operations and institutional relations expert with extensive field experience. Manages on-ground logistics, government liaisons, and ensures seamless execution of investment projects while maintaining strong institutional partnerships.',
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

services = [
    {
        'title': 'Strategic Market Access',
        'subtitle': 'Gain direct pathways to high-value investment opportunities with our comprehensive due diligence and unparalleled market intelligence.',
        'features': [
            'In-depth market analysis and feasibility studies.',
            'Identification and vetting of exclusive investment projects.',
            'Risk assessment and mitigation strategies.',
            'Support for joint ventures and strategic alliances.'
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
        'subtitle': 'Implement sustainable investment frameworks aligned with global standards and local community impact objectives.',
        'features': [
            'Development of ESG and impact investment strategies.',
            'Compliance with international sustainability reporting standards.',
            'Community engagement and social impact program design.',
            'Green energy and sustainable infrastructure project advisory.'
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

@app.route('/')
def home():
    return render_template('index.html', services=services[:4])  # Show first 4 services on home

@app.route('/services')
def services_page():
    return render_template('services.html', services=services)

@app.route('/team')
def team_page():
    return render_template('team.html', team_members=team_members)

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        # Process form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')
        
        # In a real application, you would save this to a database or send an email
        print(f"Contact form submission:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Service: {service}")
        print(f"Message: {message}")
        print(f"Timestamp: {datetime.now()}")
        
        flash('Thank you for your interest! Our investment team will contact you within 24 hours to discuss exclusive opportunities.', 'success')
        return redirect(url_for('contact_page'))
    
    return render_template('contact.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
