"use client";

import React, { useEffect, useMemo, useState } from "react";
import { GoogleMap, MarkerF, PolylineF, useJsApiLoader } from "@react-google-maps/api";
import { TripPlan } from "@/types";

const centerDefault = { lat: 48.1374, lng: 11.5755 }; // Munich

const COLORS = ["#FF5733", "#33C1FF", "#8DFF33", "#FFC133", "#FF33A8", "#33FFB5"];

type PlaceSearchMapProps = {
  tripPlan: TripPlan | null;
};

export default function PlaceSearchMap({ tripPlan }: PlaceSearchMapProps) {
  const [locations, setLocations] = useState<
    { date: string; places: { lat: number; lng: number; name: string }[] }[]
  >([]);

  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_KEY!,
    libraries: ["places"],
  });

  useEffect(() => {
    if (!tripPlan) return;

    const geocoder = new google.maps.Geocoder();

    const fetchGeocodes = async () => {
      const promises = tripPlan.days.map(async (day) => {
        const places = await Promise.all(
          day.places.map(async (p) => {
            if (!p.name || p.name.trim() === "") {
              console.warn("Skipping empty address");
              return {
                lat: 0,
                lng: 0,
                name: "Unknown Location",
              };
            }
        
            try {
              const result = await geocoder.geocode({ address: p.name });
              const location = result.results[0]?.geometry.location;
              if (!location) throw new Error("No location found");
        
              return {
                lat: location.lat(),
                lng: location.lng(),
                name: p.name,
              };
            } catch (err) {
              console.warn(`Geocoding failed for ${p.name}:`, err);
              return {
                lat: 0,
                lng: 0,
                name: p.name,
              };
            }
          })
        );
        

        return { date: day.date, places };
      });

      const resolved = await Promise.all(promises);
      setLocations(resolved);
    };

    fetchGeocodes();
  }, [tripPlan]);

  const center = useMemo(() => {
    const first = locations[0]?.places[0];
    return first?.lat && first?.lng ? { lat: first.lat, lng: first.lng } : centerDefault;
  }, [locations]);

  if (!isLoaded) return <div>Loading map...</div>;

  return (
    <div className="px-4 py-2">
      <GoogleMap zoom={13} center={center} mapContainerStyle={{ width: "100%", height: "500px" }}>
        {locations.map((day, idx) => (
          <React.Fragment key={day.date}>
            <PolylineF
              path={day.places.map((p) => ({ lat: p.lat, lng: p.lng }))}
              options={{
                strokeColor: COLORS[idx % COLORS.length],
                strokeOpacity: 0.8,
                strokeWeight: 4,
              }}
            />
            {day.places.map((place, pIdx) => (
              <MarkerF
                key={`${day.date}-${pIdx}`}
                position={{ lat: place.lat, lng: place.lng }}
                label={{
                  text: `${pIdx + 1}`,
                  fontSize: "12px",
                  color: "#000",
                }}
                title={place.name}
              />
            ))}
          </React.Fragment>
        ))}
      </GoogleMap>
    </div>
  );
}
