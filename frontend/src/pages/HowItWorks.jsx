import React, { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';

const HowItWorks = () => {
  const stepsRef = useRef([]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.style.transform = 'translateY(0)';
            entry.target.style.opacity = '1';
          }
        });
      },
      { threshold: 0.2 }
    );

    stepsRef.current.forEach((ref) => {
      if (ref) observer.observe(ref);
    });

    return () => observer.disconnect();
  }, []);

  const steps = [
    {
      number: "01",
      title: "Submit Your Request",
      description: "Tell us about your device and the issue you're experiencing. Our AI assistant will help guide you through the process.",
      icon: (
        <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      )
    },
    {
      number: "02",
      title: "Free Pickup",
      description: "We'll come to you! Our technicians provide free pickup from your location at a time that works for you.",
      icon: (
        <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 17l4 4 4-4m-4-5v9" />
        </svg>
      )
    },
    {
      number: "03",
      title: "AI Diagnosis",
      description: "Our advanced AI system performs comprehensive diagnostics to identify all issues and recommend the best repair approach.",
      icon: (
        <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      )
    },
    {
      number: "04",
      title: "Expert Repair",
      description: "Certified technicians use genuine parts and state-of-the-art tools to restore your device to perfect condition.",
      icon: (
        <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      )
    },
    {
      number: "05",
      title: "Quality Check",
      description: "Every repair undergoes rigorous testing to ensure perfect functionality before we return your device.",
      icon: (
        <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    },
    {
      number: "06",
      title: "Fast Delivery",
      description: "Your repaired device is delivered back to you, typically within 24-48 hours, with a 90-day warranty.",
      icon: (
        <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      )
    }
  ];

  return (
    <div className="min-h-screen pt-20">
      {/* Hero Section */}
      <section className="py-24 bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-8">
            How FixNet
            <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Works
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto mb-12">
            Our streamlined process combines cutting-edge AI technology with expert craftsmanship 
            to deliver the best repair experience.
          </p>
        </div>
      </section>

      {/* Steps Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="space-y-24">
            {steps.map((step, index) => (
              <div
                key={index}
                ref={(el) => (stepsRef.current[index] = el)}
                className={`flex flex-col ${
                  index % 2 === 0 ? 'lg:flex-row' : 'lg:flex-row-reverse'
                } items-center gap-12 lg:gap-20 opacity-0 transform translate-y-8 transition-all duration-700`}
                style={{ transitionDelay: `${index * 100}ms` }}
              >
                {/* Content */}
                <div className="flex-1 text-center lg:text-left">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-600 to-purple-600 text-white rounded-2xl text-2xl font-bold mb-6">
                    {step.number}
                  </div>
                  <h3 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                    {step.title}
                  </h3>
                  <p className="text-xl text-gray-600 leading-relaxed max-w-lg">
                    {step.description}
                  </p>
                </div>

                {/* Icon */}
                <div className="flex-1 flex justify-center">
                  <div className="group">
                    <div className="w-64 h-64 bg-gradient-to-br from-blue-50 to-purple-50 rounded-3xl flex items-center justify-center text-blue-600 group-hover:scale-105 transition-transform duration-300 shadow-xl group-hover:shadow-2xl">
                      {step.icon}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-br from-blue-600 to-purple-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-8">
            Ready to Experience FixNet?
          </h2>
          <p className="text-xl mb-12 opacity-90">
            Start your repair journey today and see why thousands trust FixNet 
            for their device repair needs.
          </p>
          
          <Link to="/submit-request">
            <Button className="bg-white text-blue-600 hover:bg-gray-100 px-10 py-4 text-lg rounded-full font-semibold transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-2xl">
              Submit Your Repair Request
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HowItWorks;