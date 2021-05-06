import { MapContainer, TileLayer, Polyline } from "react-leaflet";

const Map = (leafletPositions) => {
  return (
    <MapContainer
      center={[59.324416, 18.046431]}
      zoom={13}
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Polyline
        pathOptions={{ color: "purple" }}
        positions={leafletPositions}
      />
    </MapContainer>
  );
};

export default Map;