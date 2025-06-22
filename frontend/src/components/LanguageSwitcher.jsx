import React from 'react';
import { Button } from './ui/button';
import { useLanguage } from '../context/LanguageContext';

const LanguageSwitcher = ({ className = "" }) => {
  const { currentLanguage, changeLanguage } = useLanguage();

  const languages = [
    { code: 'en', label: 'EN', flag: '🇺🇸' },
    { code: 'ru', label: 'RU', flag: '🇷🇺' }
  ];

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      {languages.map((lang) => (
        <Button
          key={lang.code}
          onClick={() => changeLanguage(lang.code)}
          variant={currentLanguage === lang.code ? "default" : "outline"}
          size="sm"
          className={`min-w-[60px] transition-all duration-200 ${
            currentLanguage === lang.code 
              ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg scale-105' 
              : 'hover:scale-105 hover:shadow-md'
          }`}
        >
          <span className="mr-1">{lang.flag}</span>
          {lang.label}
        </Button>
      ))}
    </div>
  );
};

export default LanguageSwitcher;