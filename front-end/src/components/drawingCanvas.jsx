import React, { useRef, useState, useEffect } from 'react';
import { Stage, Layer, Line } from 'react-konva';
import './css/drawingCanvas.css'; // Import your CSS file custom styles
import ModelViewer from './modelViewer';
const DrawingCanvas = () => {

  // State to hold lines, and drawing properties
  const [lines, setLines] = useState([]);
  const isDrawing = useRef(false);
  const stageRef = useRef();
  const [colour, setColour] = useState('black');
  const size = 5 // Default siz
  var colours = ["green", "orange", "blue", "red", "purple", "pink", "yellow", "#654321", "black", "white"];

  // State to hold the Three.js code
  const [threeJsCode, setThreeJsCode] = useState(` const scene = new THREE.Scene();

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    const WIDTH = 1000;
    const HEIGHT = 700;
    renderer.setSize(WIDTH, HEIGHT);
    renderer.setClearColor(0x82C8E5);
    document.body.appendChild(renderer.domElement);

    // Camera
    const camera = new THREE.PerspectiveCamera(
      75, WIDTH / HEIGHT, 0.1, 1000
    );
    camera.position.set(3, 2, 0);

    // Ground
    const planeGeometry = new THREE.PlaneGeometry(20, 20);
    const planeMaterial = new THREE.MeshLambertMaterial({ color: 0x228B22 });
    const plane = new THREE.Mesh(planeGeometry, planeMaterial);
    plane.rotation.x = -Math.PI / 2;
    scene.add(plane);

    // Pine Tree - Trunk
    const trunkGeometry = new THREE.CylinderGeometry(0.2, 0.2, 1.5, 8);
    const trunkMaterial = new THREE.MeshLambertMaterial({ color: 0x8B4513 });
    const trunk = new THREE.Mesh(trunkGeometry, trunkMaterial);
    trunk.position.y = 0.75;
    scene.add(trunk);

    // Pine Tree - Foliage
    const createCone = (radius, height, yOffset) => {
      const geometry = new THREE.ConeGeometry(radius, height, 8);
      const material = new THREE.MeshLambertMaterial({ color: 0x006400 });
      const cone = new THREE.Mesh(geometry, material);
      cone.position.y = yOffset;
      return cone;
    };

    const foliage1 = createCone(1.2, 1.5, 1.8);
    const foliage2 = createCone(1.0, 1.2, 2.7);
    const foliage3 = createCone(0.8, 1.0, 3.4);
    scene.add(foliage1, foliage2, foliage3);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 10, 7.5);
    scene.add(directionalLight);

    // Orbit animation
    let angle = 0;
    function animate() {
      requestAnimationFrame(animate);

      angle += 0.01;
      const radius = 5;
      camera.position.x = Math.cos(angle) * radius;
      camera.position.z = Math.sin(angle) * radius;
      camera.position.y = 2;
      camera.lookAt(0, 1.5, 0);

      renderer.render(scene, camera);
    }

    animate();`)

    const [d3View, set3dView] = useState(false);
    const toggle3dView = () => {
      set3dView(!d3View);
    };

  // State to hold the stage dimensions
  const [stageWidth, setStageWidth] = useState(0);
  const [stageHeight, setStageHeight] = useState(0);
  useEffect(() => {
    const updateSize = () => {
      if (stageRef.current) {
        setStageWidth(window.innerWidth);
        setStageHeight(window.innerHeight);
      }
    };

    // Set initial size
    updateSize();

    // Add resize event listener
    window.addEventListener('resize', updateSize);

    return () => {
      window.removeEventListener('resize', updateSize);
    };
  }, []);

//General code for drawing canvas
  const handleMouseDown = () => {
    isDrawing.current = true;
    setLines([...lines, { points: [], colour, size }]);
  };

  const changeColour = (newColour) => {
    setColour(newColour);
  }

  const clearCanvas = () => {
    setLines([]);
  }

  const handleMouseMove = (e) => {
    if (!isDrawing.current) return;
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
  
    let lastLine = lines[lines.length - 1];
    const updatedLine = {
      ...lastLine,
      points: [...lastLine.points, point]
    };
  
    const newLines = [...lines.slice(0, -1), updatedLine];
    setLines(newLines);
  };

  const handleMouseUp = () => {
    isDrawing.current = false;
  };

  const handleAddToScene = async () => {
    const uri = stageRef.current.toDataURL();

    // Get the image data from the canvas
    const payload = {
      image_data: uri,
      threeJsCode : threeJsCode,
      width : stageWidth * .75,
      height : stageHeight * .75
    };

    try {
      // Send the POST request to the backend API
      const response = await fetch("http://127.0.0.1:8000/add-to-scene", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      
      // Handle the response from the backend
      if (response.ok) {
        const result = await response.json();
        var prompt = result.prompt;
        
        prompt = prompt
         .replace(/^```javascript\s*/, '')   
          .replace(/```$/, '');
        setThreeJsCode(prompt);
        
        // scroll to the model viewer section
        
        
        toggle3dView();
        
      } else {
        console.error("Error processing the sketch:", response.statusText);
      }
    } catch (error) {
      console.error("Failed to send sketch to backend:", error);
    }
  };

  const handleExport = async () => {
    
  // Get the image data from the canvas
  const uri = stageRef.current.toDataURL();

  const payload = {
    image_data: uri,
    width : stageWidth * .75,
    height : stageHeight * .75
  };

  try {
    // Send the POST request to the backend API
    const response = await fetch("http://127.0.0.1:8000/process-sketch", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    
    // Handle the response from the backend
    if (response.ok) {
      const result = await response.json();
      var prompt = result.prompt;
      
      prompt = prompt
       .replace(/^```javascript\s*/, '')   
        .replace(/```$/, '');
      setThreeJsCode(prompt);
      
      // scroll to the model viewer section
      
      
      toggle3dView();
      
    } else {
      console.error("Error processing the sketch:", response.statusText);
    }
  } catch (error) {
    console.error("Failed to send sketch to backend:", error);
  }
  
  };

  return (
    
    <div className="drawing">
      <h1 className="drawingTitle" style={{ display: d3View ? 'none' : 'block' }}>Drawing Canvas</h1>
      <div className='drawingArea' style={{ display: d3View ? 'none' : 'block' }}>
      
      <div className='controls'>
      {colours.map((colour) => (
          
          <button
            key={colour}
            className={`colorSwatch ${colour}`}
            onClick={() => changeColour(colour)}
          >
          </button>
        ))}
        <button onClick={clearCanvas} className="clearCanvas">
        🗑️ Clear Canvas  </button>
        
      </div>
        
      <Stage
        width={stageWidth * .75}
        height={stageHeight * .75}
        className="drawingCanvas"
        onMouseDown={handleMouseDown}
        onMousemove={handleMouseMove}
        onMouseup={handleMouseUp}
        ref={stageRef}
        style={{ width: '100%', height: '100%' }}
      >
        <Layer>


          {    
          lines.map((line, i) => (
            <Line
              key={i}
              points={line.points.flatMap(p => [p.x, p.y])}
              stroke={line.colour}
              strokeWidth={line.size}
              tension={0.5}
              lineCap="round"
              lineJoin="round"
            />
          ))}
        </Layer>
      </Stage>
      <button
        className="exportButton"
        onClick={handleExport}
      >
        🧊 Turn 3D
      </button>
      <button
        className="exportButton"
        onClick={toggle3dView}
      >
           ↔️ Switch Viewing
      </button>
      <button
        className="exportButton"
        onClick={toggle3dView}
      >
           ➕ Add to Scene
      </button>

      </div>
      <section id="model" className="modelViewerSection" style={{ display: d3View ? 'block' : 'none' }}>
        <h2 className="modelViewerTitle">3D Model Viewer</h2>
        <ModelViewer className="modelViewer" threeJsCode={threeJsCode}/>
        <button
        className="d3SwapButton"
        onClick={toggle3dView}
      >
        ↔️ Switch Viewing
      </button>
        </section>
    </div>
  );
};

export default DrawingCanvas;