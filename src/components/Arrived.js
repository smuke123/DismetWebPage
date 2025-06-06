import { arriveItems } from "../data/Data";
import Heading from "../common/Heading";
import { Link } from "react-router-dom";
import { FaInstagram } from "react-icons/fa";

const Arrived = () => {
  return (
    <div>
      <div className="w-10/12 m-auto">
        <Heading heading={"Just Arrived"} />
        <div className="flex items-center mt-10">
          <div className="w-2/3">
            <h1 className="font-semibold text-3xl">Tienda de Instagram</h1>
            <p className="my-4">
              Etiquétanos @ en tus fotos de Instagram para salir en esta sección.
            </p>
            <a
              className="border bg-accent rounded-full text-white px-4 py-2"
              to={"instagram.com"}
            >
              Visita nuestro Instagram
            </a>
          </div>
          <div className="grid grid-cols-3 gap-4 mb-8">
            {arriveItems.map((item, index) => (
              <div key={index}>
                <div className="">
                  <div
                    className={`relative rounded-3xl overflow-hidden ${
                      index === 4 ? "fifth-image" : ""
                    }`}
                  >
                    <img
                      src={item.img}
                      alt="img"
                      className="rounded-3xl hover:scale-110 transition-all duration-500"
                    />

                    <div className="absolute bottom-0 right-0 p-3 bg-white  rounded-xl">
                      <div className=" p-1 bg-yellow rounded-full text-white">
                        <FaInstagram />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Arrived;
