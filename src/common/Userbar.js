import React from "react";
import { FaTimes } from "react-icons/fa";
import LoginForm from "../components/Auth/LoginForm";
import UserInfo from "../components/Auth/UserInfo";

const Userbar = ({ isUserbarOpen, closeUserbar }) => {
  const token = localStorage.getItem("token");

  return (
    <div
      style={{
        zIndex: "100",
        transform: `translateX(${isUserbarOpen ? "0%" : "100%"})`,
      }}
      className="fixed top-0 right-0 h-full w-80 bg-white shadow-lg transition-transform duration-300 ease-in-out overflow-y-auto"
    >
      {/* Encabezado */}
      <div className="border-b mb-4 bg-secondary flex justify-between items-center p-4">
        <h1 className="text-2xl font-semibold">Perfil de Usuario</h1>
        <button onClick={closeUserbar} className="text-gray-600 hover:text-black">
          <FaTimes size={20} />
        </button>
      </div>

      {/* Contenido */}
      <div className="p-6 text-center">
        {token ? <UserInfo /> : <LoginForm />}
      </div>
    </div>
  );
};

export default Userbar;
