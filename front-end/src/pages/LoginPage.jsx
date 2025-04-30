import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../components/css/loginPage.css';
function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    const payload = {
      email : loginEmail,
      password : loginPassword
    };
  
    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
  
      if (response.ok) {
        navigate("/canvas");
      } else {
        const errorData = await response.json();
        alert(errorData.detail || "Invalid credentials");
      }
    } catch (error) {
      console.error("Login failed:", error);
      alert("Something went wrong. Please try again later.");
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
  
    const payload = {
      email,
      password
    };
  
    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
  
      if (response.ok) {
        navigate("/canvas");
      } else {
        const errorData = await response.json();
        alert(errorData.detail || "Registration failed");
      }
    } catch (error) {
      console.error("Registration failed:", error);
      alert("Something went wrong. Please try again later.");
    }
  };

  return (
    <div className='main'>
 <form onSubmit={handleLogin}>
      <h1>Login</h1>
      <input value={loginEmail} onChange={(e) => setLoginEmail(e.target.value)} placeholder="Email" />
      <input value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} placeholder="Password" type="password" />
      <button type="submit">Login</button>
    </form>
    <form onSubmit={handleRegister}>
    <h1>Register</h1>
    <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
    <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" />
    <button type="submit">Register</button>
  </form>
    </div>
   
  );
}

export default LoginPage;