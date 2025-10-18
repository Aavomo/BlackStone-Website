from flask import Flask, render_template_string

app = Flask(__name__)
app.secret_key = 'simple-dev-key'

# Inline templates to avoid file path issues
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blackstone EG & Partners</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0A0E1A 0%, #1A1D29 50%, #2D3142 100%);
            color: white;
            min-height: 100vh;
        }
        .header {
            background: rgba(5, 5, 5, 0.95);
            padding: 20px 5%;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
        }
        .logo { color: #C9A961; font-size: 1.5rem; font-weight: 700; text-decoration: none; }
        .hero {
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 40px;
        }
        .hero h1 {
            font-size: clamp(2rem, 8vw, 4rem);
            font-weight: 900;
            margin-bottom: 30px;
            background: linear-gradient(135deg, white 0%, #C9A961 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hero-subtitle {
            font-size: 1.2rem;
            margin-bottom: 40px;
            color: rgba(255, 255, 255, 0.9);
        }
        .btn {
            background: linear-gradient(135deg, #C9A961 0%, #D4B06F 100%);
            color: #0A0E1A;
            padding: 16px 40px;
            text-decoration: none;
            font-weight: 600;
            border-radius: 50px;
            display: inline-block;
            margin: 10px;
            transition: transform 0.3s ease;
        }
        .btn:hover { transform: translateY(-3px); }
        .section {
            padding: 80px 5%;
            max-width: 1200px;
            margin: 0 auto;
        }
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        .service-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        .service-card:hover { transform: translateY(-10px); }
        .service-card h3 { color: #C9A961; margin-bottom: 15px; }
        .footer {
            background: #1A1D29;
            padding: 40px 5%;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
</head>
<body>
    <header class="header">
        <a href="/" class="logo">BLACKSTONE EG & PARTNERS</a>
    </header>

    <section class="hero">
        <div>
            <h1>BLACKSTONE EG & PARTNERS</h1>
            <p class="hero-subtitle">Your Trusted Partner In Equatorial Guinea.</p>
            <a href="#services" class="btn">Explore Opportunities</a>
        </div>
    </section>

    <section class="section" id="services">
        <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 20px; color: #C9A961;">Our Services</h2>
        <p style="text-align: center; margin-bottom: 40px; color: rgba(255, 255, 255, 0.7);">
            Providing end-to-end support for sophisticated investors seeking premier opportunities in African markets.
        </p>
        
        <div class="services-grid">
            <div class="service-card">
                <h3>Strategic Market Access</h3>
                <p>Gain direct pathways to high-value investment opportunities with comprehensive due diligence.</p>
            </div>
            <div class="service-card">
                <h3>Government Relations</h3>
                <p>Elite-level engagement with key decision-makers for seamless regulatory navigation.</p>
            </div>
            <div class="service-card">
                <h3>ESG Excellence</h3>
                <p>Sustainable investment frameworks aligned with global standards and local impact.</p>
            </div>
            <div class="service-card">
                <h3>Investor Concierge</h3>
                <p>White-glove investor facilitation including logistics and personalized services.</p>
            </div>
        </div>
    </section>

    <footer class="footer">
        <p>&copy; 2025 Blackstone EG & Partners. All rights reserved.</p>
        <p style="margin-top: 10px; color: rgba(255, 255, 255, 0.5);">
            <strong>🐍 Powered by Python Flask</strong> | Empowering African Investment Excellence
        </p>
    </footer>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/test')
def test():
    return '''
    <h1>🎉 Flask is Working!</h1>
    <h2>✅ Python Version: ''' + str(__import__('sys').version) + '''</h2>
    <h2>✅ Flask is properly installed</h2>
    <p><a href="/">← Back to Website</a></p>
    '''

if __name__ == '__main__':
    print("🚀 Starting Blackstone EG & Partners website...")
    print("📍 Open your browser to: http://localhost:5000")
    print("🧪 Test page available at: http://localhost:5000/test")
    app.run(debug=True, host='0.0.0.0', port=5000)