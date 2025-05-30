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
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Contraseña:
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-white/70 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-sm"
              placeholder="••••••••"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r bg-secondary text-white py-2 rounded-lg font-medium hover:shadow-lg transition-all duration-300 text-sm"
          >
            Iniciar sesión
          </button>

          <div className="flex justify-between text-xs mt-4">
            <Link to="/register" className="text-blue-600 hover:text-blue-800 hover:underline transition-colors">
              ¿No tienes cuenta?
            </Link>
            <Link to="/forgot-password" className="text-gray-600 hover:text-gray-800 hover:underline transition-colors">
              ¿Olvidaste tu contraseña?
            </Link>
            <a
              href="http://localhost:8000/auth/google"
              className="text-blue-600 hover:text-blue-800 hover:underline transition-colors"
            >
              Registrarse con Google
            </a>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
