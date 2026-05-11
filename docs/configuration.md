# Secure Server Configuration (HTTPS + 2FA)

Quick guide to securing a web server and protecting administrative access.

## 1. HTTPS Implementation with SSL/TLS
To encrypt communications, we use **Certbot** and free certificates from **Let's Encrypt**.

### Steps:
1. **Install Certbot:**
   ```bash
   sudo apt update
   sudo apt install certbot python3-certbot-nginx  # For Nginx
   ```
2. **Obtain the certificate automatically:**
   Replace `yourdomain.com` with your actual registered domain name.
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```
3. **Verify auto-renewal:**
   ```bash
   sudo certbot renew --dry-run
   ```

---

## 2. Two-Factor Authentication (2FA) for SSH
Protect remote access to the server by requiring a Time-based One-Time Password (TOTP) generated on your mobile device.

### Steps:
1. **Install the Google Authenticator module:**
   ```bash
   sudo apt install libpam-google-authenticator
   ```
2. **Configure the second factor:**
   Run the command and scan the QR code that appears using a mobile app like [Google Authenticator](https://google.com) or [Authy](https://authy.com).
   ```bash
   google-authenticator
   ```
3. **Enable in the system (PAM):**
   Open the file with `sudo nano /etc/pam.d/sshd` and add the following line at the end:
   ```text
   auth required pam_google_authenticator.so
   ```
4. **Configure the SSH service:**
   Open `sudo nano /etc/ssh/sshd_config` and ensure the following option is set to `yes`:
   ```text
   KbdInteractiveAuthentication yes
   ```
5. **Restart SSH:**
   ```bash
   sudo systemctl restart ssh
   ```

---
*Note: Make sure to save the recovery codes generated during the 2FA setup to avoid losing access to your server.*
