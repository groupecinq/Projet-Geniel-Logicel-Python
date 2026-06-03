import os
import re

# 1. Update menu.html with Payment Modal
menu_path = r"c:\Users\Mel PC\Documents\projet_Dev_Log\restaurant_web\templates\menu.html"
with open(menu_path, "r", encoding="utf-8") as f:
    menu_html = f.read()

payment_modal_html = """
  <!-- Modal Paiement MTN / Orange -->
  <div class="cart-modal" id="paymentModal">
    <div class="cart-panel" style="max-width: 400px; margin: auto;">
      <div class="cart-header">
        <h3><i class="fa fa-mobile-alt"></i> Paiement Mobile</h3>
        <button id="closePayment"><i class="fa fa-times"></i></button>
      </div>
      <div style="padding: 20px;">
        <p style="margin-bottom: 15px; color: #ccc;">Veuillez entrer vos coordonnées MTN Mobile Money ou Orange Money pour valider le paiement de <strong id="payAmount"></strong>.</p>
        <div class="form-group" style="margin-bottom: 15px;">
          <label>Réseau</label>
          <select id="payNetwork" style="width: 100%; padding: 10px; border-radius: 5px; background: #333; color: white; border: 1px solid #555;">
            <option value="mtn">MTN Mobile Money</option>
            <option value="orange">Orange Money</option>
          </select>
        </div>
        <div class="form-group" style="margin-bottom: 15px;">
          <label>Numéro de téléphone</label>
          <input type="tel" id="payPhone" placeholder="Ex: 6 70 00 00 00" style="width: 100%; padding: 10px; border-radius: 5px; background: #333; color: white; border: 1px solid #555;" required/>
        </div>
        <div class="form-group" style="margin-bottom: 20px;">
          <label>Code Secret (PIN)</label>
          <input type="password" id="payPin" placeholder="••••" style="width: 100%; padding: 10px; border-radius: 5px; background: #333; color: white; border: 1px solid #555;" required/>
        </div>
        <button onclick="confirmPayment()" class="btn btn-primary" style="width: 100%; justify-content: center;">
          Valider le paiement
        </button>
      </div>
    </div>
  </div>
"""

# Insert modal before <footer class="site-footer">
if "id=\"paymentModal\"" not in menu_html:
    menu_html = menu_html.replace('<footer class="site-footer">', payment_modal_html + '\n  <footer class="site-footer">')

new_payer_commande = """
    function payerCommande() {
      {% if not user.is_authenticated %}
      window.location.href = "{% url 'login' %}";
      return;
      {% endif %}
      
      if (cart.length === 0) {
        showToast('❌ Votre panier est vide.', 'error');
        return;
      }
      // Open Payment Modal
      document.getElementById('cartModal').classList.remove('open');
      document.getElementById('paymentModal').classList.add('open');
      const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
      document.getElementById('payAmount').textContent = total.toLocaleString() + ' FCFA';
    }

    document.getElementById('closePayment').addEventListener('click', () => {
      document.getElementById('paymentModal').classList.remove('open');
    });

    function confirmPayment() {
      const phone = document.getElementById('payPhone').value;
      const pin = document.getElementById('payPin').value;
      if(!phone || !pin) {
        showToast('❌ Veuillez remplir tous les champs.', 'error');
        return;
      }
      
      showToast('✅ Paiement mobile réussi ! Commande validée.', 'success');
      cart = [];
      updateCart();
      document.getElementById('payPhone').value = '';
      document.getElementById('payPin').value = '';
      setTimeout(() => {
        document.getElementById('paymentModal').classList.remove('open');
      }, 1500);
    }
"""

if "function confirmPayment()" not in menu_html:
    # We replace the old payerCommande
    old_payer = """    function payerCommande() {
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
    }"""
    if old_payer in menu_html:
        menu_html = menu_html.replace(old_payer, new_payer_commande)
    else:
        # regex replace
        menu_html = re.sub(r'function payerCommande\(\) \{.*?\n    \}', new_payer_commande, menu_html, flags=re.DOTALL)

with open(menu_path, "w", encoding="utf-8") as f:
    f.write(menu_html)


# 2. Update login.html to clear autocomplete
login_path = r"c:\Users\Mel PC\Documents\projet_Dev_Log\restaurant_web\templates\login.html"
with open(login_path, "r", encoding="utf-8") as f:
    login_html = f.read()

# adding autocomplete off
if 'autocomplete="off"' not in login_html:
    login_html = login_html.replace('<form id="loginForm" class="auth-form" method="POST" action="{% url \'login\' %}">', '<form id="loginForm" class="auth-form" method="POST" action="{% url \'login\' %}" autocomplete="off">')
    login_html = login_html.replace('id="loginEmail" name="username"', 'id="loginEmail" name="username" autocomplete="new-password" value=""')
    login_html = login_html.replace('id="loginPassword" name="password"', 'id="loginPassword" name="password" autocomplete="new-password" value=""')

with open(login_path, "w", encoding="utf-8") as f:
    f.write(login_html)

print("Payment modal and autocomplete off added.")
