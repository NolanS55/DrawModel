import React, { useRef, useState } from 'react';
import { Stage, Layer, Line } from 'react-konva';
// Import Tailwind CSS for styling
import Slider from '@mui/material/Slider';
import './css/drawingCanvas.css'; // Import your CSS file for custom styles
import ModelViewer from './modelViewer';
const DrawingCanvas = () => {
  const [lines, setLines] = useState([]);
  const isDrawing = useRef(false);
  const stageRef = useRef();
  const [colour, setColour] = useState('black');
  const [size, setSize] = useState(5);
  var colours = ["green", "orange", "blue", "red", "purple", "pink", "yellow", "#654321", "black"];

  const [threeJsCode, setThreeJsCode] = useState("")

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

  const sizeUpdate = (event, newSize) => {
    setSize(newSize);
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

  const handleExport = async () => {
    
    // Get the image data from the canvas (base64-encoded)
  const uri = stageRef.current.toDataURL();

  // Prepare the payload for the API request
  const payload = {
    image_data: uri
  };

  try {
    // Send the POST request to the backend API
    const response = await fetch("http://127.0.0.1:8000/process-sketch", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload), // Send the image data as a JSON string
    });
    
    // Handle the response from the backend
    if (response.ok) {
      const result = await response.json();
      var prompt = result.prompt;
      
      prompt = prompt
       .replace(/^```javascript\s*/, '')   
        .replace(/```$/, '');
      setThreeJsCode(prompt);
      
      // Optionally, you can create a download link for the 3D model or show a success message
      alert("Successfully processed sketch and generated 3D model!");
    } else {
      console.error("Error processing the sketch:", response.statusText);
    }
  } catch (error) {
    console.error("Failed to send sketch to backend:", error);
  }
  };
  if (threeJsCode === "") {
  return (
    
    <div className="drawing">
      <div className='controls'>
      {colours.map((colour) => (
          <button
            key={colour}
            className={`bg-${colour}-600 text-white px-4 py-2 rounded hover:bg-${colour}-700`}
            onClick={() => changeColour(colour)}
          >
            {colour.charAt(0).toUpperCase() + colour.slice(1)}
          </button>
        ))}
        <button onClick={clearCanvas} className="clearCanvas">
          Clear Canvas  </button>
         <Slider sx={{ width: 300 }} defaultValue={2} step={1} min={1} max={10} onChange={sizeUpdate}></Slider> 
      </div>
        
      <Stage
        width={750}
        height={750}
        className="drawing-canvas"
        onMouseDown={handleMouseDown}
        onMousemove={handleMouseMove}
        onMouseup={handleMouseUp}
        ref={stageRef}
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
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        onClick={handleExport}
      >
        Export Drawing
      </button>
      

    </div>
  );
}
else {
return (<ModelViewer className="modelViewer" threeJsCode={threeJsCode}/>)
}
};

export default DrawingCanvas;