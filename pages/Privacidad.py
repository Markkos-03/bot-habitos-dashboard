"""
pages/Privacidad.py — Página de Política de Privacidad del dashboard.

CÓMO USAR ESTE ARCHIVO
-----------------------
1. Genera tu política de privacidad en Termly:
   https://termly.io/products/privacy-policy-generator/
   (cuenta gratis, sin tarjeta — sigue el cuestionario indicando que es
   un bot de Telegram + dashboard web, ubicación España/UE, qué datos
   recoges, y que usas Stripe como procesador de pagos externo).

2. Copia el texto/HTML que te da Termly y pégalo reemplazando la
   variable TEXTO_POLITICA de más abajo (entre las tres comillas).
   Puedes pegar HTML tal cual (Termly lo da en ese formato) — esta
   página ya lo renderiza como HTML, no hace falta convertirlo a nada.

3. Sube este archivo dentro de una carpeta llamada "pages" en el mismo
   repositorio de GitHub donde ya tienes tu dashboard.py (Streamlit
   detecta automáticamente cualquier archivo .py que pongas ahí y crea
   una página nueva sola, con su propio enlace).

4. Cuando hagas push, Streamlit Cloud redespliega solo. La URL final va
   a ser algo como:
   https://habittracker-dashboard.streamlit.app/Privacidad

Este archivo es independiente del resto del dashboard (no importa nada
de db.py ni de Supabase) — es solo una página de texto, no necesita
conectarse a ninguna base de datos.
"""

import streamlit as st

st.set_page_config(page_title="Política de Privacidad", page_icon="🔒", layout="centered", initial_sidebar_state="expanded")

