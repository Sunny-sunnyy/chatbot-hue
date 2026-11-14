import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "@fontsource/be-vietnam-pro/latin-400.css";
import "@fontsource/be-vietnam-pro/vietnamese-400.css";
import "@fontsource/be-vietnam-pro/latin-600.css";
import "@fontsource/be-vietnam-pro/vietnamese-600.css";
import "@fontsource/noto-serif-display/latin-600.css";
import "@fontsource/noto-serif-display/vietnamese-600.css";
import "./index.css";
import "./hieu_ung.css";
import { batHieuUng } from "./hieuUng.js";
import App from "./App.jsx";

batHieuUng();
createRoot(document.getElementById("root")).render(<StrictMode><App /></StrictMode>);
