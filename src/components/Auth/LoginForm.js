import React, { useState } from "react";
import { Link } from "react-router-dom";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault(); // evita el submit tradicional que recarga la página

    const response = await fetch("http://localhost:8000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      alert("Credenciales incorrectas");
      return;
    }

    const data = await response.json();
    console.log("Token recibido:", data.access_token);

    // Guardar el token en localStorage
    localStorage.setItem("token", data.access_token);

    // Redirigir al usuario a donde quieras, por ejemplo /dashboard
    window.location.href = "/";
    };

  return (
    <div className="p-4">
      <div className="bg-white/80 backdrop-blur-md rounded-xl shadow-xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
          Bienvenido de nuevo
        </h2>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Correo:
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-white/70 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-sm"
              placeholder="example@dismet.com"
              required
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-3">
              Contraseña:
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-white/70 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-sm mb-3"
              placeholder="••••••••"
              required
            />
          </div>
          
          <div>
            <button
              type="submit"
              className="block w-full bg-gradient-to-r bg-secondary text-white py-2 rounded-lg font-medium hover:shadow-lg transition-all duration-300 text-sm mb-6 mt-6"
            >
              Iniciar sesión
            </button>
          </div>

          <div className="flex items-center justify-center text-xs mt-2">
            <Link to="/register" className="text-blue-600 hover:text-blue-800 hover:underline transition-colors">
              ¿No tienes cuenta?
            </Link>
          </div>
          
          <div className="flex justify-between text-xs mt-3">

<a href="http://localhost:8000/auth/google" className="w-full block">
  <button
    type="button"
    className="w-full flex items-center justify-center gap-2 bg-white border border-gray-300 py-2 px-4 rounded-md shadow hover:bg-gray-100 transition-all"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 48 48"
      className="w-6 h-6"
    >
      <path
        fill="#EA4335"
        d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
      />
      <path
        fill="#4285F4"
        d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
      />
      <path
        fill="#FBBC05"
        d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
      />
      <path
        fill="#34A853"
        d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
      />
      <path fill="none" d="M0 0h48v48H0z" />
    </svg>
    <span className="text-sm font-medium text-gray-700">Registrarse con Google</span>
  </button>
</a>


          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
