import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { VRMLoaderPlugin, VRMHumanBoneName } from '@pixiv/three-vrm';

const VoiceAvatar = () => {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const vrmRef = useRef(null);
  const clockRef = useRef(new THREE.Clock());

  useEffect(() => {
    const scene = new THREE.Scene();
    
    // 🎥 আল্ট্রা প্রিমিয়াম ক্যামেরা ভিউ
    const camera = new THREE.PerspectiveCamera(24, 1, 0.1, 20);
    camera.position.set(0, 1.42, 1.6); // একদম পারফেক্ট চেস্ট-আপ হাইট
    camera.lookAt(0, 1.42, 0);

    const renderer = new THREE.WebGLRenderer({
      canvas: canvasRef.current,
      alpha: true,
      antialias: true,
      powerPreference: "high-performance"
    });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    const updateSize = () => {
      if (!containerRef.current) return;
      const { clientWidth, clientHeight } = containerRef.current;
      renderer.setSize(clientWidth, clientHeight);
      camera.aspect = clientWidth / clientHeight;
      camera.updateProjectionMatrix();
    };
    updateSize();
    window.addEventListener('resize', updateSize);

    // 💡 লাইটিং সেটআপ
    scene.add(new THREE.AmbientLight(0xffffff, 0.7));
    const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
    dirLight.position.set(1, 2, 3);
    scene.add(dirLight);

    const loader = new GLTFLoader();
    loader.register((parser) => new VRMLoaderPlugin(parser));

    loader.load(
      '/models/kotonoha.vrm', 
      (gltf) => {
        const vrm = gltf.userData.vrm;
        vrmRef.current = vrm;
        scene.add(vrm.scene);
        vrm.scene.rotation.y = Math.PI;

        // 🛠 হাত নামানোর ফোর্সফুল মেথড (Standard VRM Humanoid Bone Names)
        const humanoid = vrm.humanoid;
        
        // হাড়গুলো খুঁজে বের করে রোটেশন সেট করা
        const leftUpperArm = humanoid.getBoneNode(VRMHumanBoneName.LeftUpperArm);
        const rightUpperArm = humanoid.getBoneNode(VRMHumanBoneName.RightUpperArm);
        const leftLowerArm = humanoid.getBoneNode(VRMHumanBoneName.LeftLowerArm);
        const rightLowerArm = humanoid.getBoneNode(VRMHumanBoneName.RightLowerArm);

        if (leftUpperArm) leftUpperArm.rotation.z = 1.35; 
        if (rightUpperArm) rightUpperArm.rotation.z = -1.35;
        if (leftLowerArm) leftLowerArm.rotation.y = -0.2;
        if (rightLowerArm) rightLowerArm.rotation.y = 0.2;

        console.log("Arms forced to Natural Pose");
      },
      undefined,
      (error) => console.error(error)
    );

    const animate = () => {
      requestAnimationFrame(animate);
      const delta = clockRef.current.getDelta();
      const time = clockRef.current.getElapsedTime();

      if (vrmRef.current) {
        // ১. ব্লিঙ্কিং
        const blinkValue = Math.sin(time * 2) > 0.98 ? 1 : 0;
        vrmRef.current.expressionManager.setValue('blink', blinkValue);
        
        // ২. হালকা শ্বাস নেওয়ার মুভমেন্ট
        const spine = vrmRef.current.humanoid.getBoneNode(VRMHumanBoneName.Spine);
        if (spine) spine.rotation.x = Math.sin(time) * 0.02;

        vrmRef.current.update(delta);
      }
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      window.removeEventListener('resize', updateSize);
      renderer.dispose();
    };
  }, []);

  return (
    <div ref={containerRef} className="w-full h-full relative flex justify-center items-center overflow-hidden bg-transparent">
      <canvas ref={canvasRef} className="w-full h-full drop-shadow-[0_0_20px_rgba(0,255,255,0.15)]" />
    </div>
  );
};

export default VoiceAvatar;