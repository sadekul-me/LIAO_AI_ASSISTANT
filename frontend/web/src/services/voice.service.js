import api from "./api";

/* ==================================================
   VOICE SERVICE
   Speech To Text / Text To Speech / Mic
================================================== */

/* =========================================
   TEXT TO SPEECH
========================================= */
export const speakText =
  async (text) => {
    try {
      const cleanText =
        String(
          text || ""
        ).trim();

      if (!cleanText) {
        throw new Error(
          "Text required."
        );
      }

      const res =
        await api.post(
          "/voice/tts",
          {
            text:
              cleanText,
          }
        );

      return {
        success: true,
        data: res.data,
      };
    } catch (error) {
      throw {
        success: false,
        message:
          error.message ||
          "TTS failed.",
      };
    }
  };

/* =========================================
   SPEECH TO TEXT
========================================= */
export const speechToText =
  async (audioBlob) => {
    try {
      const formData =
        new FormData();

      formData.append(
        "file",
        audioBlob
      );

      const res =
        await api.post(
          "/voice/stt",
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data",
            },
          }
        );

      return {
        success: true,
        text:
          res.data?.text ||
          "",
        raw: res.data,
      };
    } catch (error) {
      throw {
        success: false,
        message:
          error.message ||
          "Speech recognition failed.",
      };
    }
  };

/* =========================================
   CHECK MIC PERMISSION
========================================= */
export const requestMicPermission =
  async () => {
    try {
      const stream =
        await navigator.mediaDevices.getUserMedia(
          {
            audio: true,
          }
        );

      stream
        .getTracks()
        .forEach((track) =>
          track.stop()
        );

      return {
        success: true,
        granted: true,
      };
    } catch {
      return {
        success: true,
        granted: false,
      };
    }
  };

/* =========================================
   START RECORDING
========================================= */
export const startRecording =
  async () => {
    try {
      const stream =
        await navigator.mediaDevices.getUserMedia(
          {
            audio: true,
          }
        );

      const mediaRecorder =
        new MediaRecorder(
          stream
        );

      const chunks = [];

      mediaRecorder.ondataavailable =
        (event) => {
          if (
            event.data.size >
            0
          ) {
            chunks.push(
              event.data
            );
          }
        };

      mediaRecorder.start();

      return {
        success: true,
        recorder:
          mediaRecorder,
        stream,
        chunks,
      };
    } catch (error) {
      throw {
        success: false,
        message:
          "Unable to start recording.",
      };
    }
  };

/* =========================================
   STOP RECORDING
========================================= */
export const stopRecording =
  (
    recorder,
    stream,
    chunks = []
  ) => {
    return new Promise(
      (resolve) => {
        if (!recorder) {
          resolve(null);
          return;
        }

        recorder.onstop =
          () => {
            const blob =
              new Blob(
                chunks,
                {
                  type: "audio/webm",
                }
              );

            stream
              ?.getTracks()
              ?.forEach(
                (
                  track
                ) =>
                  track.stop()
              );

            resolve({
              success: true,
              blob,
            });
          };

        recorder.stop();
      }
    );
  };

/* =========================================
   GET AVAILABLE VOICES
========================================= */
export const getBrowserVoices =
  () => {
    if (
      !window.speechSynthesis
    )
      return [];

    return window.speechSynthesis.getVoices();
  };