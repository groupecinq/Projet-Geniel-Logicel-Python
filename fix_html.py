import os
import re

html_dir = r"c:\Users\Mel PC\Documents\projet_Dev_Log\restaurant_web\templates"

for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(html_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Add {% load static %} if not present
        if '{% load static %}' not in content:
            content = '{% load static %}\n' + content
            
        # Replace href="style.css" etc with {% static 'style.css' %}
        content = re.sub(r'href="([^"]+\.css)"', r'href="{% static \'\1\' %}"', content)
        
        # Replace src="images/..." with src="{% static 'images/...' %}"
        content = re.sub(r'src="([^"]+\.(png|jpg|jpeg|svg|gif))"', r'src="{% static \'\1\' %}"', content)
        
        # Replace href="index.html" with {% url 'home' %}
        content = re.sub(r'href="index\.html"', r'href="{% url \'home\' %}"', content)
        content = re.sub(r'href="menu\.html"', r'href="{% url \'menu\' %}"', content)
        content = re.sub(r'href="about\.html"', r'href="{% url \'about\' %}"', content)
        content = re.sub(r'href="contact\.html"', r'href="{% url \'contact\' %}"', content)
        content = re.sub(r'href="login\.html"', r'href="{% url \'login\' %}"', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
print("HTML files updated with Django tags.")