# -------------------------------------------------------------
# PEGA AQUÍ el texto/HTML que te genere Termly, reemplazando todo
# este contenido de ejemplo entre las tres comillas.
# -------------------------------------------------------------
TEXTO_POLITICA = """
<h2>PRIVACY POLICY</h2>
<p><em>Last updated August 21, 2026</em></p>

<p>This Privacy Notice for Marcos Pinto (doing business as <strong>HabitTracker Bot</strong>) ("we," "us," or "our"), describes how and why we might access, collect, store, use, and/or share ("process") your personal information when you use our services ("Services"), including when you:</p>
<ul>
<li>Visit our website at <a href="https://habittracker-dashboard.streamlit.app">https://habittracker-dashboard.streamlit.app</a> or any website of ours that links to this Privacy Notice</li>
<li>Download and use our mobile application (Telegram), or any other application of ours that links to this Privacy Notice</li>
<li>Engage with us in other related ways, including any marketing or events</li>
</ul>

<p><strong>Questions or concerns?</strong> Reading this Privacy Notice will help you understand your privacy rights and choices. We are responsible for making decisions about how your personal information is processed. If you do not agree with our policies and practices, please do not use our Services. If you still have any questions or concerns, please contact us at <a href="mailto:marcoscas1508@gmail.com">marcoscas1508@gmail.com</a>.</p>

<h3>SUMMARY OF KEY POINTS</h3>
<p><em>This summary provides key points from our Privacy Notice, but you can find out more details about any of these topics in the table of contents below.</em></p>

<p><strong>What personal information do we process?</strong> When you use our Services, we may process personal information depending on how you interact with us and the Services, the choices you make, and the products and features you use.</p>

<p><strong>Do we process any sensitive personal information?</strong> Some information may be considered "special" or "sensitive" in certain jurisdictions, for example your racial or ethnic origins, sexual orientation, and religious beliefs. We do not process sensitive personal information.</p>

<p><strong>Do we collect any information from third parties?</strong> We do not collect any information from third parties.</p>

<p><strong>How do we process your information?</strong> We process your information to provide, improve, and administer our Services, communicate with you, for security and fraud prevention, and to comply with law. We may also process your information for other purposes with your consent. We process your information only when we have a valid legal reason to do so.</p>

<p><strong>In what situations and with which parties do we share personal information?</strong> We may share information in specific situations and with specific third parties (see below).</p>

<p><strong>How do we keep your information safe?</strong> We have adequate organizational and technical processes and procedures in place to protect your personal information. However, no electronic transmission over the internet or information storage technology can be guaranteed to be 100% secure, so we cannot promise or guarantee that hackers, cybercriminals, or other unauthorized third parties will not be able to defeat our security and improperly collect, access, steal, or modify your information.</p>

<p><strong>What are your rights?</strong> Depending on where you are located geographically, the applicable privacy law may mean you have certain rights regarding your personal information.</p>

<p><strong>How do you exercise your rights?</strong> The easiest way to exercise your rights is by visiting <a href="https://t.me/TrackerHabitFutureBot">https://t.me/TrackerHabitFutureBot</a>, or by contacting us. We will consider and act upon any request in accordance with applicable data protection laws.</p>

<h3>TABLE OF CONTENTS</h3>
<ol>
<li>What information do we collect?</li>
<li>How do we process your information?</li>
<li>What legal bases do we rely on to process your personal information?</li>
<li>When and with whom do we share your personal information?</li>
<li>How do we handle your social logins?</li>
<li>How long do we keep your information?</li>
<li>How do we keep your information safe?</li>
<li>Do we collect information from minors?</li>
<li>What are your privacy rights?</li>
<li>Controls for Do-Not-Track features</li>
<li>Do United States residents have specific privacy rights?</li>
<li>Do we make updates to this notice?</li>
<li>How can you contact us about this notice?</li>
<li>How can you review, update, or delete the data we collect from you?</li>
</ol>

<h3>1. WHAT INFORMATION DO WE COLLECT?</h3>
<p><strong>Personal information you disclose to us</strong></p>
<p><em>In Short: We collect personal information that you provide to us.</em></p>
<p>We collect personal information that you voluntarily provide to us when you express an interest in obtaining information about us or our products and Services, when you participate in activities on the Services, or otherwise when you contact us. The personal information we collect may include the following:</p>
<ul>
<li>Telegram user ID</li>
<li>Self-reported habit and goal data</li>
<li>Workout data synced from Hevy (exercises, sets, weight, reps)</li>
<li>Saved quotes</li>
<li>Language preference</li>
</ul>

<p><strong>Sensitive Information.</strong> We do not process sensitive information.</p>

<p><strong>Payment Data.</strong> We may collect data necessary to process your payment if you choose to make purchases, such as your payment instrument number and the security code associated with your payment instrument. All payment data is handled and stored by Stripe, not by us. You may find their privacy notice here: <a href="https://stripe.com/privacy">https://stripe.com/privacy</a>.</p>

<p>All personal information that you provide to us must be true, complete, and accurate, and you must notify us of any changes to such personal information.</p>

<h3>2. HOW DO WE PROCESS YOUR INFORMATION?</h3>
<p><em>In Short: We process your information to provide, improve, and administer our Services, communicate with you, for security and fraud prevention, and to comply with law. We may also process your information for other purposes only with your prior explicit consent.</em></p>
<p>We process your personal information for a variety of reasons, depending on how you interact with our Services, including to save or protect an individual's vital interest, such as to prevent harm.</p>

<h3>3. WHAT LEGAL BASES DO WE RELY ON TO PROCESS YOUR INFORMATION?</h3>
<p><em>In Short: We only process your personal information when we believe it is necessary and we have a valid legal reason (i.e., legal basis) to do so under applicable law, like with your consent, to comply with laws, to provide you with services to enter into or fulfill our contractual obligations, to protect your rights, or to fulfill our legitimate business interests.</em></p>

<p><strong>If you are located in the EU or UK, this section applies to you.</strong> The General Data Protection Regulation (GDPR) and UK GDPR require us to explain the valid legal bases we rely on in order to process your personal information. As such, we may rely on the following legal bases:</p>
<ul>
<li><strong>Consent.</strong> We may process your information if you have given us permission (i.e., consent) to use your personal information for a specific purpose. You can withdraw your consent at any time.</li>
<li><strong>Legal Obligations.</strong> We may process your information where we believe it is necessary for compliance with our legal obligations, such as to cooperate with a law enforcement body or regulatory agency, exercise or defend our legal rights, or disclose your information as evidence in litigation in which we are involved.</li>
<li><strong>Vital Interests.</strong> We may process your information where we believe it is necessary to protect your vital interests or the vital interests of a third party, such as situations involving potential threats to the safety of any person.</li>
</ul>

<p><strong>If you are located in Canada, this section applies to you.</strong> We may process your information if you have given us specific permission (i.e., express consent) to use your personal information for a specific purpose, or in situations where your permission can be inferred (i.e., implied consent). You can withdraw your consent at any time. In some exceptional cases, we may be legally permitted under applicable law to process your information without your consent, including, for example: if collection is clearly in the interests of an individual and consent cannot be obtained in a timely way; for investigations and fraud detection and prevention; for business transactions provided certain conditions are met; if disclosure is required to comply with a subpoena, warrant, court order, or rules of the court; or if the information is publicly available and is specified by the regulations.</p>

<h3>4. WHEN AND WITH WHOM DO WE SHARE YOUR PERSONAL INFORMATION?</h3>
<p><em>In Short: We may share information in specific situations described in this section and/or with the following third parties.</em></p>
<p><strong>Business Transfers.</strong> We may share or transfer your information in connection with, or during negotiations of, any merger, sale of company assets, financing, or acquisition of all or a portion of our business to another company.</p>

<h3>5. HOW DO WE HANDLE YOUR SOCIAL LOGINS?</h3>
<p><em>In Short: We do not offer registration or login via third-party social media accounts.</em></p>
<p>Our Services do not currently offer the option to register or log in using a third-party social media account (such as Facebook or X). If this changes in the future, we will update this Privacy Notice accordingly.</p>

<h3>6. HOW LONG DO WE KEEP YOUR INFORMATION?</h3>
<p><em>In Short: We keep your information for as long as necessary to fulfill the purposes outlined in this Privacy Notice unless otherwise required by law.</em></p>
<p>We retain your information for as long as your account remains active. If you delete your account (using the /borrar_cuenta or /deleteaccount command in the bot), all your personal data is permanently and immediately deleted from our systems.</p>
<p>When we have no ongoing legitimate business need to process your personal information, we will either delete or anonymize such information, or, if this is not possible (for example, because your personal information has been stored in backup archives), then we will securely store your personal information and isolate it from any further processing until deletion is possible.</p>

<h3>7. HOW DO WE KEEP YOUR INFORMATION SAFE?</h3>
<p><em>In Short: We aim to protect your personal information through a system of organizational and technical security measures.</em></p>
<p>We have implemented appropriate and reasonable technical and organizational security measures designed to protect the security of any personal information we process. However, despite our safeguards and efforts to secure your information, no electronic transmission over the Internet or information storage technology can be guaranteed to be 100% secure, so we cannot promise or guarantee that hackers, cybercriminals, or other unauthorized third parties will not be able to defeat our security and improperly collect, access, steal, or modify your information. You should only access the Services within a secure environment.</p>

<h3>8. DO WE COLLECT INFORMATION FROM MINORS?</h3>
<p><em>In Short: We do not knowingly collect data from or market to children under 18 years of age or the equivalent age as specified by law in your jurisdiction.</em></p>
<p>By using the Services, you represent that you are at least 18 or the equivalent age as specified by law in your jurisdiction, or that you are the parent or guardian of such a minor and consent to such minor dependent's use of the Services. If we learn that personal information from users less than 18 years of age has been collected, we will deactivate the account and take reasonable measures to promptly delete such data from our records. If you become aware of any data we may have collected from children under age 18, please contact us at <a href="mailto:marcoscas1508@gmail.com">marcoscas1508@gmail.com</a>.</p>

<h3>9. WHAT ARE YOUR PRIVACY RIGHTS?</h3>
<p><em>In Short: Depending on your state of residence in the US or in some regions, such as the European Economic Area (EEA), United Kingdom (UK), Switzerland, and Canada, you have rights that allow you greater access to and control over your personal information. You may review, change, or terminate your account at any time.</em></p>
<p>In some regions (like the EEA, UK, Switzerland, and Canada), you have certain rights under applicable data protection laws. These may include the right to request access and obtain a copy of your personal information, to request rectification or erasure, to restrict the processing of your personal information, to data portability, and not to be subject to automated decision-making. You can make such a request by contacting us using the details in "HOW CAN YOU CONTACT US ABOUT THIS NOTICE?" below.</p>
<p>If you are located in the UK and are unhappy with how we have handled your personal information, you can make a complaint directly to us, or refer your complaint to the Information Commissioner's Office (ICO): website ico.org.uk/make-a-complaint, helpline 0303 123 1113, or by post to Information Commissioner's Office, Wycliffe House, Water Lane, Wilmslow, Cheshire, SK9 5AF.</p>
<p>If you are located in the EEA or UK and you believe we are unlawfully processing your personal information, you also have the right to complain to your Member State data protection authority or UK data protection authority. If you are located in Switzerland, you may contact the Federal Data Protection and Information Commissioner.</p>
<p><strong>Withdrawing your consent:</strong> If we are relying on your consent to process your personal information, you have the right to withdraw your consent at any time by contacting us using the details in "HOW CAN YOU CONTACT US ABOUT THIS NOTICE?" below. This will not affect the lawfulness of the processing before its withdrawal.</p>

<h3>10. CONTROLS FOR DO-NOT-TRACK FEATURES</h3>
<p>Most web browsers and some mobile operating systems include a Do-Not-Track ("DNT") feature or setting. At this stage, no uniform technology standard for recognizing and implementing DNT signals has been finalized, so we do not currently respond to DNT browser signals. If a standard for online tracking is adopted that we must follow in the future, we will inform you in a revised version of this Privacy Notice.</p>

<h3>11. DO UNITED STATES RESIDENTS HAVE SPECIFIC PRIVACY RIGHTS?</h3>
<p><em>In Short: If you are a resident of California, Colorado, Connecticut, Delaware, Florida, Indiana, Iowa, Kentucky, Maryland, Minnesota, Montana, Nebraska, New Hampshire, New Jersey, Oregon, Rhode Island, Tennessee, Texas, Utah, or Virginia, you may have the right to request access to and receive details about the personal information we maintain about you, correct inaccuracies, get a copy of, or delete your personal information.</em></p>

<p><strong>Categories of Personal Information We Collect (past 12 months):</strong></p>
<ul>
<li>A. Identifiers (e.g., online identifier, account name) — <strong>Collected</strong></li>
<li>B. Personal information under the California Customer Records statute — Not collected</li>
<li>C. Protected classification characteristics — Not collected</li>
<li>D. Commercial information (e.g., subscription/purchase history) — <strong>Collected</strong></li>
<li>E. Biometric information — Not collected</li>
<li>F. Internet or other similar network activity — Not collected</li>
<li>G. Geolocation data — Not collected</li>
<li>H. Audio, electronic, sensory, or similar information — Not collected</li>
<li>I. Professional or employment-related information — Not collected</li>
<li>J. Education information — Not collected</li>
<li>K. Inferences drawn from collected personal information — Not collected</li>
<li>L. Sensitive personal information — Not collected</li>
</ul>
<p>We retain Category A and Category D information for as long as the user has an account with us.</p>

<p><strong>Will your information be shared with anyone else?</strong> We may disclose your personal information with our service providers pursuant to a written contract between us and each service provider. We have not disclosed, sold, or shared any personal information to third parties for a business or commercial purpose in the preceding twelve (12) months, and we will not sell or share personal information belonging to our users in the future.</p>

<p><strong>Your Rights.</strong> You have rights under certain US state data protection laws, including the right to know whether we are processing your personal data, to access it, to correct inaccuracies, to request deletion, to obtain a copy of it, to non-discrimination for exercising your rights, and to opt out of the sale or sharing of your personal data (which we do not do).</p>

<p><strong>How to Exercise Your Rights.</strong> To exercise these rights, you can contact us by visiting <a href="https://t.me/TrackerHabitFutureBot">https://t.me/TrackerHabitFutureBot</a>, by emailing us at <a href="mailto:marcoscas1508@gmail.com">marcoscas1508@gmail.com</a>, or by referring to the contact details at the bottom of this document. Under certain US state data protection laws, you can designate an authorized agent to make a request on your behalf.</p>

<p><strong>Request Verification.</strong> Upon receiving your request, we will need to verify your identity to determine you are the same person about whom we have the information in our system.</p>

<p><strong>Appeals.</strong> Under certain US state data protection laws, if we decline to take action regarding your request, you may appeal our decision by emailing us at <a href="mailto:marcoscas1508@gmail.com">marcoscas1508@gmail.com</a>. If your appeal is denied, you may submit a complaint to your state attorney general.</p>

<p><strong>California "Shine The Light" Law.</strong> California Civil Code Section 1798.83 permits California residents to request and obtain from us, once a year and free of charge, information about categories of personal information (if any) we disclosed to third parties for direct marketing purposes. If you are a California resident and would like to make such a request, please submit your request in writing using the contact details in "HOW CAN YOU CONTACT US ABOUT THIS NOTICE?" below.</p>

<h3>12. DO WE MAKE UPDATES TO THIS NOTICE?</h3>
<p><em>In Short: Yes, we will update this notice as necessary to stay compliant with relevant laws.</em></p>
<p>We may update this Privacy Notice from time to time. The updated version will be indicated by an updated "Last updated" date at the top of this Privacy Notice. If we make material changes to this Privacy Notice, we may notify you either by prominently posting a notice of such changes or by directly sending you a notification. We encourage you to review this Privacy Notice frequently to be informed of how we are protecting your information.</p>

<h3>13. HOW CAN YOU CONTACT US ABOUT THIS NOTICE?</h3>
<p>If you have questions or comments about this notice, you may email us at <a href="mailto:marcoscas1508@gmail.com">marcoscas1508@gmail.com</a>.</p>

<h3>14. HOW CAN YOU REVIEW, UPDATE, OR DELETE THE DATA WE COLLECT FROM YOU?</h3>
<p>Based on the applicable laws of your country or state of residence, you may have the right to request access to the personal information we collect from you, details about how we have processed it, correct inaccuracies, or delete your personal information. You may also have the right to withdraw your consent to our processing of your personal information. These rights may be limited in some circumstances by applicable law. To request to review, update, or delete your personal information, please visit: <a href="https://t.me/TrackerHabitFutureBot">https://t.me/TrackerHabitFutureBot</a>.</p>

<p><em>This Privacy Policy was created using Termly's Privacy Policy Generator.</em></p>
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
    .legal-box h1, .legal-box h2, .legal-box h3 {
        background: linear-gradient(135deg, #a78bfa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .legal-box a { color: #34d399; }

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
st.markdown(f'<div class="legal-box">{TEXTO_POLITICA}</div>', unsafe_allow_html=True)
