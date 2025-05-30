import React, { useEffect, useState } from "react";
import LoginForm from "./LoginForm";

const UserInfo = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setUser(null);  // No token, no user
        return;
      }

      const response = await fetch("http://localhost:8000/usuarios/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        console.error("Token inválido o expirado");
        localStorage.removeItem("access_token");
        setUser(null);
        return;
      }

      const userData = await response.json();
      setUser(userData);
    };

    fetchUser();
  }, []);

  if (!user) {
    return <LoginForm />;
  }

  return (
    <div className="bg-white/80 backdrop-blur-md rounded-xl shadow-xl p-6 border border-white/20 text-gray-800 space-y-4 mb-3 mt-3">
      <h2 className="text-2xl font-bold text-center mb-4">
        ¡Bienvenido, {user.nombre || user.username || user.correo}!
      </h2>

      <div className="text-sm space-y-2">
        <div className="flex justify-between">
          <span className="font-medium text-gray-600">Correo:</span>
          <span>{user.correo}</span>
        </div>
        <div className="flex justify-between">
          <span className="font-medium text-gray-600">ID:</span>
          <span>{user.id}</span>
        </div>
        <div className="flex justify-between">
          <span className="font-medium text-gray-600">Username:</span>
          <span>{user.username}</span>
        </div>
        <div className="flex justify-between">
          <span className="font-medium text-gray-600">Dirección:</span>
          <span>{user.direccion || "No registrada"}</span>
        </div>
        <div className="flex justify-between">
          <span className="font-medium text-gray-600">Teléfono:</span>
          <span>{user.telefono || "No registrado"}</span>
        </div>
        <div className="flex justify-between">
          <span className="font-medium text-gray-600">Rol:</span>
          <span className="font-semibold">
            {user.rol ? "Administrador" : "Usuario"}
          </span>
        </div>
      </div>

        <div className="mt-3">
            <button
                onClick={() => {
                localStorage.removeItem("access_token");
                setUser(null);
                // Podés evitar recargar la página, simplemente forzar estado
                }}
                type="submit"
                className="block w-full bg-gradient-to-r bg-secondary text-white py-2 rounded-lg font-medium hover:shadow-lg transition-all duration-300 text-sm mb-6 mt-6"
            >
                Cerrar sesión
            </button>
        </div>
    </div>
  );
};

export default UserInfo;


