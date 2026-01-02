import React, { useState } from 'react';
import styles from './styles.module.css';

export default function UrduTranslateButton() {
  const [isUrdu, setIsUrdu] = useState(false);
  const [originalContent, setOriginalContent] = useState('');

  const handleTranslation = () => {
    // Get the current page content
    const mainContent = document.querySelector('main .container');
    if (mainContent) {
      if (!isUrdu) {
        // Store original content before translation
        setOriginalContent(mainContent.innerHTML);

        // In a real implementation, this would call an API to translate the content
        // For this demo, we'll just indicate that translation would happen
        alert('In a real implementation, this would translate the content to Urdu using an AI translation service while preserving formatting.');
      } else {
        // Restore original content
        if (originalContent) {
          mainContent.innerHTML = originalContent;
        }
      }
    }

    setIsUrdu(!isUrdu);
  };

  return (
    <button
      className={`${styles.translateButton} ${isUrdu ? styles.translated : ''}`}
      onClick={handleTranslation}
      title="Translate content to Urdu"
    >
      {isUrdu ? ' Urdu:ON' : ' Urdu:OFF'}
    </button>
  );
}