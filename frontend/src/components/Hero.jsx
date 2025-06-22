import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from './ui/button';
import { useLanguage } from '../context/LanguageContext';

const Hero = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const { t } = useLanguage();

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth) * 100,
        y: (e.clientY / window.innerHeight) * 100
      });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden hero-dark">
      {/* Animated Background Elements - Muted Colors */}
      <div className="absolute inset-0">
        <div 
          className="absolute w-96 h-96 floating-element-1 rounded-full blur-3xl"
          style={{
            transform: `translate(${mousePosition.x * 0.1}px, ${mousePosition.y * 0.1}px)`,
            transition: 'transform 0.3s ease-out'
          }}
        />
        <div 
          className="absolute top-1/4 right-1/4 w-64 h-64 floating-element-2 rounded-full blur-2xl"
          style={{
            transform: `translate(${mousePosition.x * -0.05}px, ${mousePosition.y * -0.05}px)`,
            transition: 'transform 0.3s ease-out'
          }}
        />
      </div>

      {/* Floating Elements - Muted Colors */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-3 h-3 bg-gray-500 rounded-full animate-ping opacity-60" />
        <div className="absolute top-3/4 right-1/3 w-2 h-2 bg-gray-400 rounded-full animate-pulse opacity-70" />
        <div className="absolute bottom-1/4 left-1/3 w-4 h-4 bg-gray-600 rounded-full animate-bounce opacity-50" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="animate-fade-in-up">
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-extralight text-white mb-8 leading-tight">
            {t('home.heroTitle')}
            <span className="block font-bold text-gradient">
              {t('home.heroSubtitle')}
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto font-light leading-relaxed">
            {t('home.heroDescription')}
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
            <Link to="/submit-request">
              <Button className="group accent-neutral px-8 py-4 text-lg rounded-full font-medium transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-3xl">
                {t('home.startRepair')}
                <svg className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Button>
            </Link>
            
            <Link to="/how-it-works">
              <Button variant="outline" className="group border-2 border-gray-500 text-gray-300 hover:border-gray-400 hover:text-white px-8 py-4 text-lg rounded-full font-medium transition-all duration-300 transform hover:scale-105 bg-transparent backdrop-blur-sm">
                {t('home.seeHowItWorks')}
                <svg className="ml-2 w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.5a2.5 2.5 0 010 5H9" />
                </svg>
              </Button>
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
            {[
              { number: '50K+', label: t('home.stats.devicesRepaired') },
              { number: '99.2%', label: t('home.stats.successRate') },
              { number: '24hr', label: t('home.stats.averageTurnaround') },
              { number: '90 Day', label: t('home.stats.warranty') }
            ].map((stat, index) => (
              <div key={index} className="group cursor-default">
                <div className="text-3xl md:text-4xl font-bold text-white mb-2 group-hover:scale-110 transition-transform duration-200">
                  {stat.number}
                </div>
                <div className="text-sm text-gray-400 font-medium">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-gray-500 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-gray-500 rounded-full mt-2 animate-pulse" />
        </div>
      </div>
    </section>
  );
};

export default Hero;