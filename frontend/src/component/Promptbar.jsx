import React from "react";
import Micicon from "./Micicon";
import "./PromptBar.css";

export default function PromptBar() {
  return (
    <div className="prompt-wrapper">
      <input
        className="prompt-input"
        placeholder="Ask me anything..."
      />
      <Micicon />
    </div>
  );
}
