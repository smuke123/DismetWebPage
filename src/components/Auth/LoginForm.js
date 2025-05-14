import React from "react";
import { Link } from "react-router-dom";

const LoginForm = () => {
  return (
    <div className="max-w-md mx-auto p-8">
      {/* Contenedor 3D/Glass */}
      <div className="bg-white/80 backdrop-blur-md rounded-xl shadow-2xl p-8 border border-white/20 transform transition-all hover:scale-[1.02]">
        {/* Título */}
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
          Welcome Back
        </h2>

        {/* Formulario */}
        <form className="space-y-6">
          {/* Email */}
          <div>
            <label 
              htmlFor="email" 
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Tu correo:
            </label>
            <input
              type="email"
              id="email"
              className="w-full px-4 py-3 rounded-lg bg-white/70 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              placeholder="example@dismet.com"
            />
          </div>

          {/* Password */}
          <div>
            <label 
              htmlFor="password" 
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Tu contraseña:
            </label>
            <input
              type="password"
              id="password"
              className="w-full px-4 py-3 rounded-lg bg-white/70 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              placeholder="••••••••"
            />
          </div>

          {/* Botón Login */}
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-blue-600 to-blue-500 text-white py-3 px-4 rounded-lg font-medium hover:shadow-lg transition-all duration-300"
          >
            Sign In
          </button>

          {/* Links inferiores */}
          <div className="flex justify-between text-sm mt-4">
            <Link 
              to="/register" 
              className="text-blue-600 hover:text-blue-800 hover:underline transition-colors"
            >
              ¿No tienes una cuenta?
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