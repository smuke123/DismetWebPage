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
    <div className="p-4 text-left">
      <h2 className="text-xl font-bold mb-4">Hola, {user.nombre || user.correo}</h2>
      <p><strong>Correo:</strong> {user.correo}</p>
      <p><strong>ID:</strong> {user.id}</p>
      <p><strong>Username:</strong> {user.username}</p>
      <p><strong>Dirección:</strong> {user.direccion}</p>
      <p><strong>Teléfono:</strong> {user.telefono}</p>
      <p><strong>Rol:</strong> {user.rol ? "Admin" : "Usuario"}</p>

      <button
        onClick={() => {
          localStorage.removeItem("access_token");
          setUser(null);
          // Podés evitar recargar la página, simplemente forzar estado
        }}
        className="mt-4 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
      >
        Cerrar sesión
      </button>
    </div>
  );
};

export default UserInfo;


