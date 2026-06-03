import os
import re

html_dir = r"c:\Users\Mel PC\Documents\projet_Dev_Log\restaurant_web\templates"

for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(html_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Fix backslash quotes
        content = content.replace(r"\'", "'")
        
        # Fix external URLs that were accidentally templated
        content = re.sub(r"\{% static '(https?://.*?)' %\}", r"\1", content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
print("Fixed quotes and external URLs.")
