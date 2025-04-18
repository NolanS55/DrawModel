import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

const ModelViewer = ({ threeJsCode }) => {
  const mountRef = useRef();
  console.log('ModelViewer component mounted with threeJsCode: ', threeJsCode);
  useEffect(() => {
    const mount = mountRef.current;

    // Clear previous children
    while (mount.firstChild) {
      mount.removeChild(mount.firstChild);
    }

    try {
      // Patch document.body.appendChild to use the mount div
      const originalAppendChild = document.body.appendChild;
      document.body.appendChild = function (el) {
        mount.appendChild(el);
        return el;
      };

      // Run the Three.js code
      const wrappedFn = new Function('THREE', 'OrbitControls', 'window', 'document', 'requestAnimationFrame', threeJsCode);
      wrappedFn(THREE, OrbitControls, window, document, requestAnimationFrame);

      // Restore document.body.appendChild to avoid side effects
      document.body.appendChild = originalAppendChild;

      // Cleanup function: optional, depends on your threeJsCode
      return () => {
        while (mount.firstChild) {
          mount.removeChild(mount.firstChild);
        }
      };
    } catch (err) {
      console.error('Error rendering Three.js code:', err);
    }
  }, [threeJsCode]);

  return <div ref={mountRef} style={{ width: '100%', height: '100vh' }} />;
};

export default ModelViewer;