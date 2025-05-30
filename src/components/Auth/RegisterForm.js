import React from "react";

const RegisterForm = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-white mb-3">
      <div className="w-8 max-w-sm p-6 bg-white border border-gray-200 rounded-xl shadow-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
          Crear una cuenta
        </h2>

        <form className="space-y-4">
          {/* Nombre */}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-10 mt-10">
              Nombre completo
            </label>
            <input
              type="text"
              id="name"
              placeholder="John Doe"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3 mt-3"
            />
          </div>

          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-10 mt-10">
              Dirección de Correo
            </label>
            <input
              type="email"
              id="email"
              placeholder="example@dismet.com"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3 mt-3"
            />
          </div>

          {/* Username */}
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-10 mt-10">
              Nombre de usuario
            </label>
            <input
              type="text"
              id="username"
              placeholder="username123"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3 mt-3"
            />
          </div>

          {/* Dirección */}
          <div>
            <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-10 mt-10">
              Dirección
            </label>
            <input
              type="text"
              id="address"
              placeholder="123 Main St"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3 mt-3"
            />
          </div>

          {/* Teléfono */}
          <div>
            <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-10 mt-10">
              Teléfono
            </label>
            <input
              type="tel"
              id="phone"
              placeholder="+57 300 123 4567"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3 mt-3"
            />
          </div>

          {/* Contraseña */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Contraseña
            </label>
            <input
              type="password"
              id="password"
              placeholder="••••••••"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3 mt-3"
            />
          </div>

          {/* ROL (Administrador o Usuario) */}
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="rol"
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 mb-3 mt-3"
            />
            <label htmlFor="rol" className="text-sm text-gray-700">
              ¿Registrar como administrador?
            </label>
          </div>

          {/* Botón de registro */}
          <button
            type="submit"
            className="w-full bg-accent text-primary font-semibold py-2 px-4 rounded-md hover:bg-blue-700 transition-all mb-3 mt-3"
          >
            Register
          </button>
        </form>
      </div>
    </div>
  );
};

export default RegisterForm;
