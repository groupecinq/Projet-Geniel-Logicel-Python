import os

login_path = r"c:\Users\Mel PC\Documents\projet_Dev_Log\restaurant_web\templates\login.html"
with open(login_path, "r", encoding="utf-8") as f:
    login_html = f.read()

# Register Form autocomplete
login_html = login_html.replace(
    '<form id="registerForm" class="auth-form hidden" onsubmit="handleRegister(event)">',
    '<form id="registerForm" class="auth-form hidden" onsubmit="handleRegister(event)" autocomplete="off">'
)

login_html = login_html.replace(
    '<input type="email" id="regEmail" placeholder="votre@email.com" required />',
    '<input type="email" id="regEmail" placeholder="votre@email.com" autocomplete="new-password" value="" required />'
)

login_html = login_html.replace(
    '<input type="password" id="regPass" placeholder="••••••••" required />',
    '<input type="password" id="regPass" placeholder="••••••••" autocomplete="new-password" value="" required />'
)

with open(login_path, "w", encoding="utf-8") as f:
    f.write(login_html)
