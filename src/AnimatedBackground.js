
import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import smokeImage from "./smokeImage.png";

const AnimatedBackground = () => {
  const mount = useRef(null);
  const scene = useRef(null);
  const camera = useRef(null);
  const renderer = useRef(null);

  useEffect(() => {
    if (!mount.current) return; // Check if mount.current is available

    scene.current = new THREE.Scene();
    camera.current = new THREE.PerspectiveCamera(
      75,
      mount.current.offsetWidth / mount.current.offsetHeight,
      1,
      10000
    );
    camera.current.position.z = 1000;

    renderer.current = new THREE.WebGLRenderer();
    renderer.current.setSize(mount.current.offsetWidth, mount.current.offsetHeight);
    mount.current.appendChild(renderer.current.domElement);

    const light = new THREE.DirectionalLight(0xffffff, 0.5);
    light.position.set(-1, 0, 1);
    scene.current.add(light);

    const smokeGeo = new THREE.PlaneGeometry(300, 300);
    const smokeParticles = [];

    const clock = new THREE.Clock();
    let delta = 0;

    new THREE.TextureLoader().load(smokeImage, function (smokeTexture) {
      const smokeMaterial = new THREE.MeshLambertMaterial({
        color: 0x2596be,
        map: smokeTexture,
        transparent: true,
      });

      for (let p = 0; p < 150; p++) {
        const particle = new THREE.Mesh(smokeGeo, smokeMaterial);
        particle.position.set(Math.random() * 500 - 250, Math.random() * 500 + 10, Math.random() * 1000 - 100);
        particle.rotation.z = Math.random() * 360;
        scene.current.add(particle);
        smokeParticles.push(particle);
      }

      const animate = () => {
        if (!renderer.current) return; // Check if renderer.current is available
        delta = clock.getDelta();
        smokeParticles.forEach(p => {
          p.rotation.z += (delta * 0.2);
        });

        requestAnimationFrame(animate);
        renderer.current.render(scene.current, camera.current);
      };
      animate();
    });

    const handleResize = () => {
      camera.current.aspect = mount.current.offsetWidth / mount.current.offsetHeight;
      camera.current.updateProjectionMatrix();
      renderer.current.setSize(mount.current.offsetWidth, mount.current.offsetHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (mount.current && renderer.current) {
        mount.current.removeChild(renderer.current.domElement);
      }
      renderer.current = null;
    };

  }, []);

  return <div ref={mount} style={{ width: '100%', height: '100%' }} />;
};

export default AnimatedBackground;