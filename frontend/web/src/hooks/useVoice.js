import { useState, useRef, useEffect, useCallback } from "react";

/* ==================================================
   useVoice Hook
   Speech Recognition + Speech Synthesis
   Clean / Browser Ready / Scalable
================================================== */

export default function useVoice() {
  /* =========================================
     STATE
  ========================================= */
  const [isSupported, setIsSupported] =
    useState(false);

  const [isListening, setIsListening] =
    useState(false);

  const [transcript, setTranscript] =
    useState("");

  const [interimTranscript, setInterimTranscript] =
    useState("");

  const [error, setError] =
    useState(null);

  const [voiceEnabled, setVoiceEnabled] =
    useState(true);

  const [language, setLanguage] =
    useState("en-US");

  const [voices, setVoices] =
    useState([]);

  const [selectedVoice, setSelectedVoice] =
    useState(null);

  const recognitionRef = useRef(null);

  /* =========================================
     INIT
  ========================================= */
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    const speechSupported =
      !!SpeechRecognition &&
      !!window.speechSynthesis;

    setIsSupported(speechSupported);

    if (!speechSupported) return;

    const recognition =
      new SpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = language;

    recognition.onstart = () => {
      setIsListening(true);
      setError(null);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      setError(
        event?.error ||
          "Voice error"
      );

      setIsListening(false);
    };

    recognition.onresult = (event) => {
      let finalText = "";
      let interim = "";

      for (
        let i = event.resultIndex;
        i < event.results.length;
        i++
      ) {
        const result =
          event.results[i];

        const text =
          result[0].transcript;

        if (result.isFinal) {
          finalText += text + " ";
        } else {
          interim += text;
        }
      }

      if (finalText) {
        setTranscript(
          (prev) =>
            prev + finalText
        );
      }

      setInterimTranscript(
        interim
      );
    };

    recognitionRef.current =
      recognition;

    loadVoices();

    window.speechSynthesis.onvoiceschanged =
      loadVoices;

    return () => {
      recognition.stop();
    };
  }, [language]);

  /* =========================================
     LOAD VOICES
  ========================================= */
  const loadVoices =
    useCallback(() => {
      const list =
        window.speechSynthesis.getVoices();

      setVoices(list);

      if (
        list.length > 0 &&
        !selectedVoice
      ) {
        setSelectedVoice(
          list[0]
        );
      }
    }, [selectedVoice]);

  /* =========================================
     LISTENING CONTROL
  ========================================= */
  const startListening =
    useCallback(() => {
      if (
        !isSupported ||
        !recognitionRef.current
      )
        return;

      setTranscript("");
      setInterimTranscript("");
      setError(null);

      try {
        recognitionRef.current.lang =
          language;

        recognitionRef.current.start();
      } catch {}
    }, [isSupported, language]);

  const stopListening =
    useCallback(() => {
      recognitionRef.current?.stop();
    }, []);

  const toggleListening =
    useCallback(() => {
      if (isListening) {
        stopListening();
      } else {
        startListening();
      }
    }, [
      isListening,
      startListening,
      stopListening,
    ]);

  /* =========================================
     SPEAK
  ========================================= */
  const speak =
    useCallback(
      (text) => {
        if (
          !voiceEnabled ||
          !text?.trim()
        )
          return;

        if (
          !window.speechSynthesis
        )
          return;

        window.speechSynthesis.cancel();

        const utterance =
          new SpeechSynthesisUtterance(
            text
          );

        utterance.lang =
          language;

        if (selectedVoice) {
          utterance.voice =
            selectedVoice;
        }

        utterance.rate = 1;
        utterance.pitch = 1;
        utterance.volume = 1;

        window.speechSynthesis.speak(
          utterance
        );
      },
      [
        voiceEnabled,
        language,
        selectedVoice,
      ]
    );

  const stopSpeaking =
    useCallback(() => {
      window.speechSynthesis?.cancel();
    }, []);

  /* =========================================
     TEXT CONTROL
  ========================================= */
  const clearTranscript =
    useCallback(() => {
      setTranscript("");
      setInterimTranscript("");
    }, []);

  /* =========================================
     SETTINGS
  ========================================= */
  const toggleVoice =
    useCallback(() => {
      setVoiceEnabled(
        (prev) => !prev
      );
    }, []);

  /* =========================================
     EXPORT
  ========================================= */
  return {
    isSupported,
    isListening,

    transcript,
    interimTranscript,

    error,

    voiceEnabled,
    language,

    voices,
    selectedVoice,

    startListening,
    stopListening,
    toggleListening,

    speak,
    stopSpeaking,

    clearTranscript,

    toggleVoice,
    setLanguage,
    setSelectedVoice,
  };
}