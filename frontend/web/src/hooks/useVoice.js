import { useState, useRef, useEffect, useCallback } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export default function useVoice() {
  /* =========================================
      STATES
  ========================================= */
  const [isSupported, setIsSupported] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isThinking, setIsThinking] = useState(false);

  const [transcript, setTranscript] = useState("");
  const [interimTranscript, setInterimTranscript] = useState("");
  const [reply, setReply] = useState("");

  const [error, setError] = useState(null);

  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [language, setLanguage] = useState("bn-BD");

  /* =========================================
      REFS
  ========================================= */
  const recognitionRef = useRef(null);
  const audioRef = useRef(new Audio());

  /* =========================================
      INIT AUDIO
  ========================================= */
  useEffect(() => {
    const audio = audioRef.current;

    audio.onplay = () => setIsSpeaking(true);
    audio.onended = () => setIsSpeaking(false);
    audio.onpause = () => setIsSpeaking(false);
    audio.onerror = () => setIsSpeaking(false);

    return () => {
      audio.pause();
      audio.src = "";
    };
  }, []);

  /* =========================================
      INIT SPEECH RECOGNITION
  ========================================= */
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setIsSupported(false);
      return;
    }

    setIsSupported(true);

    const recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = language;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
      setError(null);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      setError(event?.error || "Voice recognition failed");
      setIsListening(false);
    };

    recognition.onresult = (event) => {
      let finalText = "";
      let interim = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const text = event.results[i][0].transcript;

        if (event.results[i].isFinal) {
          finalText += text;
        } else {
          interim += text;
        }
      }

      if (finalText) {
        setTranscript(finalText.trim());
      }

      setInterimTranscript(interim.trim());
    };

    recognitionRef.current = recognition;

    return () => {
      recognition.stop();
    };
  }, [language]);

  /* =========================================
      SPEAK (BACKEND TTS)
  ========================================= */
  const speak = useCallback(
    async (text) => {
      if (!voiceEnabled) return;
      if (!text || !text.trim()) return;

      try {
        setError(null);

        const res = await axios.post(`${API_BASE}/voice/tts`, {
          text,
        });

        if (res.data?.success) {
          const fileName = res.data.audio_path;
          const cleanName = fileName.split("\\").pop().split("/").pop();

          const audioUrl = `${API_BASE}/static/${cleanName}?t=${Date.now()}`;

          audioRef.current.src = audioUrl;
          await audioRef.current.play();
          return;
        }

        throw new Error("Backend TTS failed");
      } catch (err) {
        try {
          const utterance = new SpeechSynthesisUtterance(text);
          utterance.lang = language;

          utterance.onstart = () => setIsSpeaking(true);
          utterance.onend = () => setIsSpeaking(false);
          utterance.onerror = () => setIsSpeaking(false);

          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(utterance);
        } catch {
          setError("Speech output failed");
        }
      }
    },
    [voiceEnabled, language]
  );

  /* =========================================
      STOP SPEAKING
  ========================================= */
  const stopSpeaking = useCallback(() => {
    try {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    } catch {}

    try {
      window.speechSynthesis.cancel();
    } catch {}

    setIsSpeaking(false);
  }, []);

  /* =========================================
      CHAT WITH BACKEND AI
  ========================================= */
  const askAI = useCallback(
    async (text) => {
      if (!text || !text.trim()) return;

      try {
        setIsThinking(true);
        setError(null);

        const res = await axios.post(`${API_BASE}/chat`, {
          message: text,
          session_id: "frontend_user",
        });

        const aiReply =
          res.data?.reply || "আমি এখন উত্তর দিতে পারছি না।";

        setReply(aiReply);

        await speak(aiReply);
      } catch (err) {
        setError("AI server connection failed");
      } finally {
        setIsThinking(false);
      }
    },
    [speak]
  );

  /* =========================================
      START LISTENING
  ========================================= */
  const startListening = useCallback(() => {
    if (!isSupported) return;

    setTranscript("");
    setInterimTranscript("");
    setReply("");
    setError(null);

    try {
      recognitionRef.current?.start();
    } catch {}
  }, [isSupported]);

  /* =========================================
      STOP LISTENING
  ========================================= */
  const stopListening = useCallback(() => {
    try {
      recognitionRef.current?.stop();
    } catch {}
  }, []);

  /* =========================================
      TOGGLE LISTENING
  ========================================= */
  const toggleListening = useCallback(() => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  }, [isListening, startListening, stopListening]);

  /* =========================================
      AUTO SEND AFTER FINAL TRANSCRIPT
  ========================================= */
  useEffect(() => {
    if (!transcript) return;

    askAI(transcript);
  }, [transcript, askAI]);

  /* =========================================
      DESTROY
  ========================================= */
  useEffect(() => {
    return () => {
      stopListening();
      stopSpeaking();
    };
  }, [stopListening, stopSpeaking]);

  /* =========================================
      RETURN
  ========================================= */
  return {
    isSupported,
    isListening,
    isSpeaking,
    isThinking,

    transcript,
    interimTranscript,
    reply,

    error,

    voiceEnabled,
    setVoiceEnabled,

    language,
    setLanguage,

    startListening,
    stopListening,
    toggleListening,

    askAI,
    speak,
    stopSpeaking,
  };
}