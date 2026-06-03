import os

# 1. Update login.html
login_path = r"c:\Users\Mel PC\Documents\projet_Dev_Log\restaurant_web\templates\login.html"
with open(login_path, "r", encoding="utf-8") as f:
    login_html = f.read()

# Replace the login form opening
old_form = '<form id="loginForm" class="auth-form" onsubmit="handleLogin(event)">'
new_form = '<form id="loginForm" class="auth-form" method="POST" action="{% url \'login\' %}">\n      {% csrf_token %}\n      {% if error %}<p style="color:red;text-align:center;">{{ error }}</p>{% endif %}'
login_html = login_html.replace(old_form, new_form)

# Add name="username" to email input
old_email_input = '<input type="email" id="loginEmail" placeholder="votre@email.com" required/>'
new_email_input = '<input type="text" id="loginEmail" name="username" placeholder="Nom d\'utilisateur ou Email" required/>'
login_html = login_html.replace(old_email_input, new_email_input)

# Add name="password" to password input
old_pass_input = '<input type="password" id="loginPassword" placeholder="••••••••" required/>'
new_pass_input = '<input type="password" id="loginPassword" name="password" placeholder="••••••••" required/>'
login_html = login_html.replace(old_pass_input, new_pass_input)

# Remove handleLogin preventDefault/redirect in JS
old_handle_login = "function handleLogin(e) {"
new_handle_login = "function handleLogin(e) { return true; "
login_html = login_html.replace(old_handle_login, new_handle_login)

# Remove the line with preventDefault in handleLogin if it exists
login_html = login_html.replace("e.preventDefault();\n      const role", "const role")

# Change the login button type
old_btn = '<button type="submit" class="btn btn-primary btn-block">Se Connecter</button>'
# Wait, let's just make sure we don't mess up the button. I'll leave it as is, it's type="submit".

with open(login_path, "w", encoding="utf-8") as f:
    f.write(login_html)


# 2. Update menu.html
menu_path = r"c:\Users\Mel PC\Documents\projet_Dev_Log\restaurant_web\templates\menu.html"
with open(menu_path, "r", encoding="utf-8") as f:
    menu_html = f.read()

# Replace the checkout button logic
old_btn_checkout = '<a href="{% url \'login\' %}" class="btn btn-primary" style="width:100%;justify-content:center;margin-top:16px;">\n        <i class="fa fa-lock"></i> Confirmer la commande\n      </a>'
new_btn_checkout = """
      {% if user.is_authenticated %}
      <button onclick="payerCommande()" class="btn btn-primary" style="width:100%;justify-content:center;margin-top:16px;">
        <i class="fa fa-credit-card"></i> Payer la commande
      </button>
      {% else %}
      <a href="{% url 'login' %}" class="btn btn-primary" style="width:100%;justify-content:center;margin-top:16px;">
        <i class="fa fa-lock"></i> Se connecter pour payer
      </a>
      {% endif %}
"""

if old_btn_checkout in menu_html:
    menu_html = menu_html.replace(old_btn_checkout, new_btn_checkout)
else:
    # Let's try a regex or simpler replace if indentation is different
    import re
    menu_html = re.sub(r'<a href="\{% url \'login\' %\}".*?Confirmer la commande.*?</a>', new_btn_checkout, menu_html, flags=re.DOTALL)

# Add payerCommande JS function
if "function payerCommande()" not in menu_html:
    js_func = """
    function payerCommande() {
      if (cart.length === 0) {
        showToast('❌ Votre panier est vide.');
        return;
      }
      showToast('✅ Paiement réussi ! Commande validée.');
      cart = [];
      updateCart();
      setTimeout(() => {
        document.getElementById('cartModal').classList.remove('open');
      }, 2000);
    }
    </script>"""
    menu_html = menu_html.replace("</script>", js_func)

with open(menu_path, "w", encoding="utf-8") as f:
    f.write(menu_html)

print("Auth and Cart UI updated.")
