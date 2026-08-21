"""
pages/Terminos.py — Página de Términos de Uso del dashboard.

CÓMO USAR ESTE ARCHIVO
-----------------------
1. Genera tus términos de uso en TermsFeed:
   https://www.termsfeed.com/terms-service-generator/
   (gratis — rellena: nombre del servicio "HabitTracker Bot", qué es
   (bot de Telegram + dashboard web), país España, planes Free/Pro,
   precios 4,99€/mes o 39€/año y $5.99/$45 en dólares, trial gratis de
   7 días, cancelación y renovación automática vía Stripe).

2. Copia el texto/HTML resultante y pégalo reemplazando la variable
   TEXTO_TERMINOS de más abajo (entre las tres comillas). Puedes pegar
   HTML tal cual — esta página ya lo renderiza como HTML.

3. Sube este archivo dentro de la misma carpeta "pages" del repo de
   GitHub del dashboard, junto a Privacidad.py.

4. Al hacer push, Streamlit Cloud redespliega solo. La URL final va a
   ser algo como:
   https://habittracker-dashboard.streamlit.app/Terminos

Este archivo es independiente del resto del dashboard (no importa nada
de db.py ni de Supabase) — es solo una página de texto.
"""

import streamlit as st

st.set_page_config(page_title="Términos de Uso", page_icon="📄", layout="centered", initial_sidebar_state="expanded")

