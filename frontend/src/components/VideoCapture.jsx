import React, { useRef, useEffect } from "react";

const VideoCapture = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const sendingRef = useRef(false); // ✅ useState 대신 useRef 사용 (리렌더링 방지)

  useEffect(() => {
    // ✅ 웹캠 스트림 가져오기
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => console.error("Error accessing webcam:", err));

    // ✅ 1초마다 캡처하여 백엔드로 전송 (sendingRef 사용)
    const interval = setInterval(() => {
      if (!sendingRef.current) {
        captureAndSendFrame();
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const captureAndSendFrame = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    sendingRef.current = true; // ✅ useRef로 상태 관리하여 리렌더링 방지

    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // ✅ 현재 프레임 캡처 (불필요한 상태 변경 방지)
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // ✅ 캡처된 이미지를 Blob으로 변환 후 백엔드 전송
    canvas.toBlob(async (blob) => {
      if (!blob) {
        sendingRef.current = false;
        return;
      }

      const formData = new FormData();
      formData.append("image", blob, "webcam.jpg");

      try {
        const response = await fetch("http://localhost:8000/emotion/analyze_webcam/", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();
        // console.log("🚀 Emotion Data:", data);
      } catch (error) {
        console.error("❌ Error sending frame:", error);
      } finally {
        sendingRef.current = false; // ✅ 요청 완료 후 상태 변경
      }
    }, "image/jpeg");
  };

  return (
    <div className="w-full h-full rounded-lg overflow-hidden">
      <video ref={videoRef} autoPlay playsInline className="w-full h-full object-cover"
      />
      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
};

export default VideoCapture;