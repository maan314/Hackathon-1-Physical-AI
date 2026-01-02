import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

export default function PersonalizeButton() {
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [userBackground, setUserBackground] = useState(null);

  useEffect(() => {
    // Check if user has provided background information
    const storedBackground = localStorage.getItem('userBackground');
    if (storedBackground) {
      setUserBackground(JSON.parse(storedBackground));
    }
  }, []);

  const handlePersonalize = () => {
    if (!userBackground) {
      // Prompt user for background information if not already provided
      const softwareExp = prompt("What is your software experience level? (beginner/intermediate/advanced)");
      const hardwareExp = prompt("What is your hardware/robotics experience level? (none/basic/intermediate/advanced)");

      if (softwareExp && hardwareExp) {
        const background = { software: softwareExp, hardware: hardwareExp };
        setUserBackground(background);
        localStorage.setItem('userBackground', JSON.stringify(background));
      }
    }

    setIsPersonalized(!isPersonalized);

    // Toggle personalization class on the document body
    document.body.classList.toggle('personalized-content', !isPersonalized);
  };

  return (
    <button
      className={`${styles.personalizeButton} ${isPersonalized ? styles.personalized : ''}`}
      onClick={handlePersonalize}
      title="Personalize content based on your background"
    >
      {isPersonalized ? ' personalize:ON' : ' personalize:OFF'}
    </button>
  );
}