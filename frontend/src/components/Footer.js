import React from "react";
import { FaFacebook, FaTwitter, FaLinkedin, FaEnvelope } from "react-icons/fa";

export default function Footer() {
  return (
    <footer style={styles.footer}>
      <div className="container" style={styles.footerContent}>
        <div style={styles.footerSection}>
          <h3>About Us</h3>
          <p>
            We're dedicated to early autism detection using AI-powered facial
            expression analysis to help parents and healthcare professionals
            identify signs early.
          </p>
        </div>

        <div style={styles.footerSection}>
          <h3>Quick Links</h3>
          <ul style={styles.footerLinks}>
            <li>
              <a href="/">Home</a>
            </li>
            <li>
              <a href="/analyze">Analyze</a>
            </li>
            <li>
              <a href="#about">About</a>
            </li>
            <li>
              <a href="#contact">Contact</a>
            </li>
          </ul>
        </div>

        <div style={styles.footerSection}>
          <h3>Contact & Social</h3>
          <div style={styles.socialLinks}>
            <a href="#facebook" title="Facebook">
              <FaFacebook />
            </a>
            <a href="#twitter" title="Twitter">
              <FaTwitter />
            </a>
            <a href="#linkedin" title="LinkedIn">
              <FaLinkedin />
            </a>
            <a href="#email" title="Email">
              <FaEnvelope />
            </a>
          </div>
          <p style={{ marginTop: "1rem" }}>Email: info@autismdetection.com</p>
          <p>Phone: 1-800-AUTISM-1</p>
        </div>

        <div style={styles.footerSection}>
          <h3>Disclaimer</h3>
          <p>
            This tool is for screening purposes only and is not a diagnostic
            tool. Always consult with healthcare professionals for proper
            diagnosis.
          </p>
        </div>
      </div>

      <div style={styles.footerBottom}>
        <p>&copy; 2024 Autism Detection Platform. All rights reserved.</p>
      </div>
    </footer>
  );
}

const styles = {
  footer: {
    backgroundColor: "#2c3e50",
    color: "#ecf0f1",
    padding: "3rem 0 1rem",
    marginTop: "3rem",
    borderTop: "1px solid #34495e",
  },
  footerContent: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
    gap: "2rem",
    marginBottom: "2rem",
  },
  footerSection: {
    padding: "0 1rem",
  },
  footerLinks: {
    listStyle: "none",
    padding: 0,
  },
  socialLinks: {
    display: "flex",
    gap: "1rem",
    fontSize: "1.5rem",
  },
  footerBottom: {
    textAlign: "center",
    paddingTop: "1rem",
    borderTop: "1px solid #34495e",
    color: "#bdc3c7",
  },
};
