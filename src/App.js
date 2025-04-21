import './styles/App.css';
import Layout from './components/layout';
import Home from './pages/home';
import Detail from './pages/detail';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
/* 
import Cart from "./components/Cart"; // Ya está en components
import NavBar from "./components/NavBar"; // Nuevo componente de navegación
import Footer from "./components/Footer"; // Nuevo componente de pie de página 
// */

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<Home />} />
          <Route path='/:slug' element={<Detail />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
