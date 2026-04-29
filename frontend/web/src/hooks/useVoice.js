import { useState, useRef, useEffect, useCallback } from "react";
import axios from "axios";

export default function useVoice() {
  const [isSupported, setIsSupported] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [interimTranscript, setInterimTranscript] = useState("");
  const [error, setError] = useState(null);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [language, setLanguage] = useState("bn-BD"); // Default to Bengali for Liao

  const recognitionRef = useRef(null);
  const audioRef = useRef(new Audio());

  /* =========================================
      INIT SPEECH RECOGNITION (STT)
  ========================================= */
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setIsSupported(false);
      return;
    }

    setIsSupported(true);
    const recognition = new SpeechRecognition();
    recognition.continuous = false; // Set to false for better command control
    recognition.interimResults = true;
    recognition.lang = language;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = (event) => {
      setError(event?.error || "Voice error");
      setIsListening(false);
    };

    recognition.onresult = (event) => {
      let finalText = "";
      let interim = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const text = event.results[i][0].transcript;
        if (event.results[i].isFinal) finalText += text;
        else interim += text;
      }
      setTranscript(finalText);
      setInterimTranscript(interim);
    };

    recognitionRef.current = recognition;
  }, [language]);

  /* =========================================
      BACKEND SPEAK (TTS) - The Jarvis Voice
  ========================================= */
  const speak = useCallback(async (text) => {
    if (!voiceEnabled || !text?.trim()) return;

    try {
      // 1. Backend API Call (TTS)
      const response = await axios.post("http://127.0.0.1:8000/voice/tts", {
        text: text,
      });

      if (response.data.success) {
        // 2. Get Audio URL (Assuming you serve static files or have a full path)
        // Note: Backend output_path logic should be accessible via browser
        const audioUrl = `http://127.0.0.1:8000/static/${response.data.audio_path.split('\\').pop()}`;
        
        audioRef.current.src = audioUrl;
        audioRef.current.play();
      }
    } catch (err) {
      console.error("TTS Error:", err);
      // Fallback to Browser Speech if Backend fails
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = language;
      window.speechSynthesis.speak(utterance);
    }
  }, [voiceEnabled, language]);

  const stopSpeaking = useCallback(() => {
    audioRef.current.pause();
    window.speechSynthesis?.cancel();
  }, []);

  /* =========================================
      CONTROLS
  ========================================= */
  const startListening = useCallback(() => {
    if (!isSupported) return;
    setTranscript("");
    setError(null);
    try { recognitionRef.current.start(); } catch {}
  }, [isSupported]);

  const stopListening = useCallback(() => recognitionRef.current?.stop(), []);

  const toggleListening = useCallback(() => {
    isListening ? stopListening() : startListening();
  }, [isListening, startListening, stopListening]);

  return {
    isSupported,
    isListening,
    transcript,
    interimTranscript,
    error,
    voiceEnabled,
    startListening,
    stopListening,
    toggleListening,
    speak,
    stopSpeaking,
    setLanguage,
  };
}