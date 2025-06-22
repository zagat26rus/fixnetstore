import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import ChatBot from "./components/ChatBot";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";
import Home from "./pages/Home";
import HowItWorks from "./pages/HowItWorks";
import WhyFixNet from "./pages/WhyFixNet";
import SubmitRequest from "./pages/SubmitRequest";
import FAQ from "./pages/FAQ";
import Contact from "./pages/Contact";
import AdminLogin from "./pages/AdminLogin";
import AdminDashboard from "./pages/AdminDashboard";
import { Toaster } from "./components/ui/toaster";

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public Routes with Navigation */}
            <Route path="/" element={
              <>
                <Navigation />
                <Home />
                <ChatBot />
              </>
            } />
            <Route path="/how-it-works" element={
              <>
                <Navigation />
                <HowItWorks />
                <ChatBot />
              </>
            } />
            <Route path="/why-fixnet" element={
              <>
                <Navigation />
                <WhyFixNet />
                <ChatBot />
              </>
            } />
            <Route path="/submit-request" element={
              <>
                <Navigation />
                <SubmitRequest />
                <ChatBot />
              </>
            } />
            <Route path="/faq" element={
              <>
                <Navigation />
                <FAQ />
                <ChatBot />
              </>
            } />
            <Route path="/contact" element={
              <>
                <Navigation />
                <Contact />
                <ChatBot />
              </>
            } />
            
            {/* Admin Routes - Standalone */}
            <Route path="/admin/login" element={<AdminLogin />} />
            <Route 
              path="/admin" 
              element={
                <ProtectedRoute>
                  <AdminDashboard />
                </ProtectedRoute>
              } 
            />
          </Routes>
          <Toaster />
        </BrowserRouter>
      </AuthProvider>
    </div>
  );
}

export default App;