import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import { FaCamera, FaPlay } from "react-icons/fa";

export default function AnalysisPage() {
  const { isAuthenticated, token } = useContext(AuthContext);
  const navigate = useNavigate();
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [showSaveForm, setShowSaveForm] = useState(false);
  const [childData, setChildData] = useState({ childId: "", name: "" });
  const [children, setChildren] = useState([]);
  const [dragActive, setDragActive] = useState(false);

  // Fetch children when user wants to save
  const fetchChildren = async () => {
    if (!token) return;
    try {
      const response = await fetch("http://localhost:5000/api/children", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (response.ok) {
        setChildren(data.children);
      }
    } catch (err) {
      console.error("Failed to fetch children:", err);
    }
  };

  const toggleSaveForm = () => {
    if (!showSaveForm) {
      fetchChildren();
    }
    setShowSaveForm(!showSaveForm);
  };

  const processImage = (file) => {
    if (file && file.type.startsWith("image/")) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(file);
      setError("");
      setResult(null);
    } else {
      setError("Please select a valid image file");
    }
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      processImage(file);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      processImage(files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError("Please select an image first");
      return;
    }

    setAnalyzing(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("image", selectedImage);

      const response = await fetch("http://localhost:5000/api/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || "Analysis failed");
      }
    } catch (err) {
      setError("Error during analysis: " + err.message);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleSaveAssessment = async () => {
    if (!childData.childId && !childData.name) {
      setError("Please select or enter a child name");
      return;
    }

    if (!isAuthenticated) {
      navigate("/login");
      return;
    }

    try {
      const assessmentData = {
        child_id: childData.childId,
        autism_score: result.autism_score,
        status: result.status,
        facial_features: result.facial_features,
        recommendations: result.recommendations,
      };

      const response = await fetch(
        "http://localhost:5000/api/assessment/save",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(assessmentData),
        }
      );

      if (response.ok) {
        setError("");
        setShowSaveForm(false);
        alert("Assessment saved successfully!");
      } else {
        const data = await response.json();
        setError(data.error || "Failed to save assessment");
      }
    } catch (err) {
      setError("Error saving assessment: " + err.message);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "positive":
        return "#e74c3c";
      case "negative":
        return "#27ae60";
      case "inconclusive":
        return "#f39c12";
      default:
        return "#95a5a6";
    }
  };

  return (
    <div style={styles.container}>
      <div className="container">
        <h1 style={styles.title}>Autism Detection Analysis</h1>
        <p style={styles.subtitle}>
          Upload a photo for facial expression analysis
        </p>

        {error && <div style={styles.alert}>{error}</div>}

        <div style={styles.contentGrid}>
          {/* Upload Section */}
          <div style={styles.uploadSection}>
            <div
              style={{
                ...styles.uploadBox,
                backgroundColor: dragActive ? "#e3e8ff" : "white",
                borderColor: dragActive ? "#667eea" : "#667eea",
              }}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                style={styles.fileInput}
                id="imageInput"
              />
              <label htmlFor="imageInput" style={styles.uploadLabel}>
                <FaCamera style={{ fontSize: "2rem", marginBottom: "10px" }} />
                <p>Click to upload or drag and drop</p>
                <small>PNG, JPG, GIF up to 50MB</small>
              </label>
            </div>

            {preview && (
              <div style={styles.previewSection}>
                <h3>Preview</h3>
                <img src={preview} alt="Preview" style={styles.previewImage} />
                <button
                  onClick={handleAnalyze}
                  disabled={analyzing}
                  style={styles.analyzeButton}
                >
                  <FaPlay /> {analyzing ? "Analyzing..." : "Analyze Image"}
                </button>
              </div>
            )}
          </div>

          {/* Results Section */}
          {result && (
            <div style={styles.resultsSection}>
              <h2>Analysis Results</h2>

              <div style={styles.resultCard}>
                <div style={styles.scoreDisplay}>
                  <div
                    style={{
                      ...styles.scoreCircle,
                      borderColor: getStatusColor(result.status),
                    }}
                  >
                    <span style={{ fontSize: "2rem", fontWeight: "bold" }}>
                      {(result.autism_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div>
                    <h3 style={{ margin: "10px 0" }}>
                      Autism Probability Score
                    </h3>
                    <p style={{ color: "#7f8c8d" }}>
                      Confidence: {(result.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              </div>

              <div
                style={{
                  ...styles.statusBox,
                  backgroundColor: getStatusColor(result.status) + "20",
                  borderLeftColor: getStatusColor(result.status),
                }}
              >
                <h3
                  style={{
                    color: getStatusColor(result.status),
                    margin: "0 0 10px 0",
                  }}
                >
                  Status: {result.status.toUpperCase()}
                </h3>
                <p>{getStatusMessage(result.status)}</p>
              </div>

              <div style={styles.featuresBox}>
                <h3>Facial Features Analysis</h3>
                <div style={styles.featureGrid}>
                  <div style={styles.featureItem}>
                    <span>Eye Contact</span>
                    <div style={styles.progressBar}>
                      <div
                        style={{
                          ...styles.progressFill,
                          width: result.facial_features.eye_contact * 100 + "%",
                        }}
                      ></div>
                    </div>
                    <span style={styles.featureValue}>
                      {(result.facial_features.eye_contact * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div style={styles.featureItem}>
                    <span>Face Symmetry</span>
                    <div style={styles.progressBar}>
                      <div
                        style={{
                          ...styles.progressFill,
                          width:
                            result.facial_features.face_symmetry * 100 + "%",
                        }}
                      ></div>
                    </div>
                    <span style={styles.featureValue}>
                      {(result.facial_features.face_symmetry * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div style={styles.featureItem}>
                    <span>Expression Intensity</span>
                    <div style={styles.progressBar}>
                      <div
                        style={{
                          ...styles.progressFill,
                          width:
                            result.facial_features.expression_intensity * 100 +
                            "%",
                        }}
                      ></div>
                    </div>
                    <span style={styles.featureValue}>
                      {(
                        result.facial_features.expression_intensity * 100
                      ).toFixed(1)}
                      %
                    </span>
                  </div>
                </div>
              </div>

              <div style={styles.recommendationsBox}>
                <h3>Recommendations</h3>
                <ul style={styles.recommendationsList}>
                  {result.recommendations.map((rec, idx) => (
                    <li key={idx}>{rec}</li>
                  ))}
                </ul>
              </div>

              {isAuthenticated && (
                <button
                  onClick={toggleSaveForm}
                  style={styles.saveButton}
                >
                  {showSaveForm ? "Cancel" : "Save Assessment"}
                </button>
              )}

              {showSaveForm && (
                <div style={styles.saveForm}>
                  <h3>Save Assessment</h3>
                  {children.length === 0 ? (
                    <div style={{ textAlign: "center", padding: "20px" }}>
                      <p>You need to add a child profile first.</p>
                      <button
                        onClick={() => navigate("/dashboard")}
                        style={styles.saveButton}
                      >
                        Go to Dashboard
                      </button>
                    </div>
                  ) : (
                    <>
                      <div style={styles.formGroup}>
                        <label>Select Child</label>
                        <select
                          value={childData.childId}
                          onChange={(e) => {
                            const selectedChild = children.find(
                              (c) => c.id === parseInt(e.target.value)
                            );
                            setChildData({
                              childId: e.target.value,
                              name: selectedChild ? selectedChild.name : "",
                            });
                          }}
                          style={styles.input}
                        >
                          <option value="">-- Select a child --</option>
                          {children.map((child) => (
                            <option key={child.id} value={child.id}>
                              {child.name}
                            </option>
                          ))}
                        </select>
                      </div>
                      <button
                        onClick={handleSaveAssessment}
                        style={styles.confirmButton}
                        disabled={!childData.childId}
                      >
                        Save to Profile
                      </button>
                    </>
                  )}
                </div>
              )}
            </div>
          )}

          {!result && !preview && (
            <div style={styles.infoSection}>
              <h2>How It Works</h2>
              <div style={styles.infoSteps}>
                <div style={styles.infoStep}>
                  <div style={styles.stepNum}>1</div>
                  <h4>Upload Image</h4>
                  <p>Select a clear photo of the child's face</p>
                </div>
                <div style={styles.infoStep}>
                  <div style={styles.stepNum}>2</div>
                  <h4>AI Analysis</h4>
                  <p>Our model analyzes facial expressions and patterns</p>
                </div>
                <div style={styles.infoStep}>
                  <div style={styles.stepNum}>3</div>
                  <h4>Get Results</h4>
                  <p>Receive detailed analysis with recommendations</p>
                </div>
                <div style={styles.infoStep}>
                  <div style={styles.stepNum}>4</div>
                  <h4>Save & Track</h4>
                  <p>Save results and monitor progress over time</p>
                </div>
              </div>

              <div style={styles.disclaimerBox}>
                <h4>⚠️ Important Disclaimer</h4>
                <p>
                  This tool is for screening purposes only and is NOT a
                  diagnostic tool. The results should not be used as a
                  substitute for professional medical advice. Always consult
                  with a qualified healthcare professional for proper diagnosis
                  and treatment.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function getStatusMessage(status) {
  switch (status) {
    case "positive":
      return "Facial expression patterns suggest potential autism spectrum characteristics. Professional evaluation is recommended.";
    case "negative":
      return "No significant autism indicators detected in the facial expression analysis at this time.";
    case "inconclusive":
      return "The analysis shows mixed results. Retesting with multiple photos is recommended for better accuracy.";
    default:
      return "Analysis complete.";
  }
}

const styles = {
  container: {
    padding: "40px 20px",
    backgroundColor: "#f8f9fa",
    minHeight: "80vh",
  },
  title: {
    fontSize: "2.5rem",
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: "10px",
    color: "#2c3e50",
  },
  subtitle: {
    textAlign: "center",
    color: "#7f8c8d",
    marginBottom: "40px",
    fontSize: "1.1rem",
  },
  alert: {
    backgroundColor: "#f8d7da",
    color: "#721c24",
    padding: "15px",
    borderRadius: "4px",
    marginBottom: "20px",
    border: "1px solid #f5c6cb",
  },
  contentGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "30px",
    "@media (max-width: 1024px)": {
      gridTemplateColumns: "1fr",
    },
  },
  uploadSection: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
  },
  uploadBox: {
    backgroundColor: "white",
    border: "2px dashed #667eea",
    borderRadius: "8px",
    padding: "40px",
    textAlign: "center",
    cursor: "pointer",
    transition: "all 0.3s",
  },
  fileInput: {
    display: "none",
  },
  uploadLabel: {
    cursor: "pointer",
    display: "block",
    color: "#667eea",
  },
  previewSection: {
    backgroundColor: "white",
    borderRadius: "8px",
    padding: "20px",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  },
  previewImage: {
    width: "100%",
    maxHeight: "400px",
    objectFit: "cover",
    borderRadius: "4px",
    marginBottom: "15px",
  },
  analyzeButton: {
    width: "100%",
    padding: "12px",
    backgroundColor: "#667eea",
    color: "white",
    border: "none",
    borderRadius: "4px",
    fontSize: "16px",
    fontWeight: "bold",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "10px",
  },
  resultsSection: {
    backgroundColor: "white",
    borderRadius: "8px",
    padding: "25px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
  },
  resultCard: {
    marginBottom: "20px",
    padding: "20px",
    backgroundColor: "#f8f9fa",
    borderRadius: "8px",
  },
  scoreDisplay: {
    display: "flex",
    alignItems: "center",
    gap: "30px",
  },
  scoreCircle: {
    width: "120px",
    height: "120px",
    borderRadius: "50%",
    border: "4px solid",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    flexShrink: 0,
  },
  statusBox: {
    borderLeft: "4px solid",
    padding: "15px",
    borderRadius: "4px",
    marginBottom: "20px",
  },
  featuresBox: {
    marginBottom: "20px",
  },
  featureGrid: {
    display: "grid",
    gap: "15px",
    marginTop: "15px",
  },
  featureItem: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },
  progressBar: {
    flex: 1,
    height: "8px",
    backgroundColor: "#ecf0f1",
    borderRadius: "4px",
    overflow: "hidden",
  },
  progressFill: {
    height: "100%",
    backgroundColor: "#667eea",
    transition: "width 0.3s",
  },
  featureValue: {
    minWidth: "60px",
    textAlign: "right",
    fontWeight: "bold",
  },
  recommendationsBox: {
    marginBottom: "20px",
  },
  recommendationsList: {
    listStyle: "none",
    padding: 0,
    marginTop: "10px",
  },
  saveButton: {
    width: "100%",
    padding: "12px",
    backgroundColor: "#27ae60",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  saveForm: {
    marginTop: "20px",
    padding: "20px",
    backgroundColor: "#f8f9fa",
    borderRadius: "4px",
  },
  formGroup: {
    marginBottom: "15px",
  },
  input: {
    width: "100%",
    padding: "10px",
    border: "1px solid #ddd",
    borderRadius: "4px",
    marginTop: "5px",
  },
  confirmButton: {
    width: "100%",
    padding: "10px",
    backgroundColor: "#27ae60",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  infoSection: {
    backgroundColor: "white",
    borderRadius: "8px",
    padding: "25px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
  },
  infoSteps: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
    gap: "20px",
    marginBottom: "30px",
  },
  infoStep: {
    textAlign: "center",
  },
  stepNum: {
    width: "40px",
    height: "40px",
    borderRadius: "50%",
    backgroundColor: "#667eea",
    color: "white",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    margin: "0 auto 10px",
    fontWeight: "bold",
  },
  disclaimerBox: {
    backgroundColor: "#fff3cd",
    border: "1px solid #ffeeba",
    borderRadius: "4px",
    padding: "15px",
    color: "#856404",
  },
};
