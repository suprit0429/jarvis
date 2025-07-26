import React, { useEffect, useState } from 'react';
import "./Welcome.css";

const Welcome = () => {
  const [text, setText] = useState("WELCOME, SIR");
  const [hasInteracted, setHasInteracted] = useState(false);

  const speakText = (textToSpeak) => {
    if ('speechSynthesis' in window) {
      speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      utterance.rate = 0.8;
      utterance.pitch = 1;
      utterance.volume = 1;
      speechSynthesis.speak(utterance);
    }
  };

  useEffect(() => {
    const handleInteraction = () => {
      if (!hasInteracted) {
        setHasInteracted(true);
        speakText("Welcome, Sir");
        setTimeout(() => {
          setText("INITIALIZING...");
          speakText("Initializing");
        }, 3000);
      }
      // Remove listeners after activation
      document.removeEventListener('mousemove', handleInteraction);
      document.removeEventListener('touchstart', handleInteraction);
      document.removeEventListener('keydown', handleInteraction);
    };

    document.addEventListener('mousemove', handleInteraction);
    document.addEventListener('touchstart', handleInteraction);
    document.addEventListener('keydown', handleInteraction);

    return () => {
      document.removeEventListener('mousemove', handleInteraction);
      document.removeEventListener('touchstart', handleInteraction);
      document.removeEventListener('keydown', handleInteraction);
    };
  }, [hasInteracted]);

  return (
    <div className='welcome-screen'>
      <h1 className={`typing-text ${text === "INITIALIZING..." ? 'init' : ''}`}>
        {text}
      </h1>
    </div>
  );
};

export default Welcome;
