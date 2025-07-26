import React from "react";
import { Mic } from "lucide-react"; 
import "./Micicon.css";

export default function Micicon() {
  return (
    <div className="mic-icon" onClick={() => alert("Mic clicked!")}>
      <Mic size={20} color="#4f46e5" />
    </div>
  );
}
