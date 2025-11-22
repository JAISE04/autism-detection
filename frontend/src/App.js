import React, { useContext } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import AuthContext, { AuthProvider } from "./context/AuthContext";

// Pages
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AnalysisPage from "./pages/AnalysisPage";
import DashboardPage from "./pages/DashboardPage";
import ChildProfilePage from "./pages/ChildProfilePage";
import ChatPage from "./pages/ChatPage";

// Components
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

function AppContent() {
  const { isAuthenticated } = useContext(AuthContext);

  return (
    <div
      style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}
    >
      <Navbar />
      <main style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route
            path="/login"
            element={
              !isAuthenticated ? <LoginPage /> : <Navigate to="/dashboard" />
            }
          />
          <Route
            path="/register"
            element={
              !isAuthenticated ? <RegisterPage /> : <Navigate to="/dashboard" />
            }
          />
          <Route path="/analyze" element={<AnalysisPage />} />
          <Route
            path="/dashboard"
            element={
              isAuthenticated ? <DashboardPage /> : <Navigate to="/login" />
            }
          />
          <Route
            path="/child/:childId"
            element={
              isAuthenticated ? <ChildProfilePage /> : <Navigate to="/login" />
            }
          />
          <Route
            path="/chat"
            element={isAuthenticated ? <ChatPage /> : <Navigate to="/login" />}
          />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;
