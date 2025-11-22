import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import { FaLightbulb, FaHeart, FaUsers, FaArrowRight } from "react-icons/fa";

export default function HomePage() {
  const { isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      {/* Hero Section */}
      <section style={styles.hero}>
        <div style={styles.heroContent}>
          <h1 style={styles.heroTitle}>
            Autism Detection Through Facial Expression Analysis
          </h1>
          <p style={styles.heroSubtitle}>
            Early detection can change lives. Our AI-powered platform helps
            identify potential autism spectrum characteristics in children
            through non-invasive facial expression analysis.
          </p>
          <div style={styles.heroCTA}>
            {isAuthenticated ? (
              <button
                onClick={() => navigate("/analyze")}
                style={styles.ctaPrimary}
              >
                Start Analysis <FaArrowRight style={{ marginLeft: "0.5rem" }} />
              </button>
            ) : (
              <>
                <Link to="/register" style={styles.ctaPrimary}>
                  Get Started <FaArrowRight style={{ marginLeft: "0.5rem" }} />
                </Link>
                <Link to="/analyze" style={styles.ctaSecondary}>
                  Quick Analysis
                </Link>
              </>
            )}
          </div>
        </div>
        <div style={styles.heroImage}>
          <div style={styles.heroIcon}>🧠</div>
        </div>
      </section>

      {/* About Section */}
      <section style={styles.section}>
        <div className="container">
          <h2 style={styles.sectionTitle}>What is Autism Spectrum Disorder?</h2>
          <div style={styles.aboutGrid}>
            <div style={styles.aboutCard}>
              <FaUsers style={styles.aboutIcon} />
              <h3>Social Communication</h3>
              <p>
                Autism affects how children communicate and interact with
                others. Early intervention can help develop these skills
                significantly.
              </p>
            </div>
            <div style={styles.aboutCard}>
              <FaHeart style={styles.aboutIcon} />
              <h3>Behavioral Patterns</h3>
              <p>
                Children with autism may show different behavioral patterns
                including repetitive interests and sensory sensitivities.
              </p>
            </div>
            <div style={styles.aboutCard}>
              <FaLightbulb style={styles.aboutIcon} />
              <h3>Early Support</h3>
              <p>
                Research shows that early diagnosis and intervention lead to
                better outcomes and improved quality of life.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Our Platform Section */}
      <section style={styles.sectionAlt}>
        <div className="container">
          <h2 style={styles.sectionTitle}>How Our Platform Works</h2>
          <div style={styles.stepsGrid}>
            <div style={styles.step}>
              <div style={styles.stepNumber}>1</div>
              <h3>Upload Photo</h3>
              <p>Upload a clear photo of the child's face for analysis</p>
            </div>
            <div style={styles.step}>
              <div style={styles.stepNumber}>2</div>
              <h3>AI Analysis</h3>
              <p>Our model analyzes facial expressions and detects patterns</p>
            </div>
            <div style={styles.step}>
              <div style={styles.stepNumber}>3</div>
              <h3>Get Results</h3>
              <p>Receive detailed analysis with recommendations</p>
            </div>
            <div style={styles.step}>
              <div style={styles.stepNumber}>4</div>
              <h3>Track Progress</h3>
              <p>
                Save results and monitor progress over time with our dashboard
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section style={styles.section}>
        <div className="container">
          <h2 style={styles.sectionTitle}>Key Features</h2>
          <div style={styles.featuresGrid}>
            <div style={styles.featureCard}>
              <h3>🎯 Accurate Analysis</h3>
              <p>
                Using advanced deep learning CNN model trained on diverse
                datasets
              </p>
            </div>
            <div style={styles.featureCard}>
              <h3>👨‍👩‍👧 Parent Dashboard</h3>
              <p>Track your child's assessments and progress over time</p>
            </div>
            <div style={styles.featureCard}>
              <h3>🤖 AI Chatbot</h3>
              <p>Get expert guidance and advice on supporting your child</p>
            </div>
            <div style={styles.featureCard}>
              <h3>📊 Detailed Reports</h3>
              <p>Comprehensive analysis with medical recommendations</p>
            </div>
            <div style={styles.featureCard}>
              <h3>🔒 Secure & Private</h3>
              <p>
                Your data is protected with encryption and strict privacy
                policies
              </p>
            </div>
            <div style={styles.featureCard}>
              <h3>💬 Professional Support</h3>
              <p>Connect with professionals and other parents for guidance</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      {!isAuthenticated && (
        <section style={styles.ctaSection}>
          <div className="container" style={{ textAlign: "center" }}>
            <h2>Ready to Get Started?</h2>
            <p>
              Join thousands of parents who are using our platform for early
              autism detection
            </p>
            <div style={styles.ctaButtons}>
              <Link to="/register" style={styles.ctaPrimary}>
                Create Account
              </Link>
              <Link to="/analyze" style={styles.ctaSecondary}>
                Try Quick Analysis
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* FAQ Section */}
      <section style={styles.sectionAlt}>
        <div className="container">
          <h2 style={styles.sectionTitle}>Frequently Asked Questions</h2>
          <div style={styles.faqGrid}>
            <div style={styles.faqItem}>
              <h4>Is this a diagnostic tool?</h4>
              <p>
                No, this is a screening tool for initial assessment. Always
                consult with healthcare professionals for proper diagnosis.
              </p>
            </div>
            <div style={styles.faqItem}>
              <h4>How accurate is the analysis?</h4>
              <p>
                Our model is trained on thousands of images and achieves high
                accuracy. However, professional evaluation is always
                recommended.
              </p>
            </div>
            <div style={styles.faqItem}>
              <h4>What age group can be analyzed?</h4>
              <p>
                Our model works best for children ages 2-12, though it can be
                used for other ages.
              </p>
            </div>
            <div style={styles.faqItem}>
              <h4>How long does analysis take?</h4>
              <p>
                The analysis typically completes in 1-2 seconds after upload.
              </p>
            </div>
            <div style={styles.faqItem}>
              <h4>Is my data secure?</h4>
              <p>
                Yes, all data is encrypted and stored securely. We comply with
                HIPAA and GDPR regulations.
              </p>
            </div>
            <div style={styles.faqItem}>
              <h4>Do I need to create an account?</h4>
              <p>
                You can do a quick analysis without an account, but need one to
                save results and track progress.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

const styles = {
  container: {
    width: "100%",
  },
  hero: {
    backgroundColor: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    backgroundImage: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    color: "white",
    padding: "60px 20px",
    display: "flex",
    alignItems: "center",
    gap: "40px",
    flexWrap: "wrap",
  },
  heroContent: {
    flex: 1,
    minWidth: "300px",
  },
  heroTitle: {
    fontSize: "2.5rem",
    fontWeight: "bold",
    marginBottom: "20px",
    lineHeight: "1.2",
  },
  heroSubtitle: {
    fontSize: "1.2rem",
    marginBottom: "30px",
    opacity: 0.95,
  },
  heroCTA: {
    display: "flex",
    gap: "15px",
    flexWrap: "wrap",
  },
  heroImage: {
    flex: 1,
    minWidth: "300px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  heroIcon: {
    fontSize: "150px",
    opacity: 0.9,
  },
  section: {
    padding: "60px 20px",
    backgroundColor: "white",
  },
  sectionAlt: {
    padding: "60px 20px",
    backgroundColor: "#f8f9fa",
  },
  sectionTitle: {
    fontSize: "2rem",
    textAlign: "center",
    marginBottom: "40px",
    color: "#2c3e50",
    fontWeight: "bold",
  },
  aboutGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
    gap: "30px",
  },
  aboutCard: {
    backgroundColor: "#f0f4ff",
    padding: "30px",
    borderRadius: "8px",
    textAlign: "center",
    transition: "transform 0.3s",
  },
  aboutIcon: {
    fontSize: "3rem",
    color: "#667eea",
    marginBottom: "15px",
  },
  stepsGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
    gap: "25px",
  },
  step: {
    textAlign: "center",
    padding: "25px",
  },
  stepNumber: {
    backgroundColor: "#667eea",
    color: "white",
    width: "50px",
    height: "50px",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "1.5rem",
    fontWeight: "bold",
    margin: "0 auto 20px",
  },
  featuresGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
    gap: "25px",
  },
  featureCard: {
    backgroundColor: "white",
    padding: "25px",
    borderRadius: "8px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
    transition: "transform 0.3s",
  },
  ctaSection: {
    padding: "60px 20px",
    backgroundColor: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    backgroundImage: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    color: "white",
    textAlign: "center",
  },
  ctaButtons: {
    display: "flex",
    gap: "15px",
    justifyContent: "center",
    flexWrap: "wrap",
    marginTop: "25px",
  },
  ctaPrimary: {
    backgroundColor: "white",
    color: "#667eea",
    padding: "12px 30px",
    borderRadius: "5px",
    textDecoration: "none",
    fontWeight: "bold",
    transition: "transform 0.3s",
    display: "inline-flex",
    alignItems: "center",
    gap: "10px",
    border: "none",
    cursor: "pointer",
    fontSize: "1rem",
  },
  ctaSecondary: {
    backgroundColor: "transparent",
    color: "white",
    padding: "12px 30px",
    borderRadius: "5px",
    textDecoration: "none",
    fontWeight: "bold",
    border: "2px solid white",
    transition: "all 0.3s",
    display: "inline-flex",
    alignItems: "center",
    gap: "10px",
    cursor: "pointer",
    fontSize: "1rem",
  },
  faqGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
    gap: "25px",
  },
  faqItem: {
    backgroundColor: "white",
    padding: "25px",
    borderRadius: "8px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
  },
};