# -------------------------------------------------------------
# PEGA AQUÍ el texto/HTML que te genere TermsFeed, reemplazando todo
# este contenido de ejemplo entre las tres comillas.
# -------------------------------------------------------------
TEXTO_TERMINOS = """
<h2>Terms and Conditions</h2>
<p><em>Last updated: August 21, 2026</em></p>
<p>Please read these terms and conditions carefully before using Our Service.</p>

<h3>Interpretation and Definitions</h3>
<h4>Interpretation</h4>
<p>The words whose initial letters are capitalized have meanings defined under the following conditions. The following definitions shall have the same meaning regardless of whether they appear in singular or in plural.</p>

<h4>Definitions</h4>
<p>For the purposes of these Terms and Conditions:</p>
<ul>
<li><strong>Application</strong> means the HabitTracker Bot software, made available by the Company through the Telegram messaging platform and its accompanying web dashboard.</li>
<li><strong>Affiliate</strong> means an entity that controls, is controlled by, or is under common control with a party, where "control" means ownership of 50% or more of the shares, equity interest or other securities entitled to vote for election of directors or other managing authority.</li>
<li><strong>Country</strong> refers to: Spain</li>
<li><strong>Company</strong> (referred to as either "the Company", "We", "Us" or "Our" in these Terms and Conditions) refers to HabitTracker Bot.</li>
<li><strong>Device</strong> means any device that can access the Service such as a computer, a cell phone or a digital tablet.</li>
<li><strong>Service</strong> refers to the Application or the Website or both.</li>
<li><strong>Terms and Conditions</strong> (also referred to as "Terms") means these Terms and Conditions, which govern Your access to and use of the Service and form the entire agreement between You and the Company regarding the Service.</li>
<li><strong>Third-Party Social Media Service</strong> means any services or content (including data, information, products or services) provided by a third party that is displayed, included, made available, or linked to through the Service.</li>
<li><strong>Website</strong> refers to HabitTracker Bot, accessible from <a href="https://habittracker-dashboard.streamlit.app">https://habittracker-dashboard.streamlit.app</a></li>
<li><strong>You</strong> means the individual accessing or using the Service.</li>
</ul>

<h3>Acknowledgment</h3>
<p>These are the Terms and Conditions governing the use of this Service and the agreement between You and the Company. These Terms and Conditions set out the rights and obligations of all users regarding the use of the Service.</p>
<p>Your access to and use of the Service is conditioned on Your acceptance of and compliance with these Terms and Conditions. These Terms and Conditions apply to all visitors, users and others who access or use the Service.</p>
<p>By accessing or using the Service You agree to be bound by these Terms and Conditions. If You disagree with any part of these Terms and Conditions then You may not access the Service.</p>
<p>You represent that you are over the age of 18. The Company does not permit those under 18 to use the Service.</p>
<p>Your access to and use of the Service is also subject to Our Privacy Policy, which describes how We collect, use, and disclose personal information. Please read Our Privacy Policy carefully before using Our Service.</p>

<h3>Accounts</h3>
<p>The Service does not use a traditional registration process with a username and password. Your access is identified through your Telegram account when You interact with our Telegram bot, and through a private access link when using the web dashboard. You are responsible for safeguarding access to your own Telegram account, as any activity carried out through it is treated as authorized by You.</p>
<p>You may request the deletion of your account and all associated data at any time using the <code>/borrar_cuenta</code> (or <code>/deleteaccount</code>) command within the bot. See Our Privacy Policy for details on what this deletes.</p>

<h3>Subscriptions</h3>
<p>The Service offers a free plan ("Free") and a paid plan ("Pro"). The Free plan includes a limited set of features at no cost. The Pro plan unlocks additional features and is billed on a recurring basis, either monthly or annually, at the price displayed within the bot at the time of purchase, in euros (EUR) or US dollars (USD) depending on the currency You select.</p>
<p>New users may be eligible for a one-time free trial period of the Pro plan (currently 7 days), available only once per user.</p>
<p>Payments are processed securely by Stripe, a third-party payment processor. We do not store your full payment card details on our own servers.</p>
<p>Unless You cancel, your Pro subscription will automatically renew at the end of each billing period (monthly or annually, as applicable) at the then-current price, and Stripe will automatically charge the payment method on file.</p>
<p>You may cancel your subscription at any time from within the bot. If You cancel, You will keep access to Pro features until the end of the current billing period, after which your account will revert to the Free plan. Cancelling does not entitle You to a refund for the current billing period, except where required by applicable law.</p>
<p>Deleting your account with <code>/borrar_cuenta</code> cancels any active subscription immediately, rather than waiting for the end of the billing period.</p>

<h3>Links to Other Websites</h3>
<p>Our Service may contain links to third-party websites or services that are not owned or controlled by the Company.</p>
<p>The Company has no control over, and assumes no responsibility for, the content, privacy policies, or practices of any third-party websites or services. You further acknowledge and agree that the Company shall not be responsible or liable, directly or indirectly, for any damage or loss caused or alleged to be caused by or in connection with the use of or reliance on any such content, goods or services available on or through any such websites or services.</p>
<p>We strongly advise You to read the terms and conditions and privacy policies of any third-party websites or services that You visit.</p>

<h4>Links from a Third-Party Social Media Service</h4>
<p>The Service may display, include, make available, or link to content or services provided by a Third-Party Social Media Service. A Third-Party Social Media Service is not owned or controlled by the Company, and the Company does not endorse or assume responsibility for any Third-Party Social Media Service.</p>
<p>You acknowledge and agree that the Company shall not be responsible or liable, directly or indirectly, for any damage or loss caused or alleged to be caused by or in connection with Your access to or use of any Third-Party Social Media Service, including any content, goods, or services made available through them. Your use of any Third-Party Social Media Service is governed by that Third-Party Social Media Service's terms and privacy policies.</p>

<h3>Termination</h3>
<p>We may terminate or suspend Your access immediately, without prior notice or liability, for any reason whatsoever, including without limitation if You breach these Terms and Conditions.</p>
<p>Upon termination, Your right to use the Service will cease immediately.</p>

<h3>Limitation of Liability</h3>
<p>Notwithstanding any damages that You might incur, the entire liability of the Company and any of its suppliers under any provision of these Terms and Your exclusive remedy for all of the foregoing shall be limited to the amount actually paid by You through the Service, or 100 USD if You haven't purchased anything through the Service.</p>
<p>To the maximum extent permitted by applicable law, in no event shall the Company or its suppliers be liable for any special, incidental, indirect, or consequential damages whatsoever (including, but not limited to, damages for loss of profits, loss of data or other information, for business interruption, for personal injury, loss of privacy arising out of or in any way related to the use of or inability to use the Service, third-party software and/or third-party hardware used with the Service, or otherwise in connection with any provision of these Terms), even if the Company or any supplier has been advised of the possibility of such damages and even if the remedy fails of its essential purpose.</p>
<p>Some states do not allow the exclusion of implied warranties or limitation of liability for incidental or consequential damages, which means that some of the above limitations may not apply. In these states, each party's liability will be limited to the greatest extent permitted by law.</p>

<h3>"AS IS" and "AS AVAILABLE" Disclaimer</h3>
<p>The Service is provided to You "AS IS" and "AS AVAILABLE" and with all faults and defects without warranty of any kind. To the maximum extent permitted under applicable law, the Company, on its own behalf and on behalf of its Affiliates and its and their respective licensors and service providers, expressly disclaims all warranties, whether express, implied, statutory or otherwise, with respect to the Service, including all implied warranties of merchantability, fitness for a particular purpose, title and non-infringement, and warranties that may arise out of course of dealing, course of performance, usage or trade practice. Without limitation to the foregoing, the Company provides no warranty or undertaking, and makes no representation of any kind that the Service will meet Your requirements, achieve any intended results, be compatible or work with any other software, applications, systems or services, operate without interruption, meet any performance or reliability standards or be error free or that any errors or defects can or will be corrected.</p>
<p>Without limiting the foregoing, neither the Company nor any of the Company's providers makes any representation or warranty of any kind, express or implied: (i) as to the operation or availability of the Service, or the information, content, and materials or products included thereon; (ii) that the Service will be uninterrupted or error-free; (iii) as to the accuracy, reliability, or currency of any information or content provided through the Service; or (iv) that the Service, its servers, the content, or e-mails sent from or on behalf of the Company are free of viruses, scripts, trojan horses, worms, malware, timebombs or other harmful components.</p>
<p>Some jurisdictions do not allow the exclusion of certain types of warranties or limitations on applicable statutory rights of a consumer, so some or all of the above exclusions and limitations may not apply to You. But in such a case the exclusions and limitations set forth in this section shall be applied to the greatest extent enforceable under applicable law.</p>

<h3>Governing Law</h3>
<p>The laws of Spain, excluding its conflicts of law rules, shall govern these Terms and Your use of the Service. Your use of the Application may also be subject to other local, state, national, or international laws.</p>

<h3>Disputes Resolution</h3>
<p>If You have any concern or dispute about the Service, You agree to first try to resolve the dispute informally by contacting the Company.</p>

<h3>For European Union (EU) Users</h3>
<p>If You are a European Union consumer, you will benefit from any mandatory provisions of the law of the country in which You are resident.</p>

<h3>United States Legal Compliance</h3>
<p>You represent and warrant that (i) You are not located in a country that is subject to the United States government embargo, or that has been designated by the United States government as a "terrorist supporting" country, and (ii) You are not listed on any United States government list of prohibited or restricted parties.</p>

<h3>Severability and Waiver</h3>
<h4>Severability</h4>
<p>If any provision of these Terms is held to be unenforceable or invalid, such provision will be changed and interpreted to accomplish the objectives of such provision to the greatest extent possible under applicable law and the remaining provisions will continue in full force and effect.</p>
<h4>Waiver</h4>
<p>Except as provided herein, the failure to exercise a right or to require performance of an obligation under these Terms shall not affect a party's ability to exercise such right or require such performance at any time thereafter nor shall the waiver of a breach constitute a waiver of any subsequent breach.</p>

<h3>Translation Interpretation</h3>
<p>These Terms and Conditions may have been translated if We have made them available to You on our Service. You agree that the original English text shall prevail in the case of a dispute.</p>

<h3>Changes to These Terms and Conditions</h3>
<p>We reserve the right, at Our sole discretion, to modify or replace these Terms at any time. If a revision is material We will make reasonable efforts to provide at least 30 days' notice prior to any new terms taking effect. What constitutes a material change will be determined at Our sole discretion.</p>
<p>By continuing to access or use Our Service after those revisions become effective, You agree to be bound by the revised terms. If You do not agree to the new terms, in whole or in part, please stop using the Service.</p>

<h3>Contact Us</h3>
<p>If you have any questions about these Terms and Conditions, You can contact us by email: <a href="mailto:marcoscas1508@gmail.com">marcoscas1508@gmail.com</a></p>
"""

