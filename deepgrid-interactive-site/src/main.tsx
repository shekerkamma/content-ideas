import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { initializeWebMCPPolyfill } from "@mcp-b/webmcp-polyfill";
import App from "./App";
import "./tokens.css";
import "./global.css";
import "./reveal.css";
import "./index.css";

initializeWebMCPPolyfill();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);