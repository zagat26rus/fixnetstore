import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import ChatBot from "./components/ChatBot";
import Home from "./pages/Home";
import HowItWorks from "./pages/HowItWorks";
import WhyFixNet from "./pages/WhyFixNet";
import SubmitRequest from "./pages/SubmitRequest";
import FAQ from "./pages/FAQ";
import Contact from "./pages/Contact";
import AdminDashboard from "./pages/AdminDashboard";
import { Toaster } from "./components/ui/toaster";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          <Route path="/why-fixnet" element={<WhyFixNet />} />
          <Route path="/submit-request" element={<SubmitRequest />} />
          <Route path="/faq" element={<FAQ />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/admin" element={<AdminDashboard />} />
        </Routes>
        <ChatBot />
        <Toaster />
      </BrowserRouter>
    </div>
  );
}