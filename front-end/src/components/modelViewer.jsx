import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js';
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js';
import './css/modelViewer.css'; // Import your CSS file for custom styles


const ModelViewer = ({ threeJsCode }) => {
  const mountRef = useRef();
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

      // Run the Three.js code and import necessary modules
      const wrappedFn = new Function('THREE', 'OrbitControls', 'window', 'document', 'requestAnimationFrame', 'FontLoader', 'TextGeometry', threeJsCode);
      wrappedFn(THREE, OrbitControls, window, document, requestAnimationFrame, FontLoader, TextGeometry);

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

  return <div className='threeJSRender' ref={mountRef}/>;
};

export default ModelViewer;