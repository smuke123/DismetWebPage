import React from "react";
import { Link } from "react-router-dom";

const LoginForm = () => {
  return (
    <div className="p-4">
      <div className="bg-white/80 backdrop-blur-md rounded-xl shadow-xl p-6 border border-white/20">
        {/* Título */}
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
          Bienvenido de nuevo
        </h2>

        {/* Formulario */}
        <form className="space-y-5">
          {/* Email */}
          <div>
            <label 
              htmlFor="email" 
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Correo:
            </label>
            <input
              type="email"
              id="email"
              className="w-full px-3 py-2 rounded-lg bg-white/70 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-sm"
              placeholder="example@dismet.com"
            />
          </div>

          {/* Password */}
          <div>
            <label 
              htmlFor="password" 
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Contraseña:
            </label>
            <input
              type="password"
              id="password"
              className="w-full px-3 py-2 rounded-lg bg-white/70 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-sm"
              placeholder="••••••••"
            />
          </div>   

          {/* Botón Login */}
          <button
            type="submit"
            className="w-full bg-gradient-to-r bg-secondary text-white py-2 rounded-lg font-medium hover:shadow-lg transition-all duration-300 text-sm"
          >
            Iniciar sesión
          </button>

          {/* Links inferiores */}
          <div className="flex justify-between text-xs mt-4">
            <Link 
              to="/register" 
              className="text-blue-600 hover:text-blue-800 hover:underline transition-colors"
            >
              ¿No tienes cuenta?
            </Link>
            <Link 
              to="/forgot-password" 
              className="text-gray-600 hover:text-gray-800 hover:underline transition-colors"
            >
              ¿Olvidaste tu contraseña?
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