CSS = """
<style>
    .stApp { background: #0f0f22; color: #e5e5f0; }
    .legal-box {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 2rem 2.2rem;
        line-height: 1.65;
    }
    .legal-box h1, .legal-box h2, .legal-box h3, .legal-box h4 {
        background: linear-gradient(135deg, #a78bfa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .legal-box a { color: #34d399; }
    .legal-box code {
        background: rgba(255,255,255,0.08);
        padding: 0.1rem 0.35rem;
        border-radius: 4px;
    }

    /* ---------- Menú lateral (páginas: dashboard / Privacidad / Terminos) ---------- */
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    [data-testid="stSidebar"] {
        background: #12122a;
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebarNav"] {
        padding-top: 1.2rem;
    }
    [data-testid="stSidebarNav"] a {
        color: #cfcfe6 !important;
        border-radius: 10px;
        padding: 0.55rem 0.9rem !important;
        margin: 0.15rem 0.7rem;
        font-weight: 500;
        transition: background 0.15s ease, color 0.15s ease;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(167,139,250,0.18);
        color: #ffffff !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(135deg, rgba(124,58,237,0.35), rgba(52,211,153,0.20));
        color: #ffffff !important;
    }
    /* Menú siempre visible (ver initial_sidebar_state="expanded" arriba):
       quitamos el botón de colapsar, que era poco fiable. */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="baseButton-headerNoPadding"] {
        display: none !important;
    }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# Botón para abrir/cerrar el menú lateral. Sin CSS raro, sin JavaScript,
# sin posicionamiento fijo — un botón de Streamlit normal y corriente,
# arriba del todo de la página.
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True
if st.button("☰ Abrir/cerrar menú (dashboard, Privacidad...)", key="toggle_menu_btn"):
    st.session_state.sidebar_open = not st.session_state.sidebar_open
if not st.session_state.sidebar_open:
    st.markdown(
        '<style>[data-testid="stSidebar"] { display: none !important; }</style>',
        unsafe_allow_html=True,
    )

st.markdown(f'<div class="legal-box">{TEXTO_TERMINOS}</div>', unsafe_allow_html=True)
