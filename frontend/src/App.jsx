// App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Jobs from "./pages/jobs";
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Jobs />} />
      </Routes>
    </BrowserRouter>
  );
}
