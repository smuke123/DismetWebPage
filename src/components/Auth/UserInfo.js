import React, { useEffect, useState } from "react";

const UserInfo = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {

    const fetchUser = async () => {
      const token = localStorage.getItem("token");

      if (!token) return;

      const response = await fetch("http://localhost:8000/profile", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        console.error("Token inválido o expirado");
        localStorage.removeItem("token");
        return;
      }

      const userData = await response.json();
      setUser(userData);
    };

    fetchUser();
  }, []);

  if (!user) {
    return <p>Cargando información del usuario...</p>;
  }

  return (
    <div className="p-4 text-left">
      <h2 className="text-xl font-bold mb-4">Hola, {user.name || user.email}</h2>
      <p><strong>Correo:</strong> {user.email}</p>
      <p><strong>ID:</strong> {user.id}</p>

      <button
        onClick={() => {
          localStorage.removeItem("token");
          window.location.reload();
        }}
        className="mt-4 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
      >
        Cerrar sesión
      </button>
    </div>
  );
};

export default UserInfo;
