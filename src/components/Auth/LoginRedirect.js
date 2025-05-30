import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

const LoginRedirect = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const token = params.get("token");

    if (token) {
        localStorage.setItem("access_token", token);
        fetch("http://localhost:8000/usuarios/me", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then((res) => {
          if (!res.ok) throw new Error("No autorizado");
          return res.json();
        })
        .then((data) => {
          console.log("Usuario logueado con Google:", data);
          // Redirige a home o dashboard
          navigate("/");
        })
        .catch((err) => {
          console.error("Error al obtener usuario:", err);
          // Si no se pudo, redirige a login
          navigate("/login");
        });

      // Limpia la URL para que no quede el token visible
      window.history.replaceState({}, document.title, "/");

      // Redirige a home o dashboard
      navigate("/");
    } else {
      // No hay token, redirige a login
      navigate("/login");
    }
  }, [location, navigate]);

  return <p>Iniciando sesión con Google...</p>;
};

export default LoginRedirect;
