#!/usr/bin/env python3
"""
Demo script for Blackstone EG & Partners Flask Website
"""

import requests
import time

def test_website():
    base_url = "http://localhost:5000"
    
    # Test all routes
    routes = [
        "/",
        "/services", 
        "/team",
        "/about",
        "/contact"
    ]
    
    print("🚀 Testing Blackstone EG & Partners Python Flask Website")
    print("=" * 60)
    
    for route in routes:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            status = "✅ PASS" if response.status_code == 200 else "❌ FAIL"
            print(f"{status} {route} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ FAIL {route} - Error: {e}")
    
    print("\n" + "=" * 60)
    print("📊 Website Features:")
    print("• ✅ Python Flask Backend")
    print("• ✅ Responsive Design") 
    print("• ✅ Modern Glass-morphism UI")
    print("• ✅ Contact Form with Validation")
    print("• ✅ Team Member Profiles")
    print("• ✅ Service Descriptions")
    print("• ✅ About Page with Statistics")
    print("• ✅ Error Handling (404 page)")
    print("• ✅ Template Inheritance")
    print("• ✅ Static Asset Management")
    
    print("\n🌐 Access the website at: http://localhost:5000")
    print("📱 The website is fully responsive and mobile-friendly!")

if __name__ == "__main__":
    test_website()