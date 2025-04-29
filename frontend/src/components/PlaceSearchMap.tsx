"use client";

import React, { useMemo } from "react";
import { GoogleMap, MarkerF, PolylineF } from "@react-google-maps/api";
import { TripPlan } from "@/types";

type PlaceSearchMapProps = {
  tripPlan: TripPlan | null;
};

const centerDefault = { lat: 48.1374, lng: 11.5755 }; // Munich

const COLORS = ["#FF5733", "#33C1FF", "#8DFF33", "#FFC133", "#FF33A8", "#33FFB5"];

export default function PlaceSearchMap({ tripPlan }: PlaceSearchMapProps) {
  const center = useMemo(() => {
    if (tripPlan?.days?.[0]?.places?.[0]) {
      return {
        lat: tripPlan.days[0].places[0].lat,
        lng: tripPlan.days[0].places[0].lng,
      };
    }
    return centerDefault;
  }, [tripPlan]);

  return (
    <div className="px-4 py-2">
      <GoogleMap
        zoom={13}
        center={center}
        mapContainerStyle={{ width: "100%", height: "500px" }}
      >
        {tripPlan?.days.map((day, idx) => (
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
