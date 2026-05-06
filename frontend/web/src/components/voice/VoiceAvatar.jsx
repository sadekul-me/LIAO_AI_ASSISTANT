import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import {
  VRMLoaderPlugin,
  VRMHumanBoneName,
} from "@pixiv/three-vrm";

const VoiceAvatar = () => {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const vrmRef = useRef(null);
  const clockRef = useRef(new THREE.Clock());

  useEffect(() => {
    if (!canvasRef.current || !containerRef.current) return;

    // ==============================
    // 🎬 Scene Setup
    // ==============================
    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(24, 1, 0.1, 20);
    camera.position.set(0, 1.42, 1.6);
    camera.lookAt(0, 1.42, 0);

    const renderer = new THREE.WebGLRenderer({
      canvas: canvasRef.current,
      alpha: true,
      antialias: true,
      powerPreference: "high-performance",
    });

    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    // ==============================
    // 📐 Responsive Resize
    // ==============================
    const handleResize = () => {
      const { clientWidth, clientHeight } = containerRef.current;

      renderer.setSize(clientWidth, clientHeight);
      camera.aspect = clientWidth / clientHeight;
      camera.updateProjectionMatrix();
    };

    handleResize();
    window.addEventListener("resize", handleResize);

    // ==============================
    // 💡 Lighting Setup
    // ==============================
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.0);
    directionalLight.position.set(1, 2, 3);
    scene.add(directionalLight);

    // ==============================
    // 📦 Load VRM Model
    // ==============================
    const loader = new GLTFLoader();
    loader.register((parser) => new VRMLoaderPlugin(parser));

    loader.load(
      "/models/kotonoha.vrm",
      (gltf) => {
        const vrm = gltf.userData.vrm;
        vrmRef.current = vrm;

        scene.add(vrm.scene);
        vrm.scene.rotation.y = Math.PI;

        setupNaturalArmPose(vrm);
      },
      undefined,
      (error) => {
        console.error("VRM Load Error:", error);
      }
    );

    // ==============================
    // 🦾 Arm Pose Fix Function
    // ==============================
    const setupNaturalArmPose = (vrm) => {
      const humanoid = vrm.humanoid;

      const leftUpperArm = humanoid.getBoneNode(
        VRMHumanBoneName.LeftUpperArm
      );
      const rightUpperArm = humanoid.getBoneNode(
        VRMHumanBoneName.RightUpperArm
      );
      const leftLowerArm = humanoid.getBoneNode(
        VRMHumanBoneName.LeftLowerArm
      );
      const rightLowerArm = humanoid.getBoneNode(
        VRMHumanBoneName.RightLowerArm
      );

      if (leftUpperArm) leftUpperArm.rotation.z = 1.35;
      if (rightUpperArm) rightUpperArm.rotation.z = -1.35;
      if (leftLowerArm) leftLowerArm.rotation.y = -0.2;
      if (rightLowerArm) rightLowerArm.rotation.y = 0.2;

      console.log("✅ Arms set to natural pose");
    };

    // ==============================
    // 🔄 Animation Loop
    // ==============================
    const animate = () => {
      requestAnimationFrame(animate);

      const delta = clockRef.current.getDelta();
      const elapsedTime = clockRef.current.getElapsedTime();

      if (vrmRef.current) {
        updateAvatar(vrmRef.current, elapsedTime, delta);
      }

      renderer.render(scene, camera);
    };

    animate();

    // ==============================
    // 🧠 Avatar Animation Logic
    // ==============================
    const updateAvatar = (vrm, time, delta) => {
      // 👁 Blink Animation
      const blink = Math.sin(time * 2) > 0.98 ? 1 : 0;
      vrm.expressionManager?.setValue("blink", blink);

      // 🌬 Breathing Animation
      const spine = vrm.humanoid.getBoneNode(
        VRMHumanBoneName.Spine
      );

      if (spine) {
        spine.rotation.x = Math.sin(time) * 0.02;
      }

      vrm.update(delta);
    };

    // ==============================
    // 🧹 Cleanup
    // ==============================
    return () => {
      window.removeEventListener("resize", handleResize);
      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="w-full h-full flex items-center justify-center overflow-hidden bg-transparent relative"
    >
      <canvas
        ref={canvasRef}
        className="w-full h-full drop-shadow-[0_0_20px_rgba(0,255,255,0.15)]"
      />
    </div>
  );
};

export default VoiceAvatar;