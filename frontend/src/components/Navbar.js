import React, { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import {
  FaBars,
  FaTimes,
  FaHome,
  FaUpload,
  FaChartLine,
  FaComments,
  FaSignOutAlt,
  FaSignInAlt,
  FaUserPlus,
} from "react-icons/fa";

export default function Navbar() {
  const { isAuthenticated, user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav style={styles.navbar}>
      <div style={styles.container}>
        <Link to="/" style={styles.logo}>
          <span style={styles.logoText}>🧠 Autism Detection</span>
        </Link>

        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          style={styles.mobileMenuButton}
        >
          {mobileMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
        </button>

        <div
          style={{
            ...styles.navLinks,
            display:
              window.innerWidth <= 768 && !mobileMenuOpen ? "none" : "flex",
          }}
        >
          <Link to="/" style={styles.navLink}>
            <FaHome /> Home
          </Link>

          {!isAuthenticated ? (
            <>
              <Link to="/login" style={styles.navLink}>
                <FaSignInAlt /> Login
              </Link>
              <Link to="/register" style={styles.navLink}>
                <FaUserPlus /> Register
              </Link>
            </>
          ) : (
            <>
              <Link to="/analyze" style={styles.navLink}>
                <FaUpload /> Analyze
              </Link>
              <Link to="/dashboard" style={styles.navLink}>
                <FaChartLine /> Dashboard
              </Link>
              <Link to="/chat" style={styles.navLink}>
                <FaComments /> Chat
              </Link>
              <div style={styles.userSection}>
                <span style={styles.userName}>{user?.full_name}</span>
                <button onClick={handleLogout} style={styles.logoutBtn}>
                  <FaSignOutAlt /> Logout
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

const styles = {
  navbar: {
    backgroundColor: "#2c3e50",
    color: "white",
    padding: "1rem 0",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
    position: "sticky",
    top: 0,
    zIndex: 100,
  },
  container: {
    maxWidth: "1200px",
    margin: "0 auto",
    padding: "0 20px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  logo: {
    textDecoration: "none",
    color: "white",
    fontSize: "1.5rem",
    fontWeight: "bold",
  },
  logoText: {
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
  },
  navLinks: {
    display: "flex",
    gap: "1.5rem",
    alignItems: "center",
    flexDirection: window.innerWidth <= 768 ? "column" : "row",
    position: window.innerWidth <= 768 ? "absolute" : "relative",
    top: window.innerWidth <= 768 ? "60px" : "auto",
    left: window.innerWidth <= 768 ? 0 : "auto",
    right: window.innerWidth <= 768 ? 0 : "auto",
    backgroundColor: window.innerWidth <= 768 ? "#2c3e50" : "transparent",
    padding: window.innerWidth <= 768 ? "1rem" : "0",
  },
  navLink: {
    color: "white",
    textDecoration: "none",
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
    padding: "0.5rem 1rem",
    borderRadius: "4px",
    transition: "background-color 0.3s",
    cursor: "pointer",
    fontSize: "1rem",
  },
  userSection: {
    display: "flex",
    alignItems: "center",
    gap: "1rem",
    flexDirection: window.innerWidth <= 768 ? "column" : "row",
  },
  userName: {
    fontWeight: "500",
    whiteSpace: "nowrap",
  },
  logoutBtn: {
    backgroundColor: "#e74c3c",
    color: "white",
    border: "none",
    padding: "0.5rem 1rem",
    borderRadius: "4px",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
    transition: "background-color 0.3s",
    fontSize: "0.95rem",
  },
  mobileMenuButton: {
    display: window.innerWidth <= 768 ? "block" : "none",
    backgroundColor: "transparent",
    border: "none",
    color: "white",
    cursor: "pointer",
    fontSize: "1.5rem",
  },
};
