"use client";
import React, { useState } from "react";
import { GoogleMap, MarkerF } from "@react-google-maps/api";
import usePlacesAutocomplete, {
  getGeocode,
  getLatLng,
} from "use-places-autocomplete";

type LatLng = {
  lat: number;
  lng: number;
};

export default function PlaceSearchMap() {
  const [marker, setMarker] = useState<LatLng | null>(null);
  const {
    ready,
    value,
    suggestions: { status, data },
    setValue,
    clearSuggestions,
  } = usePlacesAutocomplete({ debounce: 300 });

  const handleSelectPlace = async (description: string) => {
    setValue(description, false);
    clearSuggestions();
    const results = await getGeocode({ address: description });
    const { lat, lng } = await getLatLng(results[0]);
    setMarker({ lat, lng });
  };

  return (
    <div className="px-4 py-2">
      <input
        className="w-full border px-3 py-2 rounded-md"
        placeholder="Search a place..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        disabled={!ready}
      />
      {status === "OK" && (
        <ul className="bg-white shadow rounded-md mt-1">
          {data.map(({ place_id, description }) => (
            <li
              key={place_id}
              className="p-2 hover:bg-gray-100 cursor-pointer"
              onClick={() => handleSelectPlace(description)}
            >
              {description}
            </li>
          ))}
        </ul>
      )}
      <GoogleMap
        zoom={13}
        center={marker ?? { lat: 25.034, lng: 121.5623 }}
        mapContainerStyle={{ width: "100%", height: "400px" }}
      >
        {marker && <MarkerF position={marker} />}
      </GoogleMap>
    </div>
  );
}
