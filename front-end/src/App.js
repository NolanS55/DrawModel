import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import CanvasPage from './pages/CanvasPage';
import './App.css';
function App() {

  return (
    <Router class="main">
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/canvas" element={<CanvasPage />} />
      </Routes>
    </Router>
  );
}

export default App;
